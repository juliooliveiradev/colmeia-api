from datetime import date

from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models import Harvest, Hive, Inspection, User


def seed_if_empty(db: Session) -> None:
    if db.query(User).first():
        return

    user = User(
        name="Ana Apicultora",
        email="apicultor@colmeia.dev",
        password_hash=hash_password("colmeia123"),
    )
    db.add(user)
    db.flush()

    hives = [
        Hive(
            user_id=user.id,
            name="Colmeia Ibirapuera",
            species="Apis mellifera",
            neighborhood="Parque Ibirapuera",
            latitude=-23.587416,
            longitude=-46.657634,
            status="ativa",
            installed_at=date(2024, 8, 12),
            notes="Núcleo urbano sombreado, próximo a jardins floridos.",
        ),
        Hive(
            user_id=user.id,
            name="Colmeia Horto",
            species="Apis mellifera",
            neighborhood="Horto Florestal",
            latitude=-23.457800,
            longitude=-46.631200,
            status="enxameacao",
            installed_at=date(2025, 1, 20),
            notes="Sinais de preparação de enxame. Atenção na próxima revisão.",
        ),
        Hive(
            user_id=user.id,
            name="Colmeia USP",
            species="Melipona quadrifasciata",
            neighborhood="Cidade Universitária",
            latitude=-23.561400,
            longitude=-46.730800,
            status="ativa",
            installed_at=date(2023, 11, 3),
            notes="Abelha nativa sem ferrão. Produção de mel de alto valor.",
        ),
    ]
    db.add_all(hives)
    db.flush()

    db.add_all(
        [
            Inspection(
                hive_id=hives[0].id,
                inspected_at=date(2026, 8, 2),
                queen_seen=True,
                brood_pattern="forte",
                pest_signs=False,
                temperament="calmo",
                notes="Rainha marcada, crias compactas e bastante pólen.",
            ),
            Inspection(
                hive_id=hives[1].id,
                inspected_at=date(2026, 8, 18),
                queen_seen=False,
                brood_pattern="regular",
                pest_signs=False,
                temperament="alerta",
                notes="Células reais visíveis. Planejar divisão.",
            ),
            Inspection(
                hive_id=hives[2].id,
                inspected_at=date(2026, 9, 5),
                queen_seen=True,
                brood_pattern="forte",
                pest_signs=False,
                temperament="calmo",
                notes="Potinhos de mel quase cheios.",
            ),
        ]
    )
    db.add_all(
        [
            Harvest(
                hive_id=hives[0].id,
                harvested_at=date(2026, 3, 15),
                honey_kg=8.4,
                wax_g=220,
                notes="Safra de verão, aroma floral.",
            ),
            Harvest(
                hive_id=hives[0].id,
                harvested_at=date(2026, 7, 10),
                honey_kg=5.1,
                wax_g=140,
                notes="Mel mais denso, boa umidade.",
            ),
            Harvest(
                hive_id=hives[2].id,
                harvested_at=date(2026, 6, 22),
                honey_kg=1.8,
                wax_g=40,
                notes="Mel de jataí, rendimento típico da espécie.",
            ),
        ]
    )
    db.commit()
