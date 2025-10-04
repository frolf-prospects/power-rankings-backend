import json
from typing import List, Optional

from fastapi import Depends, HTTPException
from sqlmodel import select, Session

from . import api_router
from ..db import get_db_session
from ..models import (
    Player, PlayerCreate, PlayerUpdate,
    Course, CourseCreate, CourseUpdate,
    Hole, HoleCreate, HoleUpdate,
    Game, GameCreate, GameUpdate,
    Score, ScoreCreate, ScoreUpdate
)


@api_router.get("/health")
def healthcheck() -> dict:
    return {"status": "ok"}


# Player endpoints
@api_router.get("/players", response_model=List[Player])
def list_players(session: Session = Depends(get_db_session)) -> List[Player]:
    result = session.exec(select(Player)).all()
    return result


@api_router.post("/players", response_model=Player)
def create_player(player: PlayerCreate, session: Session = Depends(get_db_session)) -> Player:
    db_player = Player.model_validate(player)
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player


@api_router.get("/players/{player_id}", response_model=Player)
def get_player(player_id: int, session: Session = Depends(get_db_session)) -> Player:
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@api_router.put("/players/{player_id}", response_model=Player)
def update_player(player_id: int, player_update: PlayerUpdate, session: Session = Depends(get_db_session)) -> Player:
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    player_data = player_update.model_dump(exclude_unset=True)
    for field, value in player_data.items():
        setattr(player, field, value)
    
    session.add(player)
    session.commit()
    session.refresh(player)
    return player


@api_router.delete("/players/{player_id}")
def delete_player(player_id: int, session: Session = Depends(get_db_session)) -> dict:
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    session.delete(player)
    session.commit()
    return {"message": "Player deleted successfully"}


# Course endpoints
@api_router.get("/courses", response_model=List[Course])
def list_courses(session: Session = Depends(get_db_session)) -> List[Course]:
    result = session.exec(select(Course)).all()
    return result


@api_router.post("/courses", response_model=Course)
def create_course(course: CourseCreate, session: Session = Depends(get_db_session)) -> Course:
    db_course = Course.model_validate(course)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course


@api_router.get("/courses/{course_id}", response_model=Course)
def get_course(course_id: int, session: Session = Depends(get_db_session)) -> Course:
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@api_router.put("/courses/{course_id}", response_model=Course)
def update_course(course_id: int, course_update: CourseUpdate, session: Session = Depends(get_db_session)) -> Course:
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    course_data = course_update.model_dump(exclude_unset=True)
    for field, value in course_data.items():
        setattr(course, field, value)
    
    session.add(course)
    session.commit()
    session.refresh(course)
    return course


@api_router.delete("/courses/{course_id}")
def delete_course(course_id: int, session: Session = Depends(get_db_session)) -> dict:
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    session.delete(course)
    session.commit()
    return {"message": "Course deleted successfully"}


# Hole endpoints
@api_router.get("/courses/{course_id}/holes", response_model=List[Hole])
def list_holes_by_course(course_id: int, session: Session = Depends(get_db_session)) -> List[Hole]:
    # Verify course exists
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    result = session.exec(select(Hole).where(Hole.course_id == course_id)).all()
    return result


@api_router.post("/holes", response_model=Hole)
def create_hole(hole: HoleCreate, session: Session = Depends(get_db_session)) -> Hole:
    # Verify course exists
    course = session.get(Course, hole.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_hole = Hole.model_validate(hole)
    session.add(db_hole)
    session.commit()
    session.refresh(db_hole)
    return db_hole


@api_router.get("/holes/{hole_id}", response_model=Hole)
def get_hole(hole_id: int, session: Session = Depends(get_db_session)) -> Hole:
    hole = session.get(Hole, hole_id)
    if not hole:
        raise HTTPException(status_code=404, detail="Hole not found")
    return hole


@api_router.put("/holes/{hole_id}", response_model=Hole)
def update_hole(hole_id: int, hole_update: HoleUpdate, session: Session = Depends(get_db_session)) -> Hole:
    hole = session.get(Hole, hole_id)
    if not hole:
        raise HTTPException(status_code=404, detail="Hole not found")
    
    # Verify course exists if course_id is being updated
    if hole_update.course_id is not None:
        course = session.get(Course, hole_update.course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
    
    hole_data = hole_update.model_dump(exclude_unset=True)
    for field, value in hole_data.items():
        setattr(hole, field, value)
    
    session.add(hole)
    session.commit()
    session.refresh(hole)
    return hole


@api_router.delete("/holes/{hole_id}")
def delete_hole(hole_id: int, session: Session = Depends(get_db_session)) -> dict:
    hole = session.get(Hole, hole_id)
    if not hole:
        raise HTTPException(status_code=404, detail="Hole not found")
    
    session.delete(hole)
    session.commit()
    return {"message": "Hole deleted successfully"}


# Game endpoints
@api_router.get("/games", response_model=List[Game])
def list_games(session: Session = Depends(get_db_session)) -> List[Game]:
    result = session.exec(select(Game)).all()
    return result


@api_router.post("/games", response_model=Game)
def create_game(game: GameCreate, session: Session = Depends(get_db_session)) -> Game:
    # Validate player IDs exist
    try:
        player_ids = json.loads(game.player_ids)
        for player_id in player_ids:
            player = session.get(Player, player_id)
            if not player:
                raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for player_ids")
    
    db_game = Game.model_validate(game)
    session.add(db_game)
    session.commit()
    session.refresh(db_game)
    return db_game


@api_router.get("/games/{game_id}", response_model=Game)
def get_game(game_id: int, session: Session = Depends(get_db_session)) -> Game:
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@api_router.put("/games/{game_id}", response_model=Game)
def update_game(game_id: int, game_update: GameUpdate, session: Session = Depends(get_db_session)) -> Game:
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Validate player IDs if being updated
    if game_update.player_ids is not None:
        try:
            player_ids = json.loads(game_update.player_ids)
            for player_id in player_ids:
                player = session.get(Player, player_id)
                if not player:
                    raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found")
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format for player_ids")
    
    game_data = game_update.model_dump(exclude_unset=True)
    for field, value in game_data.items():
        setattr(game, field, value)
    
    session.add(game)
    session.commit()
    session.refresh(game)
    return game


@api_router.delete("/games/{game_id}")
def delete_game(game_id: int, session: Session = Depends(get_db_session)) -> dict:
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    session.delete(game)
    session.commit()
    return {"message": "Game deleted successfully"}


# Score endpoints
@api_router.get("/scores", response_model=List[Score])
def list_scores(
    game_id: Optional[int] = None,
    hole_id: Optional[int] = None,
    player_id: Optional[int] = None,
    session: Session = Depends(get_db_session)
) -> List[Score]:
    query = select(Score)
    
    if game_id is not None:
        query = query.where(Score.game_id == game_id)
    if hole_id is not None:
        query = query.where(Score.hole_id == hole_id)
    if player_id is not None:
        query = query.where(Score.player_id == player_id)
    
    result = session.exec(query).all()
    return result


@api_router.post("/scores", response_model=Score)
def create_score(score: ScoreCreate, session: Session = Depends(get_db_session)) -> Score:
    # Validate foreign keys exist
    game = session.get(Game, score.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    hole = session.get(Hole, score.hole_id)
    if not hole:
        raise HTTPException(status_code=404, detail="Hole not found")
    
    player = session.get(Player, score.player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    db_score = Score.model_validate(score)
    session.add(db_score)
    session.commit()
    session.refresh(db_score)
    return db_score


@api_router.get("/scores/{score_id}", response_model=Score)
def get_score(score_id: int, session: Session = Depends(get_db_session)) -> Score:
    score = session.get(Score, score_id)
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    return score


@api_router.put("/scores/{score_id}", response_model=Score)
def update_score(score_id: int, score_update: ScoreUpdate, session: Session = Depends(get_db_session)) -> Score:
    score = session.get(Score, score_id)
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    
    # Validate foreign keys if being updated
    if score_update.game_id is not None:
        game = session.get(Game, score_update.game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
    
    if score_update.hole_id is not None:
        hole = session.get(Hole, score_update.hole_id)
        if not hole:
            raise HTTPException(status_code=404, detail="Hole not found")
    
    if score_update.player_id is not None:
        player = session.get(Player, score_update.player_id)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
    
    score_data = score_update.model_dump(exclude_unset=True)
    for field, value in score_data.items():
        setattr(score, field, value)
    
    session.add(score)
    session.commit()
    session.refresh(score)
    return score


@api_router.delete("/scores/{score_id}")
def delete_score(score_id: int, session: Session = Depends(get_db_session)) -> dict:
    score = session.get(Score, score_id)
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    
    session.delete(score)
    session.commit()
    return {"message": "Score deleted successfully"}


