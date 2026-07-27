from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import stripe
from src.config import STRIPE_SECRET_KEY, STRIPE_CLIENT_ID, STRIPE_WEBHOOK_SECRET, FRONTEND_URL
from src.db.session import get_db
from src.db import models
from src.utils.auth import get_current_active_user
from src.routes.payments.schemas import CreateCheckoutSessionRequest, CreateCheckoutSessionResponse

stripe.api_key = STRIPE_SECRET_KEY

router = APIRouter(prefix="/payments", tags=["Payments"])


async def get_connected_account(db: AsyncSession) -> models.StripeAccount | None:
    result = await db.execute(
        select(models.StripeAccount).filter(models.StripeAccount.is_active == True)
    )
    return result.scalars().first()


@router.get("/connect/url")
async def connect_stripe_url():
    if not STRIPE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Stripe Connect no está configurado",
        )
    redirect_uri = f"{FRONTEND_URL.rstrip('/')}/admin?stripe=callback"
    url = (
        f"https://connect.stripe.com/express/oauth/authorize"
        f"?client_id={STRIPE_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&stripe_user[email]="
    )
    return {"url": url}


@router.get("/connect/callback")
async def connect_stripe_callback(code: str = "", db: AsyncSession = Depends(get_db)):
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código de autorización requerido",
        )
    try:
        response = stripe.OAuth.token(grant_type="authorization_code", code=code)
    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al conectar Stripe: {e.user_message or 'Error de Stripe'}",
        )

    existing = await db.execute(
        select(models.StripeAccount).filter(
            models.StripeAccount.stripe_user_id == response["stripe_user_id"]
        )
    )
    account = existing.scalars().first()
    if account:
        account.access_token = response.get("access_token")
        account.refresh_token = response.get("refresh_token")
        account.stripe_publishable_key = response.get("stripe_publishable_key")
        account.is_active = True
    else:
        account = models.StripeAccount(
            stripe_user_id=response["stripe_user_id"],
            stripe_publishable_key=response.get("stripe_publishable_key"),
            access_token=response.get("access_token"),
            refresh_token=response.get("refresh_token"),
            is_active=True,
        )
        db.add(account)

    result = await db.execute(
        select(models.StripeAccount).filter(
            models.StripeAccount.stripe_user_id != response["stripe_user_id"],
            models.StripeAccount.is_active == True,
        )
    )
    for old in result.scalars().all():
        old.is_active = False

    await db.commit()
    return {
        "status": "connected",
        "stripe_user_id": response["stripe_user_id"],
    }


@router.get("/connect/status")
async def connect_stripe_status(db: AsyncSession = Depends(get_db)):
    account = await get_connected_account(db)
    if not account:
        return {"connected": False}
    try:
        acct = stripe.Account.retrieve(account.stripe_user_id)
        return {
            "connected": True,
            "charges_enabled": acct.get("charges_enabled", False),
            "details_submitted": acct.get("details_submitted", False),
            "email": acct.get("email", ""),
        }
    except stripe.error.StripeError:
        return {"connected": True, "charges_enabled": False, "details_submitted": False}


@router.post("/create-checkout-session", response_model=CreateCheckoutSessionResponse)
async def create_checkout_session(
    body: CreateCheckoutSessionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    try:
        start_date = datetime.strptime(body.startDate, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato de fecha inválido. Use YYYY-MM-DD",
        )

    if body.days < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La reserva debe ser de al menos 1 día",
        )

    end_date = start_date + timedelta(days=body.days - 1)

    if start_date < datetime.utcnow().date():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser en el pasado",
        )

    connected = await get_connected_account(db)
    if not connected:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="El sistema de pagos no está configurado. Contacte al administrador.",
        )

    result = await db.execute(
        select(models.Booking).filter(
            models.Booking.car_slug == body.car,
            models.Booking.status.in_(["pending", "completed"]),
            models.Booking.start_date <= end_date,
            models.Booking.end_date >= start_date,
        )
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El vehículo no está disponible en las fechas seleccionadas",
        )

    booking = models.Booking(
        car_slug=body.car,
        start_date=start_date,
        end_date=end_date,
        days=body.days,
        amount=body.amount,
        currency="usd",
        status="pending",
        user_id=current_user.id,
    )
    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"Renta de auto - {body.car}",
                            "description": f"{body.days} día(s) desde {body.startDate}",
                        },
                        "unit_amount": int(body.amount * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=f"{FRONTEND_URL}/booking-confirmed?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}/booking-cancelled",
            metadata={
                "booking_id": str(booking.id),
                "car_slug": body.car,
                "start_date": body.startDate,
                "end_date": end_date.isoformat(),
                "days": str(body.days),
            },
            payment_intent_data={
                "transfer_data": {
                    "destination": connected.stripe_user_id,
                },
                "application_fee_amount": 0,
            },
        )

        booking.stripe_session_id = session.id
        await db.commit()

        return CreateCheckoutSessionResponse(url=session.url)

    except stripe.error.StripeError as e:
        await db.delete(booking)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al procesar el pago: {e.user_message or 'Error de Stripe'}",
        )


@router.post("/webhook")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Firma de Stripe no encontrada",
        )

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload inválido",
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Firma de Stripe inválida",
        )

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        booking_id = session.get("metadata", {}).get("booking_id")
        if booking_id:
            result = await db.execute(
                select(models.Booking).filter(models.Booking.id == int(booking_id))
            )
            booking = result.scalars().first()
            if booking:
                booking.status = "completed"
                booking.stripe_payment_intent_id = session.get("payment_intent")
                booking.customer_name = session.get("customer_details", {}).get("name")
                booking.customer_email = session.get("customer_details", {}).get("email")
                await db.commit()

    elif event["type"] == "checkout.session.expired":
        session = event["data"]["object"]
        booking_id = session.get("metadata", {}).get("booking_id")
        if booking_id:
            result = await db.execute(
                select(models.Booking).filter(models.Booking.id == int(booking_id))
            )
            booking = result.scalars().first()
            if booking and booking.status == "pending":
                booking.status = "cancelled"
                await db.commit()

    return {"status": "ok"}



