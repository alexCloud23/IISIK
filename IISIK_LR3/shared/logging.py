from __future__ import annotations

import logging


def setup_logging(service_name: str, level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format=f"%(asctime)s %(levelname)s [{service_name}] %(name)s: %(message)s",
    )
