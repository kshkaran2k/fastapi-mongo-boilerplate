from datetime import datetime, timezone
from fastapi import APIRouter

from app.db.mongodb import MongoDB
from app.schemas.inventory import InventoryAdjust
from app.schemas.response import APIResponse, failure_response, success_response

router = APIRouter(prefix="/api/v1/inventory", tags=["inventory"])


@router.get("/{sku}", response_model=APIResponse)
async def get_inventory(sku: str):
    ok, item = await MongoDB.find_one("inventory", {"sku": sku})
    if not ok:
        return await failure_response(status_code=400, message="Inventory not found")
    return await success_response(message="Inventory fetched", data=item)


@router.post("/adjust", response_model=APIResponse)
async def adjust_inventory(payload: InventoryAdjust):
    now = datetime.now(timezone.utc).isoformat()
    ok, _ = await MongoDB.increment(
        "inventory",
        {"sku": payload.sku},
        {"available": payload.delta},
        set_data={"updated_at": now},
        upsert=True,
    )
    if not ok:
        return await failure_response(status_code=500, message="Failed to adjust inventory")
    _, item = await MongoDB.find_one("inventory", {"sku": payload.sku})
    return await success_response(message="Inventory adjusted", data=item)
