from app.sports.nfl.models import NFLGame, NFLGameRating, NFLTeam
from app.sports.nfl.rating import process_game

NFL_CONFIG = {
    "team_model": NFLTeam,
    "game_model": NFLGame,
    "rating_model": NFLGameRating,
    "process_game": process_game,
}
