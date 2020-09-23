from dataclasses import dataclass

from pydantic import HttpUrl


@dataclass
class Beer:
    title: str
    volume: float
    price: float
    link: HttpUrl
