import os
import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.models import Card
from src.service import LeitnerService


class StudyBotRepl:
    def __init__(self, service: LeitnerService, history_path: str):
        self._svc = service
        self._console = Console()
        self._commands: dict[str, tuple[str, callable]] = {
            "addPlus": ("Add items (yesterday date appended)", self._add_plus),
            "add": ("Add items [optional date: dd.mm]", self._add),
            "get": ("Today's cards [optional: dd.mm]", self._get),
            "getAll": ("Unrepeated cards (last 31 days)", self._get_all),
            "makeShifts": ("Shift today's cards", self._make_shifts),
            "makeShiftsFrom": ("Shift from a date (dd.mm)", self._make_shifts_from),
            "makeShiftsAll": ("Shift all unrepeated", self._make_shifts_all),
            "makeShiftsAllFromToday": ("Shift all as if today", self._make_shifts_all_today),
            "view": ("View all levels", self._view),
            "remove": ("Remove by name", self._remove),
            "postpone": ("Postpone a card by N days (same level)", self._postpone),
            "freeze": ("Freeze scheduling", self._freeze),
            "unfreeze": ("Resume scheduling", self._unfreeze),
            "help": ("Show this help", self._help),
            "close": ("Exit", self._close),
        }
        self._session = PromptSession(
            completer=WordCompleter(sorted(self._commands), sentence=True),
            history=FileHistory(history_path),
        )

    def run(self) -> None:
        self._console.print(
            Panel("[bold]Leitner Study Bot[/bold] — type [bold]help[/bold] for commands")
        )
        while True:
            try:
                text = self._session.prompt("leitner> ").strip()
                if not text:
                    continue
                self._dispatch(text)
            except (EOFError, KeyboardInterrupt):
                self._close()

    def _dispatch(self, text: str) -> None:
        parts = text.split(": ", maxsplit=1)
        command = parts[0]
        args_str = parts[1] if len(parts) > 1 else None

        entry = self._commands.get(command)
        if not entry:
            self._error(f"Unknown command: {command}")
            return
        try:
            entry[1](args_str)
        except Exception as e:
            self._error(str(e))

    # ---- output helpers ----

    def _success(self, msg: str) -> None:
        self._console.print(Panel(msg, style="green"))

    def _error(self, msg: str) -> None:
        self._console.print(Panel(msg, style="red"))

    def _print_cards(self, cards: list[Card], empty_msg: str = "No cards found.") -> None:
        if not cards:
            self._console.print(f"[dim]{empty_msg}[/dim]")
            return
        for card in sorted(cards, key=lambda c: str(c.rep_date), reverse=True):
            self._console.print(f"  {card}")

    # ---- command handlers ----

    def _add_plus(self, args: str | None) -> None:
        if not args:
            self._error("Usage: addPlus: item1 + item2 + ...")
            return
        cards = self._svc.add_items(args, reformat=True)
        self._success(f"Added {len(cards)} card(s)")
        for c in cards:
            self._console.print(f"  {c}")

    def _add(self, args: str | None) -> None:
        if not args:
            self._error("Usage: add: item1 + item2[: dd.mm]")
            return
        parts = args.split(": ", maxsplit=1)
        raw = parts[0]
        date_str = parts[1].strip() if len(parts) > 1 else None
        cards = self._svc.add_items(raw, date_str=date_str)
        self._success(f"Added {len(cards)} card(s)")
        for c in cards:
            self._console.print(f"  {c}")

    def _get(self, args: str | None) -> None:
        if args:
            cards = self._svc.get_by_date(args)
            self._print_cards(cards, "No cards for that date.")
        else:
            cards = self._svc.get_today()
            self._print_cards(cards, "Nothing to repeat today!")

    def _get_all(self, _args: str | None) -> None:
        cards = self._svc.get_not_repeated()
        self._print_cards(cards, "Nothing unrepeated in the last 31 days!")

    def _make_shifts(self, _args: str | None) -> None:
        self._svc.shift_today()
        self._success("Shifts done!")

    def _make_shifts_from(self, args: str | None) -> None:
        if not args:
            self._error("Usage: makeShiftsFrom: dd.mm")
            return
        self._svc.shift_from(args)
        self._success("Shifts done!")

    def _make_shifts_all(self, _args: str | None) -> None:
        self._svc.shift_all()
        self._success("All unrepeated shifted!")

    def _make_shifts_all_today(self, _args: str | None) -> None:
        self._svc.shift_all(from_today=True)
        self._success("All shifted from today!")

    def _view(self, _args: str | None) -> None:
        levels = self._svc.view_all()
        table = Table(title="Leitner Levels", show_lines=True)
        table.add_column("Level", style="bold cyan", justify="center")
        table.add_column("Cards", min_width=40)
        for level, cards in levels.items():
            card_names = ", ".join(c.name for c in cards) if cards else "[dim]empty[/dim]"
            table.add_row(str(level + 1), card_names)
        self._console.print(table)

    def _remove(self, args: str | None) -> None:
        if not args:
            self._error("Usage: remove: name")
            return
        count = self._svc.remove(args.strip())
        if count:
            self._success(f"Removed {count} card(s) named '{args.strip()}'")
        else:
            self._error(f"No cards found with name '{args.strip()}'")

    def _postpone(self, args: str | None) -> None:
        usage = "Usage: postpone: <name>, <days>"
        if not args or "," not in args:
            self._error(usage)
            return
        name, days_str = (p.strip() for p in args.rsplit(",", maxsplit=1))
        if not name:
            self._error(usage)
            return
        days = int(days_str)
        count = self._svc.postpone(name, days)
        if count:
            self._success(f"Postponed {count} card(s) by {days} day(s)")
        else:
            self._error(f"No cards found: '{name}'")

    def _freeze(self, _args: str | None) -> None:
        d = self._svc.freeze()
        self._success(f"Frozen on {d}")

    def _unfreeze(self, _args: str | None) -> None:
        days = self._svc.unfreeze()
        if days is None:
            self._error("Not frozen.")
            return
        self._success(f"Unfrozen! {days} day(s) passed.")

    def _help(self, _args: str | None) -> None:
        table = Table(title="Commands")
        table.add_column("Command", style="bold")
        table.add_column("Description")
        for name, (desc, _) in self._commands.items():
            table.add_row(name, desc)
        self._console.print(table)

    def _close(self, _args: str | None = None) -> None:
        self._svc.close()
        self._console.print("[bold]Have a nice day![/bold]")
        sys.exit(0)
