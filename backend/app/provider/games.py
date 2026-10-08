from datetime import date, datetime
from typing import Any, ClassVar
from zoneinfo import ZoneInfo

from pydantic import BaseModel

PACIFIC = ZoneInfo("America/Los_Angeles")


class NBAApiTeam(BaseModel):
    id: int
    full_name: str
    abbreviation: str


class NBAApiGame(BaseModel):
    regular_season_games: ClassVar[int] = 82

    id: int
    date: str
    season: int
    status: str
    postseason: bool
    home_team: NBAApiTeam
    visitor_team: NBAApiTeam
    home_team_score: int
    visitor_team_score: int
    ist_stage: str | None

    def is_final(self) -> bool:
        return self.status == "Final"

    def is_excluded(self) -> bool:
        return self.ist_stage == "Championship"

    def game_date(self) -> date:
        return date.fromisoformat(self.date)

    def extract(self) -> dict[str, Any]:
        home, away = self.home_team, self.visitor_team
        return {
            "home_team": {"id": home.id, "name": home.full_name, "abbreviation": home.abbreviation},
            "away_team": {"id": away.id, "name": away.full_name, "abbreviation": away.abbreviation},
            "game": {
                "home_team_id": home.id,
                "away_team_id": away.id,
                "home_score": self.home_team_score,
                "away_score": self.visitor_team_score,
            },
        }


class NFLApiTeam(BaseModel):
    id: int
    full_name: str
    abbreviation: str


class NFLApiGame(BaseModel):
    regular_season_games: ClassVar[int] = 17

    id: int
    date: str
    season: int
    status: str
    postseason: bool
    home_team: NFLApiTeam
    visitor_team: NFLApiTeam
    home_team_score: int | None
    visitor_team_score: int | None

    def is_final(self) -> bool:
        return self.status == "Final"

    def is_excluded(self) -> bool:
        return False

    def game_date(self) -> date:
        return datetime.fromisoformat(self.date).astimezone(PACIFIC).date()

    def extract(self) -> dict[str, Any]:
        home, away = self.home_team, self.visitor_team
        return {
            "home_team": {"id": home.id, "name": home.full_name, "abbreviation": home.abbreviation},
            "away_team": {"id": away.id, "name": away.full_name, "abbreviation": away.abbreviation},
            "game": {
                "home_team_id": home.id,
                "away_team_id": away.id,
                "home_score": self.home_team_score,
                "away_score": self.visitor_team_score,
            },
        }


class MLBApiTeam(BaseModel):
    id: int
    display_name: str
    abbreviation: str


class MLBApiTeamData(BaseModel):
    runs: int


class MLBApiGame(BaseModel):
    regular_season_games: ClassVar[int] = 162

    id: int
    date: str
    season: int
    status: str
    postseason: bool
    season_type: str
    home_team: MLBApiTeam
    away_team: MLBApiTeam
    home_team_data: MLBApiTeamData
    away_team_data: MLBApiTeamData

    def is_final(self) -> bool:
        return self.status == "STATUS_FINAL"

    def is_excluded(self) -> bool:
        return self.season_type == "spring_training"

    def game_date(self) -> date:
        return datetime.fromisoformat(self.date).astimezone(PACIFIC).date()

    def extract(self) -> dict[str, Any]:
        home, away = self.home_team, self.away_team
        return {
            "home_team": {"id": home.id, "name": home.display_name, "abbreviation": home.abbreviation},
            "away_team": {"id": away.id, "name": away.display_name, "abbreviation": away.abbreviation},
            "game": {
                "home_team_id": home.id,
                "away_team_id": away.id,
                "home_score": self.home_team_data.runs,
                "away_score": self.away_team_data.runs,
            },
        }


API_GAMES: dict[str, type[NBAApiGame | NFLApiGame | MLBApiGame]] = {
    "nba": NBAApiGame,
    "nfl": NFLApiGame,
    "mlb": MLBApiGame,
}
