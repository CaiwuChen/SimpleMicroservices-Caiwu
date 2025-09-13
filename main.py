from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.health import Health
from models.course import CourseCreate, CourseRead, CourseUpdate
from models.registration import RegistrationCreate, RegistrationRead, RegistrationUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
courses: Dict[UUID,CourseRead] = {}
registrations: Dict[UUID,RegistrationRead] = {}
app = FastAPI(
    title="Person/Address API",
    description="Demo FastAPI app using Pydantic v2 models for Person and Address",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]

@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(addresses.values())

    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]

    return results

@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]

@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]

# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------
@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    # Each person gets its own UUID; stored as PersonRead
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read

@app.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    results = list(persons.values())

    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]

    # nested address filtering
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]

    return results

@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]

@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]

# -----------------------------------------------------------------------------
# Course endpoints
# -----------------------------------------------------------------------------
@app.post("/courses", response_model=CourseRead, status_code=201)
def create_course(course: CourseCreate):
    # Each person gets its own UUID; stored as PersonRead
    course_read = CourseRead(**course.model_dump())
    courses[course_read.id] = course_read
    return course_read

@app.get("/courses", response_model=List[CourseRead])
def list_courses(
    coursenumber: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    instructor: Optional[str] = Query(None, description="Filter by first name"),
    time: Optional[str] = Query(None, description="Filter by last name"),
    location: Optional[str] = Query(None, description="Filter by email"),
    capacity: Optional[int] = Query(None, description="Filter by phone number"),
    enrollment: Optional[int] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
):
    results = list(courses.values())

    if coursenumber is not None:
        results = [p for p in results if p.coursenumber == coursenumber]
    if instructor is not None:
        results = [p for p in results if p.instructor == instructor]
    if time is not None:
        results = [p for p in results if p.time == time]
    if location is not None:
        results = [p for p in results if p.location == location]
    if capacity is not None:
        results = [p for p in results if p.capacity == capacity]
    if enrollment is not None:
        results = [p for p in results if str(p.enrollment) == enrollment]

    return results

@app.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]

@app.patch("/courses/{course_id}", response_model=CourseRead)
def update_course(course_id: UUID, update: CourseUpdate):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    stored = courses[course_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    stored["updated_at"] = datetime.utcnow()
    courses[course_id] = CourseRead(**stored)
    return courses[course_id]

# -----------------------------------------------------------------------------
# Registration Endpoint 
# -----------------------------------------------------------------------------
@app.post("/registrations", response_model=RegistrationRead, status_code=201)
def create_registration(reg: RegistrationCreate):
    # 1️⃣ Check that person exists
    if reg.person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    
    # 2️⃣ Check that course exists
    if reg.course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    
    course = courses[reg.course_id]
    
    # 3️⃣ Check enrollment vs capacity
    if course.enrollment < course.capacity:
        status = "enrolled"
        course.enrollment += 1  # increment current enrollment
    else:
        status = "waitlisted"
    
    # 4️⃣ Create RegistrationRead
    registration_read = RegistrationRead(
        **reg.model_dump(),
        status=status
    )
    
    # 5️⃣ Store it
    registrations[registration_read.id] = registration_read
    
    # 6️⃣ Update course record
    courses[course.id] = course
    
    return registration_read


@app.get("/registrations", response_model=List[RegistrationRead])
def list_registrations(
    person_id: Optional[UUID] = Query(None),
    course_id: Optional[UUID] = Query(None),
    status: Optional[str] = Query(None)
):
    results = list(registrations.values())
    
    if person_id is not None:
        results = [r for r in results if r.person_id == person_id]
    if course_id is not None:
        results = [r for r in results if r.course_id == course_id]
    if status is not None:
        results = [r for r in results if r.status == status]
    
    return results

def get_registration(registration_id: UUID):
    if registration_id not in registrations:
        raise HTTPException(status_code=404, detail="Registration not found")
    return registrations[registration_id]


def update_registration(registration_id: UUID, update: RegistrationUpdate):
    if registration_id not in registrations:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    stored = registrations[registration_id].model_dump()
    
    # 1️⃣ Update status
    stored.update(update.model_dump(exclude_unset=True))
    
    # 2️⃣ If status changed from enrolled -> dropped, decrement course enrollment
    registration = RegistrationRead(**stored)
    course = courses[registration.course_id]
    
    old_status = registrations[registration_id].status
    new_status = registration.status
    
    if old_status == "enrolled" and new_status == "dropped":
        course.enrollment -= 1
        
        # Optionally promote first waitlisted student
        waitlisted = next(
            (r for r in registrations.values() 
             if r.course_id == course.id and r.status == "waitlisted"),
            None
        )
        if waitlisted:
            waitlisted.status = "enrolled"
            course.enrollment += 1
            registrations[waitlisted.id] = waitlisted

    registrations[registration_id] = registration
    courses[course.id] = course
    return registration
# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
