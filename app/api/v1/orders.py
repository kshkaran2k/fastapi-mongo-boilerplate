import uuid
from datetime import datetime, timezone

from fastapi import APIRouter

from app.db.mongodb import MongoDB
from app.schemas.orders import OrderCreate
from app.schemas.response import APIResponse, failure_response, success_response

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


@router.post("", response_model=APIResponse)
async def create_order(payload: OrderCreate):
    now = datetime.now(timezone.utc).isoformat()
    order = {
        "order_id": f"ord_{uuid.uuid4().hex[:12]}",
        "customer_id": payload.customer_id,
        "items": [item.model_dump() for item in payload.items],
        "total_amount": sum(item.qty * item.unit_price for item in payload.items),
        "status": "PENDING",
        "created_at": now,
        "updated_at": now,
    }
    ok, _ = await MongoDB.insert_one("orders", order)
    if not ok:
        return await failure_response(status_code=500, message="Failed to create order")
    return await success_response(message="Order created", data=order)


@router.get("/{order_id}", response_model=APIResponse)
async def get_order(order_id: str):
    ok, order = await MongoDB.find_one("orders", {"order_id": order_id})
    if not ok:
        return await failure_response(status_code=400, message="Order not found")
    return await success_response(message="Order fetched", data=order)
