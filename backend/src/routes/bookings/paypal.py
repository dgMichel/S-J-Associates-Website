"""Minimal PayPal REST API client (orders + capture + webhook verification)."""

import base64
import json
from decimal import Decimal
from typing import Any

import httpx

from src.config import PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, PAYPAL_MODE, PAYPAL_WEBHOOK_ID


def _base_url() -> str:
    return (
        "https://api-m.sandbox.paypal.com"
        if PAYPAL_MODE == "sandbox"
        else "https://api-m.paypal.com"
    )


class PayPalError(Exception):
    pass


def _get_access_token() -> str:
    if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
        raise PayPalError("PayPal credentials not configured")
    auth = base64.b64encode(
        f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}".encode()
    ).decode()
    with httpx.Client(timeout=15.0) as client:
        resp = client.post(
            f"{_base_url()}/v1/oauth2/token",
            headers={
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"grant_type": "client_credentials"},
        )
        if resp.status_code != 200:
            raise PayPalError(f"OAuth failed: {resp.status_code} {resp.text}")
        return resp.json()["access_token"]


def create_order(
    *,
    amount_usd: Decimal,
    reference_code: str,
    description: str,
    return_url: str,
    cancel_url: str,
) -> dict:
    """Create a PayPal order. Amount must be in USD (we only accept USD in PayPal)."""
    access_token = _get_access_token()
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "reference_id": reference_code,
                "description": description,
                "amount": {
                    "currency_code": "USD",
                    "value": str(amount_usd.quantize(Decimal('0.01'))),
                },
                "custom_id": reference_code,
            }
        ],
        "application_context": {
            "brand_name": "5J & Associates",
            "shipping_preference": "NO_SHIPPING",
            "user_action": "PAY_NOW",
            "return_url": return_url,
            "cancel_url": cancel_url,
        },
    }
    with httpx.Client(timeout=15.0) as client:
        resp = client.post(
            f"{_base_url()}/v2/checkout/orders",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
    if resp.status_code not in (200, 201):
        raise PayPalError(f"create_order failed: {resp.status_code} {resp.text}")
    return resp.json()


def capture_order(order_id: str) -> dict:
    access_token = _get_access_token()
    with httpx.Client(timeout=15.0) as client:
        resp = client.post(
            f"{_base_url()}/v2/checkout/orders/{order_id}/capture",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
        )
    if resp.status_code not in (200, 201):
        raise PayPalError(f"capture_order failed: {resp.status_code} {resp.text}")
    return resp.json()


def get_order(order_id: str) -> dict:
    access_token = _get_access_token()
    with httpx.Client(timeout=15.0) as client:
        resp = client.get(
            f"{_base_url()}/v2/checkout/orders/{order_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
    if resp.status_code != 200:
        raise PayPalError(f"get_order failed: {resp.status_code} {resp.text}")
    return resp.json()


def verify_webhook_signature(
    *,
    auth_algo: str,
    cert_url: str,
    transmission_id: str,
    transmission_sig: str,
    transmission_time: str,
    webhook_id: str,
    webhook_event: dict,
) -> bool:
    """
    Verify a PayPal webhook using the official verification endpoint.
    See: https://developer.paypal.com/api/rest/webhooks/event-names/#verify-webhook-signature
    """
    if PAYPAL_WEBHOOK_ID and webhook_id != PAYPAL_WEBHOOK_ID:
        return False

    access_token = _get_access_token()
    payload = {
        "auth_algo": auth_algo,
        "cert_url": cert_url,
        "transmission_id": transmission_id,
        "transmission_sig": transmission_sig,
        "transmission_time": transmission_time,
        "webhook_id": webhook_id,
        "webhook_event": webhook_event,
    }
    with httpx.Client(timeout=15.0) as client:
        resp = client.post(
            f"{_base_url()}/v1/notifications/verify-webhook-signature",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
    if resp.status_code != 200:
        return False
    return resp.json().get("verification_status") == "SUCCESS"
