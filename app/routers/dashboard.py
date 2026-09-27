from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Harvest, Hive, Inspection, User
from app.schemas import DashboardSummary, InspectionOut
from app.services import health_score

router = APIRouter(prefix="/api/dashboard", tags=["Painel"])


@router.get("/summary", response_model=DashboardSummary)
def summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()
    hives = db.query(Hive).filter(Hive.user_id == current_user.id)
    total_hives = hives.count()
    active_hives = hives.filter(Hive.status == "ativa").count()

    inspections_this_month = (
        db.query(Inspection)
        .join(Hive)
        .filter(
            Hive.user_id == current_user.id,
            extract("year", Inspection.inspected_at) == today.year,
            extract("month", Inspection.inspected_at) == today.month,
        )
        .count()
    )

    honey_this_year = (
        db.query(func.coalesce(func.sum(Harvest.honey_kg), 0))
        .join(Hive)
        .filter(Hive.user_id == current_user.id, extract("year", Harvest.harvested_at) == today.year)
        .scalar()
    )

    status_rows = (
        db.query(Hive.status, func.count(Hive.id))
        .filter(Hive.user_id == current_user.id)
        .group_by(Hive.status)
        .all()
    )
    status_distribution = {status: count for status, count in status_rows}

    month_rows = (
        db.query(extract("month", Harvest.harvested_at), func.sum(Harvest.honey_kg))
        .join(Hive)
        .filter(Hive.user_id == current_user.id, extract("year", Harvest.harvested_at) == today.year)
        .group_by(extract("month", Harvest.harvested_at))
        .all()
    )
    month_map = {int(month): float(total) for month, total in month_rows}
    honey_by_month = [
        {"month": month, "honey_kg": month_map.get(month, 0.0)} for month in range(1, 13)
    ]

    recent = (
        db.query(Inspection)
        .join(Hive)
        .filter(Hive.user_id == current_user.id)
        .order_by(Inspection.inspected_at.desc())
        .limit(5)
        .all()
    )
    recent_out = []
    for item in recent:
        data = InspectionOut.model_validate(item)
        recent_out.append(data.model_copy(update={"health_score": health_score(item)}))

    return DashboardSummary(
        total_hives=total_hives,
        active_hives=active_hives,
        inspections_this_month=inspections_this_month,
        honey_this_year_kg=float(honey_this_year or 0),
        status_distribution=status_distribution,
        honey_by_month=honey_by_month,
        recent_inspections=recent_out,
    )
