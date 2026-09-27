from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Julio Apicultor",
                "email": "julio@colmeia.dev",
                "password": "colmeia123",
            }
        }
    )

    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=80)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    created_at: datetime


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class HiveCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Colmeia Vila Mariana",
                "species": "Apis mellifera",
                "neighborhood": "Vila Mariana",
                "latitude": -23.589,
                "longitude": -46.634,
                "status": "ativa",
                "installed_at": "2026-03-10",
                "notes": "Caixa nova, próximo a jardim comunitário.",
            }
        }
    )

    name: str = Field(min_length=2, max_length=120)
    species: str = "Apis mellifera"
    neighborhood: str = ""
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    status: str = "ativa"
    installed_at: date
    notes: str = ""


class HiveUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Colmeia Vila Mariana",
                "status": "enxameacao",
                "notes": "Sinais de enxameação. Planejar divisão.",
            }
        }
    )

    name: str | None = Field(default=None, min_length=2, max_length=120)
    species: str | None = None
    neighborhood: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    status: str | None = None
    installed_at: date | None = None
    notes: str | None = None


class HiveOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    species: str
    neighborhood: str
    latitude: float
    longitude: float
    status: str
    installed_at: date
    notes: str
    created_at: datetime


class InspectionCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "hive_id": 1,
                "inspected_at": "2026-09-20",
                "queen_seen": True,
                "brood_pattern": "forte",
                "pest_signs": False,
                "temperament": "calmo",
                "notes": "Rainha vista, crias compactas e bastante pólen.",
            }
        }
    )

    hive_id: int
    inspected_at: date
    queen_seen: bool = False
    brood_pattern: str = "regular"
    pest_signs: bool = False
    temperament: str = "calmo"
    notes: str = ""


class InspectionUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "queen_seen": False,
                "brood_pattern": "regular",
                "pest_signs": True,
                "temperament": "alerta",
                "notes": "Possível varroa. Revisitar em 7 dias.",
            }
        }
    )

    inspected_at: date | None = None
    queen_seen: bool | None = None
    brood_pattern: str | None = None
    pest_signs: bool | None = None
    temperament: str | None = None
    notes: str | None = None


class InspectionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hive_id: int
    inspected_at: date
    queen_seen: bool
    brood_pattern: str
    pest_signs: bool
    temperament: str
    notes: str
    created_at: datetime
    health_score: int = 0


class HarvestCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "hive_id": 1,
                "harvested_at": "2026-09-15",
                "honey_kg": 6.4,
                "wax_g": 180,
                "notes": "Safra de inverno, mel mais denso.",
            }
        }
    )

    hive_id: int
    harvested_at: date
    honey_kg: float = Field(ge=0)
    wax_g: float = Field(default=0, ge=0)
    notes: str = ""


class HarvestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hive_id: int
    harvested_at: date
    honey_kg: float
    wax_g: float
    notes: str
    created_at: datetime


class PaginatedHives(BaseModel):
    items: list[HiveOut]
    total: int
    page: int
    page_size: int


class DashboardSummary(BaseModel):
    total_hives: int
    active_hives: int
    inspections_this_month: int
    honey_this_year_kg: float
    status_distribution: dict[str, int]
    honey_by_month: list[dict]
    recent_inspections: list[InspectionOut]
