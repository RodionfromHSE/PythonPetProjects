import os

from boilerplate_tools import setup_root, load_config

setup_root(n_up=0)

from src.models import LeitnerConfig
from src.repository import CardRepository
from src.service import LeitnerService
from src.repl import StudyBotRepl

_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    conf = load_config(os.path.join(_DIR, "config.yaml"))
    leitner_config = LeitnerConfig()
    repo = CardRepository(conf.db.path, leitner_config)
    service = LeitnerService(repo, leitner_config)
    history_path = os.path.join(_DIR, ".leitner_history")
    repl = StudyBotRepl(service, history_path)
    repl.run()


if __name__ == "__main__":
    main()
