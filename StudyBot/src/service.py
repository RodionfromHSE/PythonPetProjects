from datetime import date, timedelta

from src.models import Card, LeitnerConfig, parse_short_date
from src.repository import CardRepository


class LeitnerService:
    def __init__(self, repo: CardRepository, config: LeitnerConfig):
        self._repo = repo
        self._config = config

    def add_items(
        self,
        raw: str,
        date_str: str | None = None,
        reformat: bool = False,
    ) -> list[Card]:
        """Add cards from 'item1 + item2 + ...' string."""
        names = [n.strip() for n in raw.split(" + ")]
        if reformat:
            yesterday = (date.today() - timedelta(days=1)).strftime("%d.%m")
            names = [f"{n} {yesterday}" for n in names]

        rep_date = parse_short_date(date_str) if date_str else date.today()
        cards = []
        for name in names:
            card = Card(name=name, rep_date=rep_date)
            self._repo.add(card, self._config.initial_level)
            cards.append(card)
        self._repo.commit()
        return cards

    def get_today(self) -> list[Card]:
        return self._repo.get_by_date(date.today())

    def get_by_date(self, date_str: str) -> list[Card]:
        return self._repo.get_by_date(parse_short_date(date_str))

    def get_not_repeated(self, days_range: int = 31) -> list[Card]:
        cards: list[Card] = []
        today = date.today()
        for delta in range(days_range):
            cards.extend(self._repo.get_by_date(today - timedelta(days=delta)))
        return cards

    def shift_today(self) -> None:
        self._repo.shift_cards(date.today())
        self._repo.commit()

    def shift_from(self, date_str: str) -> None:
        start = parse_short_date(date_str)
        self._repo.shift_range(start, date.today() + timedelta(days=1))
        self._repo.commit()

    def shift_all(self, from_today: bool = False) -> None:
        start = date.today() - timedelta(days=31)
        end = date.today() + timedelta(days=1)
        self._repo.shift_range(start, end, from_today=from_today)
        self._repo.commit()

    def view_all(self) -> dict[int, list[Card]]:
        return {
            level: self._repo.get_all_on_level(level)
            for level in range(self._config.levels)
        }

    def remove(self, name: str) -> int:
        count = self._repo.delete_by_name(name)
        self._repo.commit()
        return count

    def freeze(self) -> date:
        today = date.today()
        self._repo.set_meta("freeze_date", today.isoformat())
        self._repo.commit()
        return today

    def unfreeze(self) -> int | None:
        """Unfreeze and shift all cards. Returns days passed, or None if not frozen."""
        raw = self._repo.get_meta("freeze_date")
        if not raw:
            return None
        freeze_date = date.fromisoformat(raw)
        self._repo.delete_meta("freeze_date")
        days_passed = (date.today() - freeze_date).days
        self._repo.calendar_shift(days_passed)
        self._repo.commit()
        return days_passed

    def close(self) -> None:
        self._repo.close()
