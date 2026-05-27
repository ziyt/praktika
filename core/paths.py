
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
DB_PATH = APP_DIR / "db" / "shoe_store.db"
RESOURCES_DIR = APP_DIR / "resources"
PRODUCTS_PHOTO_DIR = RESOURCES_DIR / "products"
PLACEHOLDER_IMAGE = RESOURCES_DIR / "picture.png"
LOGO_IMAGE = RESOURCES_DIR / "logo.png"
APP_ICON = RESOURCES_DIR / "icon.ico"

def resolve_photo(photo_path):
    if not photo_path:
        return PLACEHOLDER_IMAGE
    candidate = APP_DIR / photo_path
    if candidate.exists():
        return candidate
    return PLACEHOLDER_IMAGE
