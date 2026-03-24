from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class LeitnerConfig:
    initial_level: int = 0
    levels: int = 5
    shifts: tuple[int, ...] = (2, 4, 7, 10)


@dataclass
class Card:
    name: str
    rep_date: date
    link: str | None = None

    @classmethod
    def from_row(cls, row: tuple[str, str, str]) -> "Card":
        name, link, date_str = row
        link = link if link and link != "None" else None
        return cls(name=name, rep_date=date.fromisoformat(date_str), link=link)

    def shift_date(self, days: int, from_today: bool = False) -> None:
        base = date.today() if from_today else self.rep_date
        self.rep_date = base + timedelta(days=days)

    def __str__(self) -> str:
        if self.link:
            return f"[{self.name}]({self.link}) | {self.rep_date}"
        return f"{self.name} | {self.rep_date}"


def parse_short_date(s: str) -> date:
    """Parse 'dd.mm' to a date in the current year."""
    day, month = s.strip().split(".")
    return date(date.today().year, int(month), int(day))
