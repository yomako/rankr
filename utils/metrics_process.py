from typing import List

from config import DBConfig
from rankr.db_models import Ranking
from utils import value_process

ranking_systems = tuple(DBConfig.RANKINGS["ranking_systems"])
metric_types = DBConfig.RANKINGS["metrics"]
non_metric_cols = DBConfig.RANKINGS["non_metrics"]


def metrics_process(row: dict) -> List[Ranking]:
    """Converts a .csv row into a list of Ranking objects.

    Args:
        row (dict): The .csv row as a dictionary.

    Returns:
        List[Ranking]: The list of Ranking objects to be attached to an
        institution object.
    """
    metrics = []
    for col in row:
        if col in non_metric_cols:
            continue

        metric = metric_types[col]["name"]
        value_type = metric_types[col]["type"]
        metric_value = value_process(row[col], value_type=value_type)
        metrics.append(
            Ranking(
                metric=metric,
                value=metric_value,
                value_type=value_type,
                ranking_system=row["Ranking System"],
                ranking_type=row["Ranking Type"],
                year=row["Year"],
                field=row["Field"],
                subject=row["Subject"],
            )
        )
    return metrics
