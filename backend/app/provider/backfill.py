import argparse
import logging
import time

from app.db.session import SessionLocal
from app.provider.api_client import list_games
from app.provider.games import API_GAMES
from app.sports.config import SPORTS

logger = logging.getLogger(__name__)


def _create_or_update_team(session, team_model, team_data):
    team = session.get(team_model, team_data["id"])
    if team is None:
        team = team_model(id=team_data["id"])
        session.add(team)
    team.name = team_data["name"]
    team.abbreviation = team_data["abbreviation"]


def _is_excluded(game, fields):
    return game.is_excluded() or fields["home_team"]["id"] < 0 or fields["away_team"]["id"] < 0


def _mark_games_past_regular_season(session, game_model, regular_season_games, season):
    games = session.query(game_model).filter(game_model.season == season).order_by(game_model.date, game_model.id).all()

    played = {}
    for game in games:
        played[game.away_team_id] = played.get(game.away_team_id, 0) + 1
        played[game.home_team_id] = played.get(game.home_team_id, 0) + 1
        if played[game.home_team_id] > regular_season_games:
            game.postseason = True


def ingest_games(sport, season=None, dates=None, request_delay=60):
    config = SPORTS[sport]
    team_model = config["team_model"]
    game_model = config["game_model"]
    api_game_model = API_GAMES[sport]

    added_count = 0
    skipped_count = 0
    excluded_count = 0
    added_season = None
    cursor = None

    with SessionLocal() as session:
        while True:
            logger.info(f"[{sport}] Fetching next page...")
            games_page = list_games(sport, 100, season=season, cursor=cursor, dates=dates)
            page_games = games_page["data"]
            if not page_games:
                break

            for game_data in page_games:
                game = api_game_model.model_validate(game_data)
                if not game.is_final():
                    skipped_count += 1
                    continue

                if session.get(game_model, game.id):
                    continue

                fields = game.extract()
                if _is_excluded(game, fields):
                    excluded_count += 1
                    continue

                _create_or_update_team(session, team_model, fields["home_team"])
                _create_or_update_team(session, team_model, fields["away_team"])

                session.add(
                    game_model(
                        id=game.id,
                        season=game.season,
                        date=game.game_date(),
                        postseason=game.postseason,
                        **fields["game"],
                    )
                )
                added_count += 1
                added_season = game.season

            session.commit()
            cursor = games_page["meta"].get("next_cursor")
            if not cursor:
                break
            time.sleep(request_delay)

        if added_season:
            _mark_games_past_regular_season(session, game_model, api_game_model.regular_season_games, added_season)
        session.commit()

        logger.info(
            f"[{sport}] Done. Added {added_count} games, skipped {skipped_count} non-final, excluded {excluded_count}."
        )
        return added_count


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="Backfill historical games for a sport/season.")
    parser.add_argument("sport", choices=SPORTS.keys())
    parser.add_argument("season", type=int)
    parser.add_argument(
        "--request-delay",
        type=float,
        default=60,
        help="Seconds to sleep between paginated API requests",
    )
    args = parser.parse_args()

    ingest_games(args.sport, args.season, request_delay=args.request_delay)
