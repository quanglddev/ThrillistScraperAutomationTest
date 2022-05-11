from dataclasses import dataclass


@dataclass
class Article:
    activity: str
    href: str
    title: str
    description: str
