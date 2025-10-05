import json
import os
from contextlib import contextmanager
from typing import Iterator, Generator

from sqlmodel import SQLModel, Session, create_engine, select

from .config import settings
from .models import Player, Course, Hole


# SQLite specific connect args are safe to pass for other DBs as empty dict
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, echo=False, connect_args=connect_args)


def create_db_and_tables() -> None:
    # Create all tables with new schema
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


def get_db_session() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session and closes it after use"""
    with Session(engine) as session:
        yield session


def seed_database() -> None:
    """Load seed data from JSON files into the database"""
    with Session(engine) as session:
        # Get the path to the db_seeds directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        seeds_dir = os.path.join(current_dir, "db_seeds")
        
        # Seed Players
        players_file = os.path.join(seeds_dir, "players.json")
        if os.path.exists(players_file):
            with open(players_file, 'r') as f:
                players_data = json.load(f)
                for player_data in players_data:
                    player = Player(**player_data)
                    session.add(player)
            print(f"Seeded {len(players_data)} players")
        
        # Seed Courses
        courses_file = os.path.join(seeds_dir, "courses.json")
        if os.path.exists(courses_file):
            with open(courses_file, 'r') as f:
                courses_data = json.load(f)
                for course_data in courses_data:
                    course = Course(**course_data)
                    session.add(course)
            print(f"Seeded {len(courses_data)} courses")
        
        # Seed Holes
        holes_file = os.path.join(seeds_dir, "holes.json")
        if os.path.exists(holes_file):
            with open(holes_file, 'r') as f:
                holes_data = json.load(f)
                for hole_data in holes_data:
                    hole = Hole(**hole_data)
                    session.add(hole)
            print(f"Seeded {len(holes_data)} holes")
        
        session.commit()
        print("Database seeding completed successfully!")


