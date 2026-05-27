
import shutil
import uuid
from pathlib import Path

from PIL import Image

from .paths import APP_DIR, PRODUCTS_PHOTO_DIR

MAX_SIZE = (300, 200)

def import_product_photo(source_path: str) -> str:
    src = Path(source_path)
    if not src.exists():
        raise FileNotFoundError(source_path)
    PRODUCTS_PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower() or ".jpg"
    name = f"{uuid.uuid4().hex}{ext}"
    dest = PRODUCTS_PHOTO_DIR / name
    with Image.open(src) as img:
        img.thumbnail(MAX_SIZE)
        if img.mode in ("RGBA", "P") and ext in (".jpg", ".jpeg"):
            img = img.convert("RGB")
        img.save(dest)
    return str(dest.relative_to(APP_DIR))

def remove_product_photo(relative_path):
    if not relative_path:
        return
    abs_path = (APP_DIR / relative_path).resolve()
    if not abs_path.exists():
        return
    if PRODUCTS_PHOTO_DIR.resolve() not in abs_path.parents:
        return
    try:
        abs_path.unlink()
    except OSError:
        pass
