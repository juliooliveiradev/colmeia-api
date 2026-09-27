from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Hive, Inspection, User
from app.schemas import InspectionCreate, InspectionOut, InspectionUpdate
from app.services import health_score

router = APIRouter(prefix="/api/inspections", tags=["Revisões"])


def _to_out(item: Inspection) -> InspectionOut:
    data = InspectionOut.model_validate(item)
    return data.model_copy(update={"health_score": health_score(item)})


@router.get("", response_model=list[InspectionOut])
def list_inspections(
    hive_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(Inspection)
        .join(Hive)
        .filter(Hive.user_id == current_user.id)
        .order_by(Inspection.inspected_at.desc())
    )
    if hive_id:
        query = query.filter(Inspection.hive_id == hive_id)
    return [_to_out(item) for item in query.all()]


@router.post("", response_model=InspectionOut, status_code=status.HTTP_201_CREATED)
def create_inspection(
    payload: InspectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _owned_hive(db, payload.hive_id, current_user.id)
    item = Inspection(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return _to_out(item)


@router.put("/{inspection_id}", response_model=InspectionOut)
def update_inspection(
    inspection_id: int,
    payload: InspectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = _owned_inspection(db, inspection_id, current_user.id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return _to_out(item)


@router.delete("/{inspection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inspection(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = _owned_inspection(db, inspection_id, current_user.id)
    db.delete(item)
    db.commit()


def _owned_hive(db: Session, hive_id: int, user_id: int) -> Hive:
    hive = db.query(Hive).filter(Hive.id == hive_id, Hive.user_id == user_id).first()
    if not hive:
        raise HTTPException(status_code=404, detail="Colmeia não encontrada")
    return hive


def _owned_inspection(db: Session, inspection_id: int, user_id: int) -> Inspection:
    item = (
        db.query(Inspection)
        .join(Hive)
        .filter(Inspection.id == inspection_id, Hive.user_id == user_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Revisão não encontrada")
    return item
