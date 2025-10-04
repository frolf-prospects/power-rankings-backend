from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship


class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    fun_fact: Optional[str] = Field(default=None)
    power_ranking: Optional[int] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PlayerCreate(SQLModel):
    first_name: str
    last_name: str
    fun_fact: Optional[str] = None
    power_ranking: Optional[int] = None


class PlayerUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    fun_fact: Optional[str] = None
    power_ranking: Optional[int] = None


class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    location: str
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CourseCreate(SQLModel):
    name: str
    location: str
    description: str


class CourseUpdate(SQLModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None


class Hole(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="course.id")
    hole_number: int
    par: int
    length: int
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class HoleCreate(SQLModel):
    course_id: int
    hole_number: int
    par: int
    length: int
    description: Optional[str] = None


class HoleUpdate(SQLModel):
    course_id: Optional[int] = None
    hole_number: Optional[int] = None
    par: Optional[int] = None
    length: Optional[int] = None
    description: Optional[str] = None


class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_ids: str  # JSON string of player IDs for simplicity
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class GameCreate(SQLModel):
    player_ids: str
    description: Optional[str] = None


class GameUpdate(SQLModel):
    player_ids: Optional[str] = None
    description: Optional[str] = None


class Score(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    hole_id: int = Field(foreign_key="hole.id")
    player_id: int = Field(foreign_key="player.id")
    score: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ScoreCreate(SQLModel):
    game_id: int
    hole_id: int
    player_id: int
    score: int


class ScoreUpdate(SQLModel):
    game_id: Optional[int] = None
    hole_id: Optional[int] = None
    player_id: Optional[int] = None
    score: Optional[int] = None
