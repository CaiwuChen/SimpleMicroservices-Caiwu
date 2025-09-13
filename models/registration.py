from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


# --------------------------
# Registration Base
# --------------------------
class RegistrationBase(BaseModel):
    """Shared fields for a Registration."""

    person_id: UUID = Field(
        ...,
        description="The unique ID of the registered person.",
        json_schema_extra={"example": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"},
    )
    course_id: UUID = Field(
        ...,
        description="The unique ID of the course.",
        json_schema_extra={"example": "0e8ec51e-c5df-4e8f-a254-4fcfab5754c9"},
    )


# --------------------------
# Registration Create
# --------------------------
class RegistrationCreate(RegistrationBase):
    """Creation payload for a Registration."""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "person_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
                    "course_id": "0e8ec51e-c5df-4e8f-a254-4fcfab5754c9",
                }
            ]
        }
    }


# --------------------------
# Registration Update
# --------------------------
class RegistrationUpdate(BaseModel):
    """Partial update for a Registration; supply only fields to change."""

    status: Optional[str] = Field(
        None,
        description="Update the registration status.",
        json_schema_extra={"example": "dropped"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"status": "dropped"},
                {"status": "waitlisted"},
            ]
        }
    }


# --------------------------
# Registration Read
# --------------------------
class RegistrationRead(RegistrationBase):
    """Server representation of a Registration returned to clients."""

    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Registration ID.",
        json_schema_extra={"example": "33333333-3333-4333-8333-333333333333"},
    )
    status: str = Field(
        ...,
        description="Registration status (e.g., enrolled, waitlisted, dropped).",
        json_schema_extra={"example": "enrolled"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the registration was created (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the registration was last updated (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "33333333-3333-4333-8333-333333333333",
                    "person_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
                    "course_id": "0e8ec51e-c5df-4e8f-a254-4fcfab5754c9",
                    "status": "enrolled",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
