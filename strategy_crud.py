from flask import request, jsonify, render_template, Blueprint
from db import insert_strategy, get_user_id, get_strategy, del_strategy, up_to_date_strategy
from flask_jwt_extended import jwt_required, get_jwt_identity
from rabbitmq import publish_message
import redis
import json

strategies = Blueprint("strategies", __name__)

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

@strategies.route('/', methods=['GET'])
def get_strategies():
    return render_template("strategy_crud.html")

# Create and save strategy to PostgreSQL
@strategies.route('/', methods=['POST'])
@jwt_required()
def create_strategy():
    username = get_jwt_identity()
    user_id = get_user_id(username)

    data = request.get_json()

    insert_strategy(user_id, data)

    message = f"User {user_id} created strategy {data['name']}"
    publish_message("strategy_queue", message)

    redis_client.delete(f"strategies_user_{user_id}")

    return jsonify({"message": "Strategy created", "strategy": data}), 201

# Read user's strategies
@strategies.route('/<int:strategy_id>', methods=['GET'])
@jwt_required()
def read_strategy(strategy_id):
    username = get_jwt_identity()
    user_id = get_user_id(username)

    cache_key = f"strategy_user_{user_id}_id_{strategy_id}"
    cached_strategy = redis_client.get(cache_key)
    if cached_strategy:
        your_strategy = json.loads(cached_strategy)
    else:
        your_strategy = get_strategy(strategy_id)

        redis_client.set(cache_key, json.dumps(your_strategy), ex=3600)

    return jsonify({"message": f"Your strategies: {your_strategy}"})


# Update user's strategy
@strategies.route('/<int:strategy_id>', methods=['PUT'])
@jwt_required()
def update_strategy(strategy_id):
    data = request.get_json()
    username = get_jwt_identity()
    user_id = get_user_id(username)

    up_to_date_strategy(strategy_id, data)

    redis_client.delete(f"strategy_user_{user_id}_id_{strategy_id}")

    message = f"User {user_id} updated strategy {strategy_id}"
    publish_message("strategy_queue", message)

    return jsonify({"message": f"Strategy {strategy_id} was updated!", "strategy": data}), 201

# Delete user`s strategy
@strategies.route('/<int:strategy_id>', methods=['DELETE'])
@jwt_required()
def delete_strategy(strategy_id):
    username = get_jwt_identity()
    user_id = get_user_id(username)

    del_strategy(strategy_id)

    redis_client.delete(f"strategy_user_{user_id}_id_{strategy_id}")

    return jsonify({"message": f"Strategy {strategy_id} deleted"})

# Strategy simulation
@strategies.route("/<int:strategy_id>/simulate", methods=['POST'])
@jwt_required()
def simulate(strategy_id):
    strategy = get_strategy(strategy_id)

    historical_data = request.get_json()

    buy_conditions = strategy.get("buy_conditions", [])
    sell_conditions = strategy.get("sell_conditions", [])

    total_trades = 0
    profit_loss = 0.0
    max_drawdown = 0.0
    current_position = None
    entry_price = 0.0
    highest_equity = 0.0

    for day in historical_data:

        if not current_position and evaluate_conditions(buy_conditions, day):
            current_position = "LONG"
            entry_price = day["close"]
            total_trades += 1

        if current_position and evaluate_conditions(sell_conditions, day):
            profit_loss += day["close"] - entry_price
            current_position = None

        if not current_position:
            current_equity = profit_loss
        else:
            current_equity = profit_loss + (day["close"] - entry_price)
        
        if current_equity > highest_equity:
            highest_equity = current_equity
    
        if highest_equity != 0:
            drawdown = (highest_equity - current_equity) / highest_equity * 100
        else:
            drawdown = 0
            
        max_drawdown = min(max_drawdown, -drawdown)

    win_rate = calculate_win_rate(historical_data, buy_conditions, sell_conditions)

    return jsonify({
        "strategy_id": strategy_id,
        "total_trades": total_trades,
        "profit_loss": round(profit_loss, 2),
        "win_rate": round(win_rate, 2),
        "max_drawdown": round(max_drawdown, 2)
    })

def evaluate_conditions(conditions, data):
    indicator = conditions.get("indicator")
    threshold = conditions.get("threshold")

    if indicator == "momentum":
        momentum = (data["close"] - data["open"]) / data["open"] * 100
        return momentum > threshold if threshold > 0 else momentum < threshold

    return False

def calculate_win_rate(historical_data, buy_conditions, sell_conditions):
    wins = 0
    total = 0
    current_position = None
    entry_price = 0.0

    for day in historical_data:
        if not current_position and evaluate_conditions(buy_conditions, day):
            current_position = "LONG"
            entry_price = day["close"]

        elif current_position and evaluate_conditions(sell_conditions, day):
            total += 1
            if day["close"] > entry_price:
                wins += 1
            current_position = None

    if total == 0:
        return 0.0

    return (wins / total) * 100
