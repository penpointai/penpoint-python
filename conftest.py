from pathlib import Path


def pytest_configure(config):
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        from dotenv import load_dotenv

        load_dotenv(env_path)
