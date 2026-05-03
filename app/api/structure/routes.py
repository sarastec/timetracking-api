from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.models import Activity, Folder
from app.api.structure.schemas import Node


router = APIRouter(prefix="/structure", tags=["structure"])


@router.get("", response_model=list[Node])
def get_structure(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Fetch all folders and activities belonging to the user
    folders = db.query(Folder).filter(Folder.user_id == current_user.id).all()
    activities = db.query(Activity).filter(Activity.user_id == current_user.id).all()

    # Folders' children
    children_map = {f.id: [] for f in folders}

    for f in folders:
        if f.parent_id:
            children_map[f.parent_id].append(f)

    # Activities maps
    activity_map = {f.id: [] for f in folders}
    root_activities = []

    for a in activities:
        if a.folder_id:
            activity_map[a.folder_id].append(a)
        else:
            root_activities.append(a)

    # Build folders structures
    def build_folder(folder):
        return Node(
            id=folder.id,
            name=folder.name,
            type="folder",
            parent_id=folder.parent_id,
            children=[
                *[build_folder(child) for child in children_map.get(folder.id, [])],
                *[
                    Node(
                        id=a.id,
                        name=a.name,
                        type="activity",
                        parent_id=folder.id,
                        children=[]
                    )
                    for a in activity_map.get(folder.id, [])
                ]
            ]
        )

    root_folders = [f for f in folders if f.parent_id is None]

    # Return all root activities and root folders with their children
    return [
        *[build_folder(f) for f in root_folders],
        *[
            Node(
                id=a.id,
                name=a.name,
                type="activity",
                parent_id=None,
                children=[]
            )
            for a in root_activities
        ]
    ]
