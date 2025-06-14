from pathlib import Path
from dotenv import load_dotenv


def load_env() -> None:
    """Load environment variables from a local .env file if it exists."""
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
