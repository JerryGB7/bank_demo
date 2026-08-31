from sqlalchemy.orm import DeclarativeBase

# This is the shared declarative base for all SQLAlchemy models in the app.
# It gives SQLAlchemy a common parent class for model definitions, which is
# required so mapped classes can register their metadata and table mappings.
# Using one base class keeps the ORM setup consistent and makes it easier for
# tools like Alembic to discover all models in the application.
class Base(DeclarativeBase):
    pass