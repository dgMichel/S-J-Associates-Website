"""
Booking + payment routes (public + admin).
- POST /bookings                       -> create booking in pending_payment
- GET  /bookings/:reference            -> look up by reference_code
- POST /payments/paypal/create-order   -> create PayPal order for a booking
- POST /payments/paypal/capture/:id    -> capture a PayPal order
- POST /payments/paypal/webhook        -> IPN from PayPal
- GET  /payments/bank-transfer/instructions/:booking_id
- POST /payments/bank-transfer/submit-proof/:booking_id
- GET  /admin/bookings                 -> list all (admin)
- POST /admin/bookings/:id/approve-bank-transfer
- POST /admin/bookings/:id/reject-bank-transfer
- POST /admin/bookings/:id/cancel
"""

from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.config import FRONTEND_URL
from src.db.supabase import get_supabase_admin
from src.utils.auth import get_current_user, require_admin

from src.routes.bookings import paypal as paypal_client
from src.routes.bookings.schemas import (
    BankInstructionsResponse,
    BankProofSubmit,
    BookingCreate,
    BookingListItem,
    BookingRejectRequest,
    BookingResponse,
    PayPalCaptureResponse,
    PayPalCreateOrderRequest,
    PayPalCreateOrderResponse,
)
from src.routes.bookings.service import (
    check_dates_available,
    compute_booking_totals,
    generate_reference_code,
    mark_booking_paid,
    unblock_dates_for_booking,
)


router = APIRouter(tags=["Bookings & Payments"])


# =====================================================
# Helpers
# =====================================================

def _serialize_booking(row: dict) -> BookingResponse:
    return BookingResponse(**row)


def _get_booking_or_404(booking_id: int) -> dict:
    sb = get_supabase_admin()
    res = sb.table("bookings").select("*").eq("id", booking_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return res.data[0]


# =====================================================
# PUBLIC - Booking creation & lookup
# =====================================================

@router.post("/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(body: BookingCreate, user=Depends(get_current_user)):
    totals = compute_booking_totals(body.car_slug, body.start_date, body.end_date, body.nationality)
    check_dates_available(body.car_slug, body.start_date, body.end_date)

    sb = get_supabase_admin()
    user_id = getattr(user, "id", None)

    for _ in range(5):
        ref = generate_reference_code()
        row = {
            "reference_code": ref,
            "user_id": user_id,
            "car_slug": body.car_slug,
            "start_date": body.start_date.isoformat(),
            "end_date": body.end_date.isoformat(),
            "days": totals["days"],
            "customer_name": body.customer_name,
            "customer_email": body.customer_email,
            "customer_phone": body.customer_phone,
            "customer_country": body.customer_country,
            "nationality": body.nationality,
            "currency": totals["currency"],
            "subtotal": float(totals["subtotal"]),
            "deposit": float(totals["deposit"]),
            "total": float(totals["total"]),
            "payment_method": body.payment_method,
            "status": (
                "awaiting_transfer_approval"
                if body.payment_method == "bank_transfer"
                else "pending_payment"
            ),
        }
        try:
            res = sb.table("bookings").insert(row).execute()
            break
        except Exception as e:
            if "duplicate" in str(e).lower() or "unique" in str(e).lower():
                continue
            raise HTTPException(status_code=500, detail=f"DB error: {e}")
    else:
        raise HTTPException(status_code=500, detail="No se pudo generar referencia única")

    if not res.data:
        raise HTTPException(status_code=500, detail="No se pudo crear la reserva")
    return _serialize_booking(res.data[0])


@router.get("/bookings/by-reference/{reference_code}", response_model=BookingResponse)
async def get_booking_by_reference(reference_code: str):
    sb = get_supabase_admin()
    res = (
        sb.table("bookings")
        .select("*")
        .eq("reference_code", reference_code.upper())
        .execute()
    )
    if not res.data:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return _serialize_booking(res.data[0])


# =====================================================
# PUBLIC - PayPal
# =====================================================

@router.post("/payments/paypal/create-order", response_model=PayPalCreateOrderResponse)
async def paypal_create_order(body: PayPalCreateOrderRequest):
    sb = get_supabase_admin()
    booking = _get_booking_or_404(body.booking_id)
    if booking["payment_method"] != "paypal":
        raise HTTPException(400, "Esta reserva no usa PayPal")
    if booking["status"] not in ("pending_payment",):
        raise HTTPException(409, f"Reserva no pagable en estado '{booking['status']}'")

    # PayPal only takes USD. Foreign customers already pay USD; nationals pay XCD.
    # For nationals we charge in USD via PayPal (they see the conversion at checkout).
    if booking["currency"] == "XCD":
        from src.routes.bookings.service import USD_TO_XCD
        amount_usd = (
            __import__("decimal").Decimal(str(booking["total"])) / USD_TO_XCD
        ).quantize(__import__("decimal").Decimal("0.01"))
    else:
        amount_usd = __import__("decimal").Decimal(str(booking["total"]))

    description = f"Car rental: {booking['car_slug']} ({booking['start_date']} → {booking['end_date']})"

    try:
        order = paypal_client.create_order(
            amount_usd=amount_usd,
            reference_code=booking["reference_code"],
            description=description,
            return_url=f"{FRONTEND_URL}/payment-success?ref={booking['reference_code']}",
            cancel_url=f"{FRONTEND_URL}/payment-cancelled?ref={booking['reference_code']}",
        )
    except paypal_client.PayPalError as e:
        raise HTTPException(502, f"PayPal error: {e}")

    approval_url = next(
        (link["href"] for link in order.get("links", []) if link.get("rel") == "approve"),
        None,
    )
    if not approval_url:
        raise HTTPException(502, "PayPal no devolvió approval_url")

    payment_row = {
        "booking_id": booking["id"],
        "provider": "paypal",
        "paypal_order_id": order["id"],
        "amount": float(amount_usd),
        "currency": "USD",
        "status": "created",
        "raw_response": order,
    }
    pay_res = sb.table("payments").insert(payment_row).execute()
    if not pay_res.data:
        raise HTTPException(500, "No se pudo registrar el pago")

    return PayPalCreateOrderResponse(
        payment_id=pay_res.data[0]["id"],
        order_id=order["id"],
        approval_url=approval_url,
    )


@router.post("/payments/paypal/capture/{paypal_order_id}", response_model=PayPalCaptureResponse)
async def paypal_capture(paypal_order_id: str):
    sb = get_supabase_admin()
    pay = (
        sb.table("payments")
        .select("*")
        .eq("paypal_order_id", paypal_order_id)
        .single()
        .execute()
    )
    if not pay.data:
        raise HTTPException(404, "Pago no encontrado")
    if pay.data["status"] == "captured":
        return PayPalCaptureResponse(
            payment_id=pay.data["id"],
            status="captured",
            booking_status="paid",
        )

    try:
        order = paypal_client.capture_order(paypal_order_id)
    except paypal_client.PayPalError as e:
        raise HTTPException(502, f"PayPal capture error: {e}")

    status_name = order.get("status")
    if status_name != "COMPLETED":
        sb.table("payments").update({"status": "failed", "raw_response": order}).eq(
            "id", pay.data["id"]
        ).execute()
        raise HTTPException(402, f"Pago no completado: {status_name}")

    # Pull payer info from capture
    payer = (order.get("payer") or {})
    capture = (
        order.get("purchase_units", [{}])[0]
        .get("payments", {})
        .get("captures", [{}])[0]
    )

    sb.table("payments").update({
        "status": "captured",
        "paypal_capture_id": capture.get("id"),
        "paypal_payer_id": payer.get("payer_id"),
        "paypal_payer_email": payer.get("email_address"),
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "raw_response": order,
    }).eq("id", pay.data["id"]).execute()

    booking = mark_booking_paid(pay.data["booking_id"])

    return PayPalCaptureResponse(
        payment_id=pay.data["id"],
        status="captured",
        booking_status=booking["status"],
    )


@router.post("/payments/paypal/webhook", status_code=204)
async def paypal_webhook(request: Request):
    """PayPal IPN. Idempotent. Verifies signature."""
    body = await request.json()
    headers = request.headers

    if not paypal_client.verify_webhook_signature(
        auth_algo=headers.get("PAYPAL-AUTH-ALGO", ""),
        cert_url=headers.get("PAYPAL-CERT-URL", ""),
        transmission_id=headers.get("PAYPAL-TRANSMISSION-ID", ""),
        transmission_sig=headers.get("PAYPAL-TRANSMISSION-SIG", ""),
        transmission_time=headers.get("PAYPAL-TRANSMISSION-TIME", ""),
        webhook_id=headers.get("PAYPAL-WEBHOOK-ID", ""),
        webhook_event=body,
    ):
        raise HTTPException(401, "Invalid webhook signature")

    event_type = body.get("event_type")
    resource = body.get("resource") or {}
    order_id = resource.get("id")

    if event_type == "CHECKOUT.ORDER.APPROVED":
        # User approved but didn't return to our site - capture it server-side
        try:
            order = paypal_client.capture_order(order_id)
            if order.get("status") == "COMPLETED":
                sb = get_supabase_admin()
                pay = (
                    sb.table("payments")
                    .select("*")
                    .eq("paypal_order_id", order_id)
                    .single()
                    .execute()
                )
                if pay.data and pay.data["status"] != "captured":
                    payer = order.get("payer") or {}
                    capture = (
                        order.get("purchase_units", [{}])[0]
                        .get("payments", {})
                        .get("captures", [{}])[0]
                    )
                    sb.table("payments").update({
                        "status": "captured",
                        "paypal_capture_id": capture.get("id"),
                        "paypal_payer_id": payer.get("payer_id"),
                        "paypal_payer_email": payer.get("email_address"),
                        "captured_at": datetime.now(timezone.utc).isoformat(),
                        "raw_response": order,
                    }).eq("id", pay.data["id"]).execute()
                    mark_booking_paid(pay.data["booking_id"])
        except paypal_client.PayPalError:
            pass  # log and retry later in production

    return None


# =====================================================
# PUBLIC - Bank transfer
# =====================================================

@router.get("/payments/bank-transfer/instructions/{booking_id}", response_model=BankInstructionsResponse)
async def bank_instructions(booking_id: int):
    sb = get_supabase_admin()
    booking = _get_booking_or_404(booking_id)
    if booking["payment_method"] != "bank_transfer":
        raise HTTPException(400, "Esta reserva no usa transferencia bancaria")
    if booking["status"] not in ("pending_payment", "awaiting_transfer_approval"):
        raise HTTPException(409, "La reserva ya no acepta transferencia")

    acc = (
        sb.table("bank_accounts")
        .select("*")
        .eq("currency", booking["currency"])
        .eq("is_active", True)
        .order("display_order")
        .limit(1)
        .execute()
    )
    if not acc.data:
        raise HTTPException(500, "No hay cuentas bancarias configuradas para esta moneda")
    a = acc.data[0]

    return BankInstructionsResponse(
        booking_id=booking["id"],
        reference_code=booking["reference_code"],
        bank_name=a["bank_name"],
        account_name=a["account_name"],
        account_number=a["account_number"],
        swift_code=a.get("swift_code"),
        currency=a["currency"],
        amount=booking["total"],
        instructions=a.get("instructions"),
    )


@router.post("/payments/bank-transfer/submit-proof/{booking_id}", status_code=204)
async def bank_submit_proof(booking_id: int, body: BankProofSubmit, user=Depends(get_current_user)):
    sb = get_supabase_admin()
    booking = _get_booking_or_404(booking_id)
    if booking["payment_method"] != "bank_transfer":
        raise HTTPException(400, "Esta reserva no usa transferencia bancaria")
    if booking["status"] not in ("pending_payment", "awaiting_transfer_approval"):
        raise HTTPException(409, "La reserva no acepta comprobante en este estado")

    sb.table("bank_transfers").upsert(
        {
            "booking_id": booking_id,
            "reference_code": booking["reference_code"],
            "proof_url": body.proof_url,
            "proof_uploaded_at": datetime.now(timezone.utc).isoformat(),
        },
        on_conflict="booking_id",
    ).execute()

    sb.table("bookings").update({"status": "awaiting_transfer_approval"}).eq(
        "id", booking_id
    ).execute()
    return None


# =====================================================
# ADMIN
# =====================================================

@router.get("/admin/bookings", response_model=list[BookingListItem], dependencies=[Depends(require_admin)])
async def admin_list_bookings(status_filter: str | None = None):
    sb = get_supabase_admin()
    q = sb.table("bookings").select("*").order("created_at", desc=True)
    if status_filter:
        q = q.eq("status", status_filter)
    res = q.execute()
    return [BookingListItem(**row) for row in (res.data or [])]


@router.post("/admin/bookings/{booking_id}/approve-bank-transfer", response_model=BookingResponse, dependencies=[Depends(require_admin)])
async def admin_approve_bank_transfer(booking_id: int, user=Depends(require_admin)):
    sb = get_supabase_admin()
    booking = _get_booking_or_404(booking_id)
    if booking["payment_method"] != "bank_transfer":
        raise HTTPException(400, "Esta reserva no es por transferencia")
    if booking["status"] not in ("awaiting_transfer_approval", "pending_payment"):
        raise HTTPException(409, f"Estado inválido: {booking['status']}")

    sb.table("bank_transfers").update({
        "approved_by": getattr(user, "id", None),
        "approved_at": datetime.now(timezone.utc).isoformat(),
    }).eq("booking_id", booking_id).execute()

    updated = mark_booking_paid(booking_id)
    return _serialize_booking(updated)


@router.post("/admin/bookings/{booking_id}/reject-bank-transfer", response_model=BookingResponse, dependencies=[Depends(require_admin)])
async def admin_reject_bank_transfer(booking_id: int, body: BookingRejectRequest, user=Depends(require_admin)):
    sb = get_supabase_admin()
    booking = _get_booking_or_404(booking_id)
    if booking["payment_method"] != "bank_transfer":
        raise HTTPException(400, "Esta reserva no es por transferencia")

    sb.table("bank_transfers").update({
        "rejection_reason": body.reason,
        "rejected_by": getattr(user, "id", None),
        "rejected_at": datetime.now(timezone.utc).isoformat(),
    }).eq("booking_id", booking_id).execute()

    res = sb.table("bookings").update({"status": "rejected"}).eq("id", booking_id).execute()
    return _serialize_booking(res.data[0])


@router.post("/admin/bookings/{booking_id}/cancel", response_model=BookingResponse, dependencies=[Depends(require_admin)])
async def admin_cancel_booking(booking_id: int):
    sb = get_supabase_admin()
    booking = _get_booking_or_404(booking_id)

    if booking["status"] == "paid":
        unblock_dates_for_booking(booking_id)

    res = sb.table("bookings").update({"status": "cancelled"}).eq("id", booking_id).execute()
    return _serialize_booking(res.data[0])
