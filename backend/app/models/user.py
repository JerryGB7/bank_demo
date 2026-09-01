from __future__ import annotations

from sqlalchemy import Boolean, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .enums import Technician_RBAC

# This model describes the "users" table in the database.
# SQLAlchemy uses Python classes to map to database tables, and each attribute
# below represents a column in that table.
# This is important because it gives the application a structured way to query,
# insert, update, and delete user records while keeping the database schema in sync
# with the code.
class User(Base):
    # The table name is explicitly set so SQLAlchemy creates/uses a database table
    # called "users" rather than deriving one from the class name.
    __tablename__ = "users"

    # Primary key for each user record. Every table row must have a unique id.
    # This is how the application can reliably look up a specific user.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Username column: a short string used as a unique login identifier.
    # "unique=True" ensures no two users can share the same username, and
    # "index=True" speeds up searches by username.
    # A fixed max length of 50 prevents overly large values and keeps the schema
    # consistent and efficient.
    username: Mapped[String] = mapped_column(String(50), unique=True, index=True)

    # Store a hashed password instead of a raw password.
    # This is critical for security: if the database is ever exposed, attackers do
    # not immediately get usable login credentials.
    # A hashed value is one-way, so the application must verify passwords by
    # hashing the submitted password and comparing it to this stored hash.
    password_hash: Mapped[str] = mapped_column(String(255))

    # Role is stored as a database enum backed by the Technician_RBAC Python Enum.
    # This is important because it restricts values to a known set of roles, making
    # the authorization model predictable and enforceable.
    # The enum name is explicitly set to "technician-rbac" so the database can
    # store it as a named enum type when supported by the database backend.
    # values_callable ensures the underlying database receives the enum values
    # (for example, "admin", "technician") rather than Python enum names.
    role: Mapped[Technician_RBAC] = mapped_column(
        SQLEnum(
            Technician_RBAC,
            name="technician-rbac",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        )
    )

    # Indicates whether the user account is active.
    # This is a common application flag used to disable accounts without deleting
    # them, which is useful for administrative control, security, and auditing.
    # A default value of True means new users are active unless the application
    # explicitly turns them off.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # __repr__ is helpful for debugging and logging.
    # It gives a readable summary of the object without dumping every field.
    # This is valuable during development and testing when inspecting ORM objects
    # in the console or application logs.
    def __repr__(self):
        return f"User: {self.username}, id={self.id}, role={self.role.value}"

