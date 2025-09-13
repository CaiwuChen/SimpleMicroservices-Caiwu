from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, StringConstraints

UNIType = Annotated[str, StringConstraints(pattern=r"^[A-Z]{4}\d{4}$")]

class CourseBase(BaseModel):
    
    coursenumber: UNIType = Field(
        ...,
        description="Columbia University Course ID (4 Uppercase letters + 4 digits).",
        json_schema_extra={"example": "COMS4153"},
    )
    instructor: str = Field(
        ...,
        description="The person who teach this course ",
        json_schema_extra={"example": "Donald F Ferguson"},
    )
    time: str = Field(
        ...,
        description="The time and data to take this course",
        json_schema_extra={"example": "F 1:10pm-3:40pm"},
    )
    location: str = Field(
        ...,
        description="Room or where to take the course.",
        json_schema_extra={"example": "501 Northwest Corner Building"},
    )
    capacity: int = Field(
        ...,
        description="The maximum number student of this course will involve",
        json_schema_extra={"example": "160"},
    )
    enrollment: int = Field(
        ...,
        description="the current number of student enroll into this course.",
        json_schema_extra={"example": "143"},
    )
   

class CourseCreate(CourseBase):
    """Creation payload for a Course."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "coursenumber": "COMS4153",
                    "instructor": "Donald F Ferguson",
                    "time": "F 1:10pm-3:40pm",
                    "location": "501 Northwest Corner Building",
                    "capacity": "160",
                    "enrollment": "143",
                }
            ]
        }
    }


class CourseUpdate(BaseModel):
    """Partial update for a Course; supply only fields to change."""
    
    coursenumber: Optional[UNIType ] = Field(None, json_schema_extra={"example": "ELEN4153"})
    instructor: Optional[str] = Field(None, json_schema_extra={"example": "Joseph"})
    time: Optional[str] = Field(None, json_schema_extra={"example": "TR 1:10pm-2:25pm"})
    location: Optional[str] = Field(None, json_schema_extra={"example": "309 Havemeyer Hall"})
    capacity: Optional[int] = Field(None, json_schema_extra={"example": "200"})
    enrollment: Optional[int] = Field(None, json_schema_extra={"example": "10"})
    

    model_config = {
        "examples": [
                {"coursenumber": "ELEN4153"},
                {"instructor": "Joseph"},
                {"time": "TR 1:10pm-2:25pm", "location": "309 Havemeyer Hall"},
                {"enrollment": 10, "capacity": 200},
            ]
    }


class CourseRead(CourseBase):
    """Server representation of a Course returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Course ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "99999999-9999-4999-8999-999999999999",
                    "coursenumber": "ELEN4153",
                    "instructor": "Joseph",
                    "time": "TR 1:10pm-2:25pm",
                    "location": "309 Havemeyer Hall",
                    "capacity": 200,
                    "enrollment": 10,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
