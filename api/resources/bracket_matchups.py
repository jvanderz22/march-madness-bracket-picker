from flask_restful import Api, Resource, reqparse, request
import math

from models import Bracket, BracketMatchup, Team, TournamentTeam
from db.session import session_scope


class BracketWinnerError(Exception):
    def __init__(self, message):
        self.message = message


def set_bracket_matchup_winner(session, bracket_matchup, winner_id, notes, confidence):
    if bracket_matchup.winner_id is not None:
        raise BracketWinnerError("Could not set new winner matchup")
    if bracket_matchup.team1_id != winner_id and bracket_matchup.team2_id != winner_id:
        raise BracketWinnerError("Invalid winner for matchup")

    bracket_matchup.winner_id = winner_id
    bracket_matchup.notes = notes
    bracket_matchup.confidence = confidence

    next_game_number = math.ceil(bracket_matchup.game_number / 2)
    next_matchup = (
        session.query(BracketMatchup)
        .filter(
            BracketMatchup.bracket_id == bracket_matchup.bracket_id,
            BracketMatchup.round_number == bracket_matchup.round_number + 1,
            BracketMatchup.game_number == next_game_number,
        )
        .first()
    )

    if next_matchup is not None:
        winner_next_game_position = 1 if bracket_matchup.game_number % 2 == 1 else 2
        if winner_next_game_position == 1:
            next_matchup.team1_id = winner_id
        else:
            next_matchup.team2_id = winner_id

    session.commit()


def get_team_data_json(session, team_id, tournament_id):
    team = session.query(Team).filter(Team.id == team_id).first()
    tournament_team = (
        session.query(TournamentTeam)
        .filter(
            TournamentTeam.team_id == team_id,
            TournamentTeam.tournament_id == tournament_id,
        )
        .first()
    )
    return {
        "id": team.id,
        "name": team.name,
        "tournament_team_id": tournament_team.id,
        "seed": tournament_team.seed,
        "stats": tournament_team.stats,
    }


def bracket_matchup_response_json(session, bracket_matchup, bracket):
    tournament_id = bracket.tournament_id
    team1_dict = None
    team2_dict = None
    if bracket_matchup.team1_id is not None:
        team1_dict = get_team_data_json(
            session, bracket_matchup.team1_id, tournament_id
        )

    if bracket_matchup.team2_id is not None:
        team2_dict = get_team_data_json(
            session, bracket_matchup.team2_id, tournament_id
        )

    bracket_matchup_data = bracket_matchup.to_dict()
    return {**bracket_matchup_data, "team1": team1_dict, "team2": team2_dict}


def get_bracket_matchup_bracket(session, bracket_matchup_id):
    user_id = request.environ["user"]["id"]
    bracket_matchup = (
        session.query(BracketMatchup)
        .filter(BracketMatchup.id == bracket_matchup_id)
        .first()
    )
    bracket = (
        session.query(Bracket)
        .filter(Bracket.id == bracket_matchup.bracket_id, Bracket.user_id == user_id)
        .first()
    )
    return bracket_matchup, bracket


class BracketMatchupResource(Resource):
    def get(self, bracket_matchup_id):
        with session_scope() as session:
            bracket_matchup, bracket = get_bracket_matchup_bracket(
                session, bracket_matchup_id
            )
            if bracket is None or bracket_matchup is None:
                return None, 404
            return bracket_matchup_response_json(session, bracket_matchup, bracket), 200

    def patch(self, bracket_matchup_id):
        with session_scope() as session:
            bracket_matchup, bracket = get_bracket_matchup_bracket(
                session, bracket_matchup_id
            )
            if bracket is None or bracket_matchup is None:
                return None, 404
            parser = reqparse.RequestParser()
            parser.add_argument("winner_id", type=str)
            parser.add_argument("notes", type=str)
            parser.add_argument("confidence", type=int)
            args = parser.parse_args()
            winner_id = args["winner_id"]
            notes = args.get("notes", "")
            confidence = args.get("confidence", None)

            try:
                set_bracket_matchup_winner(
                    session, bracket_matchup, winner_id, notes, confidence
                )
            except BracketWinnerError as e:
                return {"message": e.message}, 400

            return bracket_matchup_response_json(session, bracket_matchup, bracket), 200
