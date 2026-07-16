from pathlib import Path


BACKEND_APP_DIR = Path(__file__).resolve().parents[1] / "backend" / "app"
__path__ = [str(BACKEND_APP_DIR)]
