from pathlib import Path
import json

from models import Game, Team, Tournament
from db.session import session_scope

from scripts.utils import get_pos_round, get_pos_game_number, get_region, TOTAL_ROUNDS


def create_teams(session, bracket_info):
    for team_info in bracket_info:
        team_name = team_info["team"]
        team = session.query(Team.id).filter(Team.name == team_name).first()
        if team is None:
            team = Team(name=team_name)
            session.add(team)


def add_team_to_tournament(session, team_info):
    pos = team_info["pos"]
    round = get_pos_round(pos)
    game_number = get_pos_game_number(pos)
    if round == 1:
        game_position = 1 if pos.find("a") > -1 else 2
    else:
        game_position = 1 if int(pos) % 2 == 1 else 2

    game = (
        session.query(Game)
        .filter(Game.round_number == round, Game.game_number == game_number)
        .first()
    )
    team = session.query(Team).filter(Team.name == team_info["team"]).first()
    print("team_id", team.id)

    if game_position == 1:
        game.team1_id = team.id
    if game_position == 2:
        game.team2_id = team.id


def create_games(session, tournament, bracket_info):
    round_number = TOTAL_ROUNDS
    while round_number > 0:
        games_in_round = 2 ** (TOTAL_ROUNDS - round_number)
        game_number = 1
        while game_number <= games_in_round:

            game = (
                session.query(Game.id)
                .filter(
                    Game.round_number == round_number, Game.game_number == game_number
                )
                .first()
            )
            if game is None:
                region = get_region(round_number, game_number)
                game = Game(
                    round_number=round_number,
                    game_number=game_number,
                    tournament_id=tournament.id,
                    region=region,
                )
                session.add(game)
            game_number += 1
        round_number -= 1
    for team_info in bracket_info:
        add_team_to_tournament(session, team_info)
    not_included_games = (
        session.query(Game)
        .filter(Game.round_number == 1, Game.team1_id == None, Game.team2_id == None)
        .all()
    )
    for game in not_included_games:
        game.exists_in_bracket = False
    session.commit()


if __name__ == "__main__":

    base_path = Path(__file__).parent.parent
    tournament_file_dir = base_path / "data/tournament_data"
    tournament_file = "ncaa_mens_2021_bracket.json"
    tournament_file_data = open(tournament_file_dir / tournament_file, "r")
    tournament_data = json.load(tournament_file_data)
    bracket_info = tournament_data["bracket"]
    with session_scope() as session:
        create_teams(session, bracket_info)

        tournament = (
            session.query(Tournament.id)
            .filter(Tournament.tournament_name == tournament_data["name"])
            .first()
        )
        if tournament is None:
            tournament = Tournament(
                tournament_name=tournament_data["name"],
                year=tournament_data["year"],
            )
            session.add(tournament)
        create_games(session, tournament, bracket_info)
