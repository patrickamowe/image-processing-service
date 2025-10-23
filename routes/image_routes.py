import uuid
from io import BytesIO
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.models import Image
from schemas.image_schema import ImageResponse, ImageList, ImageUpdate
from pathlib import Path
from utils.auth_utils import get_current_user
from db.database import get_db
from schemas.user_schema import GetUser
from PIL import Image as PILImage, UnidentifiedImageError
from utils.image_utils import transform_image, delete_image_duplicate
import os

router = APIRouter(prefix="/images", tags=["Images"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True) #create the directory if it does not exist

@router.post("/", response_model=ImageResponse)
async def upload_image_file(
        file: UploadFile = File(),
        db: Session = Depends(get_db),
        authenticated_user: GetUser = Depends(get_current_user)
):
    """Upload an image file, validate it, save it, and store its metadata in the database."""

    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only image files are allowed."
        )

    file_content_bytes = await file.read()

    # Validate image integrity using Pillow
    try:
        pillow_image = PILImage.open(BytesIO(file_content_bytes))
        pillow_image.verify()
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not a valid image."
        )

    # Reopen the image (verify() closes the file internally)
    pillow_image = PILImage.open(BytesIO(file_content_bytes))
    image_width, image_height = pillow_image.size

    # Generate a unique file name and determine save path
    extension = file.filename.split(".")[-1].lower()
    unique_image_name = f"{uuid.uuid4()}.{extension}"
    saved_image_path = UPLOAD_DIR / unique_image_name

    # Save image to uploads directory
    with open(saved_image_path, "wb") as image_buffer:
        image_buffer.write(file_content_bytes)

    # Build metadata dictionary
    image_metadata = {
        "image_name": unique_image_name,
        "image_format": file.content_type,
        "extension": extension,
        "image_size_kb": round(len(file_content_bytes) / 1024, 2),
        "width": image_width,
        "height": image_height
    }

    # Create and save database record
    new_image_record = Image(
        url=str(saved_image_path),
        user_id=authenticated_user.user_id,
        meta_data=image_metadata
    )
    db.add(new_image_record)
    db.commit()
    db.refresh(new_image_record)

    return new_image_record


@router.get("/{image_id}", response_model=ImageResponse)
async def get_image_by_id(image_id: int, db: Session = Depends(get_db)):
    """Retrieve a single image record from the database by its unique ID."""

    image_record = db.query(Image).filter(Image.id == image_id).first()
    if not image_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found."
        )

    return image_record


@router.get("/", response_model=ImageList)
async def list_uploaded_images(
        page_no: int = 1,
        page_limit: int = 10,
        db: Session = Depends(get_db)
):
    """Retrieve a paginated list of uploaded images with their metadata."""

    offset_value = (page_no - 1) * page_limit
    image_records = db.query(Image).offset(offset_value).limit(page_limit).all()

    image_response_list = [
        {
            "id": image_record.id,
            "url": image_record.url,
            "meta_data": image_record.meta_data,
            "created_at": image_record.created_at
        }
        for image_record in image_records
    ]

    return {"images": image_response_list}


@router.post("/{image_id}/transform", response_model=ImageResponse)
async def apply_image_transformations(
        image_id: int,
        transformations: dict[str, dict | str | int | bool],
        db: Session = Depends(get_db),
        authenticated_user: GetUser = Depends(get_current_user)
):
    """Apply a series of transformations to an image and update its metadata."""

    project_root_dir = Path(__file__).resolve().parent.parent

    # Retrieve image record from the database
    image_record = db.query(Image).filter(Image.id == image_id).first()
    if not image_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found."
        )

    # Only the uploader can modify their own image
    if image_record.user_id != authenticated_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to modify this image."
        )

    original_image_url = image_record.url
    original_image_path = project_root_dir / original_image_url

    # Open and transform the image
    original_pillow_image = PILImage.open(original_image_path)
    original_image_format = original_pillow_image.format
    transformed_pillow_image, compress = transform_image(original_pillow_image, transformations)

    # Determine new file extension and save the transformed image
    image_format = transformed_pillow_image.format
    new_file_extension = image_format.lower() if image_format is not None else original_image_format.lower()
    transformed_image_path = original_image_path.with_suffix(f".{new_file_extension}")

    if compress:
        transformed_pillow_image.save(transformed_image_path, format=image_format, quality=50, optimize=True)
    else:
        transformed_pillow_image.save(transformed_image_path, format=image_format)

    # Delete duplicate if format changed
    delete_image_duplicate(str(original_image_path), str(transformed_image_path))

    # Collect updated metadata
    image_width, image_height = transformed_pillow_image.size
    updated_file_url = str(Path(original_image_url).with_suffix(f".{new_file_extension}"))
    updated_file_size_kb = round(os.path.getsize(transformed_image_path) / 1024, 2)

    updated_meta_data = {
        "image_name": Path(image_record.meta_data.get("image_name")).stem + f".{new_file_extension}",
        "image_format": f"image/{new_file_extension}",
        "extension": new_file_extension,
        "image_size_kb": updated_file_size_kb,
        "width": image_width,
        "height": image_height,
    }

    # Update record in the database
    updated_image_record = ImageUpdate(url=updated_file_url, meta_data=updated_meta_data)
    record_data_to_update = updated_image_record.model_dump(exclude_unset=True)

    for attribute, new_value in record_data_to_update.items():
        setattr(image_record, attribute, new_value)

    db.commit()
    db.refresh(image_record)

    return image_record

