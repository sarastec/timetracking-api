from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.deps import get_db, get_current_user
from app.models import Folder
from app.api.folders.schemas import FolderEdit


router = APIRouter(prefix="/folders", tags=["folders"])


@router.post("", status_code=201)
def create_folder(
    folder: FolderEdit,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_folder = Folder(
        name=folder.name,
        parent_id=folder.parent_id,
        user_id=current_user.id,
        created_dt=datetime.now(timezone.utc)
    )

    db.add(new_folder)
    db.commit()
    db.refresh(new_folder)

    return {
        "id": new_folder.id,
        "name": new_folder.name,
        "parent_id": new_folder.parent_id
    }


@router.put("/{folder_id}", status_code=200)
def update_folder(
    folder_id: int,
    folder: FolderEdit,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_folder = db.query(Folder).filter(
        Folder.id == folder_id,
        Folder.user_id == current_user.id
    ).first()

    if not db_folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    db_folder.name = folder.name
    db_folder.parent_id = folder.parent_id
    db_folder.modified_dt=datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_folder)

    return {
        "id": db_folder.id,
        "name": db_folder.name,
        "parent_id": db_folder.parent_id
    }


@router.delete("/{folder_id}", status_code=204)
def delete_folder(
    folder_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_folder = db.query(Folder).filter(
        Folder.id == folder_id,
        Folder.user_id == current_user.id
    ).first()

    if not db_folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    db.delete(db_folder)
    db.commit()

    return
