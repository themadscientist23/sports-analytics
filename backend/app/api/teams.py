from fastapi import APIRouter, HTTPException

from app.api.deps import DbSession
from app.schemas.teams import TeamDetail, TeamStanding
from app.services.stats import catelo_history, seasons, standings, team_by_abbreviation
from app.sports.config import SPORTS, Sport

router = APIRouter()


@router.get("/{sport}/seasons", response_model=list[int])
def get_seasons(sport: Sport, db: DbSession):
    config = SPORTS[sport]
    return seasons(db, config)


@router.get("/{sport}/seasons/{season}/teams", response_model=list[TeamStanding])
def get_teams(sport: Sport, season: int, db: DbSession):
    config = SPORTS[sport]
    return standings(db, config, season)


@router.get("/{sport}/seasons/{season}/teams/{abbreviation}", response_model=TeamDetail)
def get_team(sport: Sport, season: int, abbreviation: str, db: DbSession):
    config = SPORTS[sport]
    team = team_by_abbreviation(db, config, abbreviation)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    history = catelo_history(db, config, team.id, season)
    return {
        "team": {
            "id": team.id,
            "name": team.name,
            "abbreviation": team.abbreviation,
            "current_catelo": history[-1]["catelo"] if history else None,
        },
        "history": history,
    }
