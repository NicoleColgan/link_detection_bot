from typing import List, Dict
from datetime import datetime
import csv

"""

Is this right for the output pah stripping the /


"""


def write_csv(rows: List[Dict], outdir: str = ".") -> str:
    filename = f"url_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    path = f"{outdir.rstrip('/')}/{filename}"
    field_names = ["original_url", "usable", "reason", "resolution_steps", "status_code", "response_url"]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                "original_url": r.get("original_url"),
                "usable": r.get("usable"),
                "reason": r.get("reason"),
                "resolution_steps": r.get("resolution_steps"),
                "status_code": r.get("status_code"),
                "response_url": r.get("response_url"),
            })
    return path