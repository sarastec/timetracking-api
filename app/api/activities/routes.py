from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.deps import get_db, get_current_user
from app.models import Activity, Folder
from app.api.activities.schemas import ActivityEdit


router = APIRouter(prefix="/activities", tags=["activities"])


@router.post("", status_code=201)
def create_activity(
    activity: ActivityEdit,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if activity.folder_id != None:
        db_parent_folder = db.query(Folder).filter(
            Folder.id == activity.folder_id,
            Folder.user_id == current_user.id
        ).first()

        if db_parent_folder == None:
            raise HTTPException(status_code=400, detail="Incorrect parent folder id")
        
    new_activity = Activity(
        name=activity.name,
        folder_id=activity.folder_id,
        user_id=current_user.id,
        created_dt=datetime.now(timezone.utc)
    )

    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)

    return {
        "id": new_activity.id,
        "name": new_activity.name,
        "folder_id": new_activity.folder_id
    }


@router.put("/{activity_id}", status_code=200)
def update_activity(
    activity_id: int,
    activity: ActivityEdit,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.user_id == current_user.id
    ).first()

    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    if activity.folder_id != None:
        db_parent_folder = db.query(Folder).filter(
            Folder.id == activity.folder_id,
            Folder.user_id == current_user.id
        ).first()

        if db_parent_folder == None:
            raise HTTPException(status_code=400, detail="Incorrect parent folder id")

    db_activity.name = activity.name
    db_activity.folder_id = activity.folder_id
    db_activity.modified_dt=datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_activity)

    return {
        "id": db_activity.id,
        "name": db_activity.name,
        "folder_id": db_activity.folder_id
    }


@router.delete("/{activity_id}", status_code=204)
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.user_id == current_user.id
    ).first()

    if not db_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    if db_activity.status_id == 2:
        raise HTTPException(status_code=400, detail="Activity already deleted")

    db_activity.status_id = 2
    db_activity.modified_dt=datetime.now(timezone.utc)

    db.commit()

    return
