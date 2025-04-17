from dataclasses import dataclass
from typing import Optional

@dataclass
class Genre:
    """Entité Genre dans la couche domaine, indépendante de tout framework"""
    id: int
    name: str
