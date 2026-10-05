from app.sports.nba.models import NBAGame, NBAGameRating, NBATeam
from app.sports.nba.rating import process_game

NBA_CONFIG = {
    "team_model": NBATeam,
    "game_model": NBAGame,
    "rating_model": NBAGameRating,
    "process_game": process_game,
}
