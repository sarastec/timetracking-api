from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from app.db import Base


class UserStatus(Base):
    __tablename__ = "user_status_lookup"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class Subscription(Base):
    __tablename__ = "subscriptions_lookup"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    status_id = Column(Integer, ForeignKey("user_status_lookup.id"), index=True, nullable=False, default=1)
    subscription_id = Column(Integer, ForeignKey("subscriptions_lookup.id"), nullable=False, default=1)
    created_dt = Column(DateTime, nullable=False)
    modified_dt = Column(DateTime, nullable=True)


class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("folders.id"), index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    created_dt = Column(DateTime, nullable=False)
    modified_dt = Column(DateTime, nullable=True)


class ActivityStatus(Base):
    __tablename__ = "activity_status_lookup"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    status_id = Column(Integer, ForeignKey("activity_status_lookup.id"), index=True, nullable=False, default=1)
    created_dt = Column(DateTime, nullable=False)
    modified_dt = Column(DateTime, nullable=True)


class TimeEntry(Base):
    __tablename__ = "time_entries"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), index=True, nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=True)
