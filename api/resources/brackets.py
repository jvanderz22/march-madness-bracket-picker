from flask_restful import Api, Resource, reqparse, request
from flask import jsonify
from models import Bracket, BracketMatchup, Game, Tournament
from sqlalchemy import or_

from db.session import session_scope

tournament_year = 2021


def bracket_response_json(bracket_id):
    with session_scope() as session:
        bracket = session.query(Bracket).filter(Bracket.id == bracket_id).first()
        picked_matchups = (
            session.query(BracketMatchup)
            .filter(
                BracketMatchup.bracket_id == bracket_id,
                BracketMatchup.winner_id != None,
            )
            .all()
        )
        available_matchups = (
            session.query(BracketMatchup)
            .filter(
                BracketMatchup.bracket_id == bracket_id,
                BracketMatchup.team1_id != None,
                BracketMatchup.team2_id != None,
                BracketMatchup.winner_id == None,
            )
            .all()
        )

        unavailable_matchups = (
            session.query(BracketMatchup)
            .filter(
                BracketMatchup.bracket_id == bracket_id,
                or_(BracketMatchup.team1_id == None, BracketMatchup.team2_id == None),
            )
            .all()
        )

        return {
            **bracket.to_dict(),
            "picked_matchups": [matchup.to_dict() for matchup in picked_matchups],
            "available_matchups": [matchup.to_dict() for matchup in available_matchups],
            "unavailable_matchups": [
                matchup.to_dict() for matchup in unavailable_matchups
            ],
        }


class BracketsResource(Resource):
    def get(self):
        user_id = request.environ["user"]["id"]
        with session_scope() as session:
            brackets = session.query(Bracket).filter(Bracket.user_id == user_id).all()
            return [bracket.to_dict() for bracket in brackets]

    def post(self):
        user_id = request.environ["user"]["id"]
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)

        args = parser.parse_args()

        with session_scope() as session:
            tournament = (
                session.query(Tournament)
                .filter(Tournament.year == tournament_year)
                .first()
            )
            bracket = Bracket(
                name=args["name"], user_id=user_id, tournament_id=tournament.id
            )
            session.add(bracket)
            session.commit()

            games = (
                session.query(Game)
                .filter(
                    Game.tournament_id == tournament.id, Game.exists_in_bracket == True
                )
                .all()
            )

            bracket_matchups = [
                BracketMatchup(
                    bracket_id=bracket.id,
                    game_id=game.id,
                    round_number=game.round_number,
                    game_number=game.game_number,
                    team1_id=game.team1_id,
                    team2_id=game.team2_id,
                )
                for game in games
            ]

            session.add_all(bracket_matchups)
            session.commit()

            return bracket_response_json(bracket.id), 201


class BracketResource(Resource):
    def get(self, bracket_id):
        return bracket_response_json(bracket_id), 200
