from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Harvest, Hive, User
from app.schemas import HarvestCreate, HarvestOut

router = APIRouter(prefix="/api/harvests", tags=["Colheitas"])


@router.get("", response_model=list[HarvestOut])
def list_harvests(
    hive_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(Harvest)
        .join(Hive)
        .filter(Hive.user_id == current_user.id)
        .order_by(Harvest.harvested_at.desc())
    )
    if hive_id:
        query = query.filter(Harvest.hive_id == hive_id)
    return query.all()


@router.post("", response_model=HarvestOut, status_code=status.HTTP_201_CREATED)
def create_harvest(
    payload: HarvestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    hive = db.query(Hive).filter(Hive.id == payload.hive_id, Hive.user_id == current_user.id).first()
    if not hive:
        raise HTTPException(status_code=404, detail="Colmeia não encontrada")
    item = Harvest(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{harvest_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_harvest(
    harvest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (
        db.query(Harvest)
        .join(Hive)
        .filter(Harvest.id == harvest_id, Hive.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Colheita não encontrada")
    db.delete(item)
    db.commit()
