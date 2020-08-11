from pathlib import Path
from typing import List

from config import DBConfig
from rankr.db_models import Institution, SessionLocal
from utils import csv_export, csv_size, ranking_process

ranking_systems = DBConfig.RANKINGS["ranking_systems"]

db = SessionLocal()
ili: List[Institution] = db.query(Institution).all()
soup = {}
for inst in ili:
    try:
        soup[inst.country.country][inst.soup] = inst.grid_id
    except KeyError:
        soup[inst.country.country] = {inst.soup: inst.grid_id}
db.close()


not_mached = []
for system in ranking_systems:
    dir_path: Path = DBConfig.MAIN_DIR / system
    if not dir_path.exists():
        continue

    files: List[Path] = sorted(
        [f for f in dir_path.iterdir() if f.suffix == ".csv"], reverse=True
    )
    for cnt, file in enumerate(files, start=1):
        print(f"Processing file ({cnt}/{len(files)}): {file.stem}")
        try:
            db = SessionLocal()
            size = csv_size(file)
            institutions_list, not_mached_list, fuzz_list = ranking_process(
                db, file, soup
            )
            if len(institutions_list) + len(not_mached_list) != size:
                raise ValueError("Some institutions may have been lost!")
            not_mached.extend(not_mached_list)
            if institutions_list:
                db.add_all(institutions_list)
                db.commit()
        except ValueError as exc:
            print(exc)
        finally:
            db.close()

if not_mached:
    csv_export(DBConfig.MAIN_DIR / "not_mached.csv", not_mached)
    print(f"Saved the list of {len(not_mached)} not matched institutions.")

if fuzz_list:
    csv_export(DBConfig.MAIN_DIR / "fuzz_list.csv", fuzz_list)
    print(f"Saved the list of {len(fuzz_list)} fuzzy-matched institutions.")
