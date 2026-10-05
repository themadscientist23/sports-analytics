import datetime

from pydantic import BaseModel


class TeamStanding(BaseModel):
    id: int
    name: str
    abbreviation: str
    wins: int
    losses: int
    ties: int
    points_for: int
    points_against: int
    catelo: float | None


class TeamSummary(BaseModel):
    id: int
    name: str
    abbreviation: str
    current_catelo: float | None


class GameHistoryEntry(BaseModel):
    date: datetime.date
    catelo: float
    opponent: str
    home: bool
    score: str


class TeamDetail(BaseModel):
    team: TeamSummary
    history: list[GameHistoryEntry]
