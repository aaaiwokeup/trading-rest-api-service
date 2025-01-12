from flask import request, render_template, Blueprint
from flask_jwt_extended import jwt_required
import redis

from db import engine
from services import StrategyService

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

strategies = Blueprint("strategies", __name__)
strategy_service = StrategyService(redis_client, engine)

@strategies.route('/', methods=['GET'])
def get_strategies():
    return render_template("strategy_crud.html")

# Create and save strategy to PostgreSQL
@strategies.route('/', methods=['POST'])
@jwt_required()
def create_strategy():
    data = request.get_json()
    return strategy_service.create_strategy(data)

# Read user's strategies
@strategies.route('/<int:strategy_id>', methods=['GET'])
@jwt_required()
def read_strategy(strategy_id):
    return strategy_service.read_strategy(strategy_id)

# Update user's strategy
@strategies.route('/<int:strategy_id>', methods=['PUT'])
@jwt_required()
def update_strategy(strategy_id):
    data = request.get_json()
    return strategy_service.update_strategy(strategy_id, data)

# Delete user`s strategy
@strategies.route('/<int:strategy_id>', methods=['DELETE'])
@jwt_required()
def delete_strategy(strategy_id):
    return strategy_service.delete_strategy(strategy_id)

# Strategy simulation
@strategies.route("/<int:strategy_id>/simulate", methods=['POST'])
@jwt_required()
def simulate(strategy_id):
    historical_data = request.get_json()
    return strategy_service.simulate(strategy_id, historical_data)