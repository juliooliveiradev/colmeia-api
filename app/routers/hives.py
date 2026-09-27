from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Hive, User
from app.schemas import HiveCreate, HiveOut, HiveUpdate, PaginatedHives

router = APIRouter(prefix="/api/hives", tags=["Colmeias"])

ALLOWED_SORT = {"name", "status", "installed_at", "created_at", "neighborhood"}


@router.get("", response_model=PaginatedHives)
def list_hives(
    q: str | None = Query(default=None, description="Busca por nome, bairro ou espécie"),
    status_filter: str | None = Query(default=None, alias="status"),
    sort_by: str = Query(default="created_at"),
    sort_dir: str = Query(default="desc", pattern="^(asc|desc)$"),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Hive).filter(Hive.user_id == current_user.id)

    if q:
        like = f"%{q.strip()}%"
        query = query.filter(
            or_(Hive.name.ilike(like), Hive.neighborhood.ilike(like), Hive.species.ilike(like))
        )
    if status_filter:
        query = query.filter(Hive.status == status_filter)

    column_name = sort_by if sort_by in ALLOWED_SORT else "created_at"
    column = getattr(Hive, column_name)
    query = query.order_by(column.asc() if sort_dir == "asc" else column.desc())

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedHives(items=items, total=total, page=page, page_size=page_size)


@router.post("", response_model=HiveOut, status_code=status.HTTP_201_CREATED)
def create_hive(
    payload: HiveCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    hive = Hive(user_id=current_user.id, **payload.model_dump())
    db.add(hive)
    db.commit()
    db.refresh(hive)
    return hive


@router.get("/{hive_id}", response_model=HiveOut)
def get_hive(
    hive_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _owned_hive(db, hive_id, current_user.id)


@router.put("/{hive_id}", response_model=HiveOut)
def update_hive(
    hive_id: int,
    payload: HiveUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    hive = _owned_hive(db, hive_id, current_user.id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(hive, key, value)
    db.commit()
    db.refresh(hive)
    return hive


@router.delete("/{hive_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hive(
    hive_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    hive = _owned_hive(db, hive_id, current_user.id)
    db.delete(hive)
    db.commit()


def _owned_hive(db: Session, hive_id: int, user_id: int) -> Hive:
    hive = db.query(Hive).filter(Hive.id == hive_id, Hive.user_id == user_id).first()
    if not hive:
        raise HTTPException(status_code=404, detail="Colmeia não encontrada")
    return hive
