from pathlib import Path
import json

from models import Game, Team, Tournament, TournamentAverage, TournamentTeam
from db.session import session_scope

from scripts.utils import get_region, get_pos_round, get_pos_game_number

if __name__ == "__main__":

    base_path = Path(__file__).parent.parent
    tournament_file_dir = base_path / "data/tournament_data"
    tournament_file = "ncaa_mens_2021_bracket.json"
    tournament_file_data = open(tournament_file_dir / tournament_file, "r")
    tournament_data = json.load(tournament_file_data)

    averages_file = (
        base_path / "scripts/kenpom_scraping/averages_data" / "averages_2021.json"
    )
    averages_file_data = open(averages_file, "r")
    averages_data = json.load(averages_file_data)

    teams_file = base_path / "scripts/kenpom_scraping/teams_data" / "teams_2021.json"
    teams_file_data = open(teams_file, "r")
    team_stats_data = json.load(teams_file_data)

    bracket_info = tournament_data["bracket"]
    with session_scope() as session:
        tournament = (
            session.query(Tournament.id)
            .filter(Tournament.tournament_name == tournament_data["name"])
            .first()
        )

        for team_info in bracket_info:
            pos = team_info["pos"]
            region = get_region(get_pos_round(pos), get_pos_game_number(pos))
            seed = team_info["seed"]
            team_name = team_info["team"]
            team_stats = team_stats_data["data"][team_name]

            team = session.query(Team).filter(Team.name == team_name).first()
            tournament_team = (
                session.query(TournamentTeam)
                .filter(
                    TournamentTeam.team_id == team.id,
                    TournamentTeam.tournament_id == tournament.id,
                )
                .first()
            )
            if tournament_team is None:
                tournament_team = TournamentTeam(
                    team_id=team.id,
                    tournament_id=tournament.id,
                    seed=seed,
                    region=region,
                    stats=team_stats,
                )
                session.add(tournament_team)

        tournament_average = (
            session.query(TournamentAverage)
            .filter(TournamentAverage.id == tournament.id)
            .first()
        )
        if tournament_average is None:
            tournament_average = TournamentAverage(
                tournament_id=tournament.id, stats=averages_data["data"]
            )
            session.add(tournament_average)
