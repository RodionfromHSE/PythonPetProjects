import sqlite3
from datetime import date, timedelta

from src.models import Card, LeitnerConfig


def _daterange(start: date, end: date):
    for n in range((end - start).days):
        yield start + timedelta(n)


class CardRepository:
    def __init__(self, db_path: str, config: LeitnerConfig):
        self._config = config
        self._con = sqlite3.connect(db_path, check_same_thread=False)
        self._cur = self._con.cursor()
        self._ensure_tables()

    def _ensure_tables(self):
        for i in range(self._config.levels):
            self._cur.execute(
                f"CREATE TABLE IF NOT EXISTS level{i} "
                "(objName TEXT, link TEXT, date TEXT)"
            )
        self._cur.execute(
            "CREATE TABLE IF NOT EXISTS metadata "
            "(key TEXT PRIMARY KEY, value TEXT)"
        )
        self._con.commit()

    def add(self, card: Card, level: int) -> None:
        self._cur.execute(
            f"INSERT INTO level{level} VALUES (?, ?, ?)",
            (card.name, card.link, str(card.rep_date)),
        )

    def get_by_date(self, target: date, level: int | None = None) -> list[Card]:
        levels = [level] if level is not None else range(self._config.levels)
        cards: list[Card] = []
        for lvl in levels:
            self._cur.execute(
                f"SELECT * FROM level{lvl} WHERE date = ?", (str(target),)
            )
            cards.extend(Card.from_row(row) for row in self._cur.fetchall())
        return cards

    def extract_by_date(self, target: date, level: int) -> list[Card]:
        """Get and delete all cards for a date on a level."""
        cards = self.get_by_date(target, level)
        self._cur.execute(
            f"DELETE FROM level{level} WHERE date = ?", (str(target),)
        )
        return cards

    def delete_by_name(self, name: str) -> int:
        """Delete cards matching name (case-insensitive) across all levels."""
        total = 0
        for i in range(self._config.levels):
            self._cur.execute(
                f"SELECT COUNT(*) FROM level{i} "
                "WHERE objName = ? COLLATE NOCASE",
                (name,),
            )
            count = self._cur.fetchone()[0]
            if count:
                self._cur.execute(
                    f"DELETE FROM level{i} WHERE objName = ? COLLATE NOCASE",
                    (name,),
                )
                total += count
        return total

    def get_all_on_level(self, level: int) -> list[Card]:
        self._cur.execute(f"SELECT * FROM level{level}")
        return [Card.from_row(row) for row in self._cur.fetchall()]

    def extract_all_on_level(self, level: int) -> list[Card]:
        cards = self.get_all_on_level(level)
        self._cur.execute(f"DELETE FROM level{level}")
        return cards

    def shift_cards(self, day: date, from_today: bool = False) -> None:
        for level in range(self._config.levels):
            cards = self.extract_by_date(day, level)
            if level == self._config.levels - 1:
                break  # last-level cards graduate
            for card in cards:
                card.shift_date(self._config.shifts[level], from_today)
                self.add(card, level + 1)

    def shift_range(self, start: date, end: date, from_today: bool = False) -> None:
        for day in _daterange(start, end):
            self.shift_cards(day, from_today)

    def calendar_shift(self, days: int) -> None:
        """Shift every card's date forward by `days` (used by unfreeze)."""
        for level in range(self._config.levels):
            cards = self.extract_all_on_level(level)
            for card in cards:
                card.shift_date(days)
                self.add(card, level)

    def get_meta(self, key: str) -> str | None:
        self._cur.execute("SELECT value FROM metadata WHERE key = ?", (key,))
        row = self._cur.fetchone()
        return row[0] if row else None

    def set_meta(self, key: str, value: str) -> None:
        self._cur.execute(
            "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
            (key, value),
        )

    def delete_meta(self, key: str) -> None:
        self._cur.execute("DELETE FROM metadata WHERE key = ?", (key,))

    def commit(self) -> None:
        self._con.commit()

    def close(self) -> None:
        self.commit()
        self._cur.close()
        self._con.close()
