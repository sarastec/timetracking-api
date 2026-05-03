from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.models import TimeEntry, Activity
from app.api.time_entries.schemas import TimerAction


router = APIRouter(prefix="/time-entries", tags=["time-entries"])


@router.post("/start", status_code=200)
def start_timer(
    time_entry: TimerAction,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check if activity id exists and belongs to the user
    activity = db.query(Activity).filter(
        Activity.id == time_entry.activity_id,
        Activity.user_id == current_user.id
    ).first()

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if previous entry for this activity already ended
    active_entry = db.query(TimeEntry).filter(
        TimeEntry.activity_id == time_entry.activity_id,
        TimeEntry.end.is_(None)
    ).first()

    if active_entry:
        raise HTTPException(
            status_code=400,
            detail="Timer already running for this activity"
        )
    
    # Create new entry
    new_time_entry = TimeEntry(
        activity_id = time_entry.activity_id,
        start = time_entry.time,
        end = None
    )

    db.add(new_time_entry)
    db.commit()
    db.refresh(new_time_entry)

    return {
        "id": new_time_entry.id,
        "activity_id": new_time_entry.activity_id,
        "start": new_time_entry.start,
        "end": new_time_entry.end
    }


@router.post("/end", status_code=200)
def end_timer(
    time_entry: TimerAction,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check if activity id exists and belongs to the user
    activity = db.query(Activity).filter(
        Activity.id == time_entry.activity_id,
        Activity.user_id == current_user.id
    ).first()

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if there is a started entry for this activity
    active_entry = db.query(TimeEntry).filter(
        TimeEntry.activity_id == time_entry.activity_id,
        TimeEntry.end.is_(None)
    ).first()

    if not active_entry:
        raise HTTPException(
            status_code=400,
            detail="No running timer found for this activity"
        )
    
    # End time entry
    active_entry.end = time_entry.time

    db.commit()
    db.refresh(active_entry)

    return {
        "id": active_entry.id,
        "activity_id": active_entry.activity_id,
        "start": active_entry.start,
        "end": active_entry.end
    }


@router.get("", status_code=200)
def get_all_time_entries(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    entries = (
        db.query(TimeEntry)
        .join(Activity, TimeEntry.activity_id == Activity.id)
        .filter(Activity.user_id == current_user.id)
        .all()
    )

    return [
        {
            "id": e.id,
            "activity_id": e.activity_id,
            "start": e.start,
            "end": e.end
        }
        for e in entries
    ]
