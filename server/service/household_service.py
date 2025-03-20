import json
from fastapi import APIRouter, HTTPException, Depends ,status
from sqlalchemy.orm import Session 
from service.models.household import HouseItemSchema
from service.models.database import get_db




router = APIRouter()


@router.get("/get_items/")
async def get_household_items(db: Session = Depends(get_db)):
    items = db.execute("SELECT item_id, item_name, min_watt_range, max_watt_range FROM meta.houseitem").fetchall()
    return items


@router.get("/get_item_by_name/{item_name}")
async def get_item_by_name(item_name: str, db: Session = Depends(get_db)):
    query = f"SELECT item_id, item_name, min_watt_range, max_watt_range FROM meta.houseitem WHERE item_name = '{item_name}'"
    items = db.execute(query, {"item_name": item_name}).fetchall()
    
    if not items:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return items