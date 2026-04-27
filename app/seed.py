from app.db import SessionLocal
from app.models import UserStatus, Subscription, ActivityStatus


# Make sure lookup tables are populated on startup
def seed_lookup_tables():
    db = SessionLocal()

    try:
        # USER STATUS
        if db.query(UserStatus).count() == 0:
            db.add_all([
                UserStatus(id=1, name="active"),
                UserStatus(id=2, name="deleted")
            ])

        # SUBSCRIPTIONS
        if db.query(Subscription).count() == 0:
            db.add_all([
                Subscription(id=1, name="free"),
                Subscription(id=2, name="premium")
            ])

        # ACTIVITY STATUS
        if db.query(ActivityStatus).count() == 0:
            db.add_all([
                ActivityStatus(id=1, name="active"),
                ActivityStatus(id=2, name="deleted")
            ])

        db.commit()

    finally:
        db.close()
        