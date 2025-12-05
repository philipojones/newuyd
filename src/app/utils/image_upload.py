"""Image upload utilities."""

import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return Path(filename).suffix.lower()


def is_allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return get_file_extension(filename) in ALLOWED_EXTENSIONS


async def validate_file_size(file: UploadFile) -> bool:
    """Validate file size."""
    file.file.seek(0, 2)  # Seek to end
    size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    return size <= MAX_FILE_SIZE


async def save_upload_file(upload_file: UploadFile, upload_dir: Path) -> str:
    """Save uploaded file and return the relative path."""
    if not upload_file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    if not is_allowed_file(upload_file.filename):
        raise HTTPException(
            status_code=400,
            detail=(
                f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            ),
        )

    if not await validate_file_size(upload_file):
        raise HTTPException(
            status_code=400,
            detail=(
                f"File too large. Maximum size is {MAX_FILE_SIZE // (1024 * 1024)}MB"
            ),
        )

    # Generate unique filename
    file_extension = get_file_extension(upload_file.filename)
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    # Ensure upload directory exists
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Save file
    file_path = upload_dir / unique_filename
    try:
        contents = await upload_file.read()
        with file_path.open("wb") as f:
            f.write(contents)

        # Return relative path from assets folder
        return f"assets/upload/{unique_filename}"
    except OSError as err:
        raise HTTPException(
            status_code=500, detail=f"Error saving file: {err!s}"
        ) from err
    finally:
        await upload_file.close()


def get_upload_directory() -> Path:
    """Get the upload directory path."""
    base_dir = Path(__file__).parent.parent.parent
    return base_dir / "assets" / "upload"


def delete_file(file_path: str) -> bool:
    """Delete a file from the upload directory."""
    try:
        upload_dir = get_upload_directory()
        full_path = upload_dir / Path(file_path).name
        if full_path.exists():
            full_path.unlink()
            return True
        return False
    except OSError:
        return False
