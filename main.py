from typing import Optional, Annotated
from datetime import datetime, timezone
from pathlib import Path
import json
from collections import Counter

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Session, create_engine, Relationship, select, col
from sqlalchemy import or_

app = FastAPI(
    title="Applied Programming Course HS-Coburg",
    description="Note API with SQLite database, filters, tags and categories",
    version="3.0.0",
)


############################################
### Basic endpoints
############################################


@app.get("/")
def root():
    return {"message": "Hello, World"}


@app.get("/status")
def get_status():
    return {"status": "online", "version": "3.0.0", "day": 3}


@app.get("/about")
def get_about():
    return {
        "project": "Note API",
        "author": "Kulish Diana",
        "course": "Applied Programming",
    }


@app.get("/name/{name}")
def greet_name(name: str):
    return {"message": f"Hello, {name}!"}


@app.get("/square/{number}")
def calculate_square(number: int):
    result = number * number
    return {
        "number": number,
        "square": result,
        "calculation": f"{number} × {number} = {result}",
    }


@app.get("/student")
def get_student():
    return {
        "name": "Diana Kulish",
        "semester": 1,
        "course": "Wirtschaftsinformatik",
        "university": "HS Coburg",
    }


@app.get("/double/{number}")
def calculate_double(number: int):
    result = number * 2
    return {
        "number": number,
        "double": result,
        "calculation": f"{number} * 2 = {result}",
    }


@app.get("/even/{number}")
def check_even(number: int):
    if number % 2 == 0:
        result = "even"
    else:
        result = "odd"

    return {"number": number, "type": result}


############################################
### Path Parameters Practice
############################################


@app.get("/test/123")
def test_fixed_123():
    return {"message": "This is the fixed endpoint for 123"}


@app.get("/test/{value}")
def test_value(value: str):
    return {"value": value}


@app.get("/test/{value}/test2/{value2}")
def test_two_values(value: str, value2: str):
    return {"value": value, "value2": value2}


############################################
### Database models
############################################


class NoteTagLink(SQLModel, table=True):
    note_id: Optional[int] = Field(
        default=None,
        foreign_key="notes.id",
        primary_key=True,
    )
    tag_id: Optional[int] = Field(
        default=None,
        foreign_key="tags.id",
        primary_key=True,
    )


class Note(SQLModel, table=True):
    __tablename__ = "notes"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str = "general"
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    tags: list["Tag"] = Relationship(
        back_populates="notes",
        link_model=NoteTagLink,
    )


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

    notes: list[Note] = Relationship(
        back_populates="tags",
        link_model=NoteTagLink,
    )


############################################
### API models
############################################


class NoteCreate(BaseModel):
    title: str
    content: str
    category: str = "general"
    tags: list[str] = []


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[list[str]] = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: list[str]
    created_at: str

    class Config:
        from_attributes = True


############################################
### Database setup
############################################


DATABASE_URL = "sqlite:///notes.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def normalize_tag(tag_name: str) -> str:
    return tag_name.lower().strip()


def note_to_response(note: Note) -> NoteResponse:
    return NoteResponse(
        id=note.id,
        title=note.title,
        content=note.content,
        category=note.category,
        tags=sorted([tag.name for tag in note.tags]),
        created_at=note.created_at,
    )


def get_or_create_tags(tag_names: list[str], session: Session) -> list[Tag]:
    tag_objects = []
    seen_tags = set()

    for tag_name in tag_names:
        clean_tag = normalize_tag(tag_name)

        if not clean_tag:
            continue

        if clean_tag in seen_tags:
            continue

        seen_tags.add(clean_tag)

        statement = select(Tag).where(Tag.name == clean_tag)
        existing_tag = session.exec(statement).first()

        if existing_tag:
            tag_objects.append(existing_tag)
        else:
            new_tag = Tag(name=clean_tag)
            session.add(new_tag)
            session.commit()
            session.refresh(new_tag)
            tag_objects.append(new_tag)

    return tag_objects


def migrate_json_to_database():
    """
    Move existing data from data/notes.json into notes.db.
    Migration runs only if database is empty.
    """

    with Session(engine) as session:
        existing_notes = session.exec(select(Note)).first()

        if existing_notes:
            return

        json_file = Path("data/notes.json")

        if not json_file.exists():
            return

        with open(json_file, "r", encoding="utf-8") as file:
            old_notes = json.load(file)

        for old_note in old_notes:
            db_note = Note(
                id=old_note.get("id"),
                title=old_note.get("title"),
                content=old_note.get("content"),
                category=old_note.get("category", "general"),
                created_at=old_note.get(
                    "created_at",
                    datetime.now(timezone.utc).isoformat(),
                ),
            )

            old_tags = old_note.get("tags", [])
            db_note.tags = get_or_create_tags(old_tags, session)

            session.add(db_note)

        session.commit()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    migrate_json_to_database()


create_db_and_tables()


############################################
### Note API endpoints
############################################


@app.post("/notes", status_code=201)
def create_note(note: NoteCreate, session: SessionDep) -> NoteResponse:
    """Create a new note"""

    db_note = Note(
        title=note.title,
        content=note.content,
        category=note.category,
    )

    db_note.tags = get_or_create_tags(note.tags, session)

    session.add(db_note)
    session.commit()
    session.refresh(db_note)

    return note_to_response(db_note)


@app.get("/notes")
def list_notes(
    session: SessionDep,
    category: str = None,
    search: str = None,
    tag: str = None,
    created_after: str = None,
    created_before: str = None,
) -> list[NoteResponse]:
    """
    List notes with optional filters.

    Filters:
    - category
    - search
    - tag
    - created_after
    - created_before
    """

    statement = select(Note)

    if category:
        statement = statement.where(Note.category == category)

    if search:
        statement = statement.where(
            or_(
                col(Note.title).ilike(f"%{search}%"),
                col(Note.content).ilike(f"%{search}%"),
            )
        )

    if created_after:
        statement = statement.where(Note.created_at >= created_after)

    if created_before:
        statement = statement.where(Note.created_at <= created_before)

    if tag:
        tag_lower = normalize_tag(tag)

        statement = (
            statement.join(NoteTagLink, Note.id == NoteTagLink.note_id)
            .join(Tag, Tag.id == NoteTagLink.tag_id)
            .where(Tag.name == tag_lower)
        )

    notes = session.exec(statement).all()

    return [note_to_response(note) for note in notes]


@app.get("/notes/stats")
def get_note_stats(session: SessionDep):
    """
    Get statistics about notes.

    Returns:
    - Total notes
    - Notes per category
    - Most used tags top 5
    - Total number of unique tags
    """

    notes = session.exec(select(Note)).all()
    tags = session.exec(select(Tag)).all()

    category_counter = Counter()
    tag_counter = Counter()

    for note in notes:
        category_counter[note.category] += 1

        for tag in note.tags:
            tag_counter[tag.name] += 1

    top_tags = []

    for tag_name, count in tag_counter.most_common(5):
        top_tags.append(
            {
                "tag": tag_name,
                "count": count,
            }
        )

    return {
        "total_notes": len(notes),
        "by_category": dict(category_counter),
        "top_tags": top_tags,
        "unique_tags_count": len(tags),
    }


@app.get("/notes/{note_id}")
def get_note(note_id: int, session: SessionDep) -> NoteResponse:
    """Get a specific note by ID"""

    note = session.get(Note, note_id)

    if not note:
        raise HTTPException(
            status_code=404,
            detail=f"Note with ID {note_id} not found",
        )

    return note_to_response(note)


@app.put("/notes/{note_id}")
def update_note(
    note_id: int,
    note_update: NoteCreate,
    session: SessionDep,
) -> NoteResponse:
    """
    Fully update a note.

    PUT replaces the full resource.
    """

    note = session.get(Note, note_id)

    if not note:
        raise HTTPException(
            status_code=404,
            detail=f"Note with ID {note_id} not found",
        )

    note.title = note_update.title
    note.content = note_update.content
    note.category = note_update.category
    note.tags = get_or_create_tags(note_update.tags, session)

    session.add(note)
    session.commit()
    session.refresh(note)

    return note_to_response(note)


@app.patch("/notes/{note_id}")
def partial_update_note(
    note_id: int,
    note_update: NoteUpdate,
    session: SessionDep,
) -> NoteResponse:
    """
    Partially update a note.

    PATCH updates only the fields that are provided.
    """

    note = session.get(Note, note_id)

    if not note:
        raise HTTPException(
            status_code=404,
            detail=f"Note with ID {note_id} not found",
        )

    update_data = note_update.model_dump(exclude_unset=True)

    if "title" in update_data:
        note.title = update_data["title"]

    if "content" in update_data:
        note.content = update_data["content"]

    if "category" in update_data:
        note.category = update_data["category"]

    if "tags" in update_data:
        note.tags = get_or_create_tags(update_data["tags"], session)

    session.add(note)
    session.commit()
    session.refresh(note)

    return note_to_response(note)


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: SessionDep):
    """Delete a note by ID"""

    note = session.get(Note, note_id)

    if not note:
        raise HTTPException(
            status_code=404,
            detail=f"Note with ID {note_id} not found",
        )

    session.delete(note)
    session.commit()

    return


############################################
### Tags endpoints
############################################


@app.get("/tags")
def list_tags(session: SessionDep) -> list[str]:
    """Get all unique tags"""

    tags = session.exec(select(Tag)).all()

    return sorted([tag.name for tag in tags])


@app.get("/tags/{tag_name}/notes")
def get_notes_by_tag(
    tag_name: str,
    session: SessionDep,
) -> list[NoteResponse]:
    """Get all notes with a specific tag"""

    tag_lower = normalize_tag(tag_name)

    statement = select(Tag).where(Tag.name == tag_lower)
    tag = session.exec(statement).first()

    if not tag:
        return []

    return [note_to_response(note) for note in tag.notes]


############################################
### Categories endpoints
############################################


@app.get("/categories")
def list_categories(session: SessionDep) -> list[str]:
    """Get all unique categories"""

    notes = session.exec(select(Note)).all()

    categories = set()

    for note in notes:
        categories.add(note.category)

    return sorted(list(categories))


@app.get("/categories/{category_name}/notes")
def get_notes_by_category(
    category_name: str,
    session: SessionDep,
) -> list[NoteResponse]:
    """Get all notes in a specific category"""

    statement = select(Note).where(Note.category == category_name)
    notes = session.exec(statement).all()

    return [note_to_response(note) for note in notes]


############################################
### Query Parameters Practice
############################################


@app.get("/queryparameters")
def query_parameters(param1: str = None, param2: int = None) -> dict:
    """
    Example endpoint to demonstrate query parameters.
    """

    namen = ["martin", "sophia", "michael", "emma", "maria", "matthias"]

    if not param1:
        return {"namen": namen}

    namen_gefiltert = []

    for name in namen:
        if param1 in name:
            namen_gefiltert.append(name)

    return {
        "param1": param1,
        "param2": param2,
        "namen": namen_gefiltert,
    }

############################################
### Course API
############################################


class CourseCreate(BaseModel):
    """Model for creating courses (no ID)"""
    code: str
    name: str
    semester: int
    ects: int
    lecturer: str


class Course(BaseModel):
    """Model for courses (with ID)"""
    id: int
    code: str
    name: str
    semester: int
    ects: int
    lecturer: str


COURSES_FILE = Path("courses.json")


def load_courses():
    courses_db = []
    course_id_counter = 1

    if COURSES_FILE.exists():
        with open(COURSES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            courses_db = [Course(**course) for course in data]

            if courses_db:
                course_id_counter = max(c.id for c in courses_db) + 1

    return courses_db, course_id_counter


def save_courses(courses_db):
    with open(COURSES_FILE, 'w', encoding='utf-8') as f:
        courses_data = [course.dict() for course in courses_db]
        json.dump(courses_data, f, indent=2, ensure_ascii=False)


@app.post("/courses", status_code=201)
def create_course(course: CourseCreate) -> Course:
    """Create a new course"""
    courses_db, course_id_counter = load_courses()

    for existing in courses_db:
        if existing.code.upper() == course.code.upper():
            raise HTTPException(
                status_code=409,
                detail=f"Course with code '{course.code}' already exists"
            )

    new_course = Course(
        id=course_id_counter,
        **course.dict()
    )

    courses_db.append(new_course)
    save_courses(courses_db)

    return new_course


@app.get("/courses")
def list_courses(
    semester: int = None,
    min_ects: int = 0
) -> list[Course]:
    """List all courses with optional filters"""
    courses_db, _ = load_courses()

    filtered = courses_db

    if semester is not None:
        filtered = [c for c in filtered if c.semester == semester]

    if min_ects > 0:
        filtered = [c for c in filtered if c.ects >= min_ects]

    return filtered


@app.get("/courses/{course_id}")
def get_course(course_id: int) -> Course:
    """Get a specific course by ID"""
    courses_db, _ = load_courses()

    for course in courses_db:
        if course.id == course_id:
            return course

    raise HTTPException(
        status_code=404,
        detail=f"Course with ID {course_id} not found"
    )
