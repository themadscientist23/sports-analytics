from app.sports.mlb.models import MLBGame, MLBGameRating, MLBTeam
from app.sports.mlb.rating import process_game

MLB_CONFIG = {
    "team_model": MLBTeam,
    "game_model": MLBGame,
    "rating_model": MLBGameRating,
    "process_game": process_game,
}
