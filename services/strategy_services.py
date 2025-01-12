from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from rabbitmq import publish_message
from sqlalchemy import insert, select, update, delete
import json

from db import users_table, strategies_table

class StrategyService:
    def __init__(self, redis_client, engine):
        self.redis_client = redis_client
        self.engine = engine

    # DB requests
    def get_user_id(self, username):
        with self.engine.connect() as conn:
            query = select(users_table.c.id).where(users_table.c.username == username)
            result = conn.execute(query)
            try:
                user_id = result.fetchone()[0]
                return user_id
            except TypeError:
                return None

    def insert_strategy(self, user_id, strategy):
        with self.engine.connect() as conn:
            query = insert(strategies_table).values(user_id=user_id, strategy=strategy)
            conn.execute(query)
            conn.commit()

    def get_strategy(self, strategy_id):
        with self.engine.connect() as conn:
            query = select(strategies_table.c.strategy).where(strategies_table.c.id == strategy_id)
            result = conn.execute(query)
            try:
                strategy = result.fetchone()[0]
                return strategy
            except TypeError:
                return None

    def up_to_date_strategy(self, strategy_id, updated_data):
        with self.engine.connect() as conn:
            query = update(strategies_table).where(strategies_table.c.id == strategy_id).values(strategy=updated_data)
            conn.execute(query)
            conn.commit()

    def del_strategy(self, strategy_id):
        with self.engine.connect() as conn:
            query = delete(strategies_table).where(strategies_table.c.id == strategy_id)
            conn.execute(query)
            conn.commit()

    # CRUD operations
    def create_strategy(self, data):
        username = get_jwt_identity()
        user_id = self.get_user_id(username)


        self.insert_strategy(user_id, data)

        message = f"User {user_id} created strategy {data['name']}"
        publish_message("strategy_queue", message)

        self.redis_client.delete(f"strategies_user_{user_id}")

        return jsonify({"message": "Strategy created", "strategy": data}), 201

    def read_strategy(self, strategy_id):
        username = get_jwt_identity()
        user_id = self.get_user_id(username)

        cache_key = f"strategy_user_{user_id}_id_{strategy_id}"
        cached_strategy = self.redis_client.get(cache_key)
        if cached_strategy:
            your_strategy = json.loads(cached_strategy)
        else:
            your_strategy = self.get_strategy(strategy_id)

            self.redis_client.set(cache_key, json.dumps(your_strategy), ex=3600)

        return jsonify({"message": f"Your strategies: {your_strategy}"})

    def update_strategy(self, strategy_id, data):
        username = get_jwt_identity()
        user_id = self.get_user_id(username)

        self.up_to_date_strategy(strategy_id, data)

        self.redis_client.delete(f"strategy_user_{user_id}_id_{strategy_id}")

        message = f"User {user_id} updated strategy {strategy_id}"
        publish_message("strategy_queue", message)

        return jsonify({"message": f"Strategy {strategy_id} was updated!", "strategy": data}), 201

    def delete_strategy(self, strategy_id):
        username = get_jwt_identity()
        user_id = self.get_user_id(username)

        self.del_strategy(strategy_id)

        self.redis_client.delete(f"strategy_user_{user_id}_id_{strategy_id}")

        return jsonify({"message": f"Strategy {strategy_id} deleted"})

    # Basic simulation
    def simulate(self, strategy_id, historical_data):
        strategy = self.get_strategy(strategy_id)

        buy_conditions = strategy.get("buy_conditions", [])
        sell_conditions = strategy.get("sell_conditions", [])

        total_trades = 0
        profit_loss = 0.0
        max_drawdown = 0.0
        current_position = None
        entry_price = 0.0
        highest_equity = 0.0

        for day in historical_data:

            if not current_position and self.evaluate_conditions(buy_conditions, day):
                current_position = "LONG"
                entry_price = day["close"]
                total_trades += 1

            if current_position and self.evaluate_conditions(sell_conditions, day):
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

        win_rate = self.calculate_win_rate(historical_data, buy_conditions, sell_conditions)

        return jsonify({
            "strategy_id": strategy_id,
            "total_trades": total_trades,
            "profit_loss": round(profit_loss, 2),
            "win_rate": round(win_rate, 2),
            "max_drawdown": round(max_drawdown, 2)
        })

    def evaluate_conditions(self, conditions, data):
        indicator = conditions.get("indicator")
        threshold = conditions.get("threshold")

        if indicator == "momentum":
            momentum = (data["close"] - data["open"]) / data["open"] * 100
            return momentum > threshold if threshold > 0 else momentum < threshold

        return False

    def calculate_win_rate(self, historical_data, buy_conditions, sell_conditions):
        wins = 0
        total = 0
        current_position = None
        entry_price = 0.0

        for day in historical_data:
            if not current_position and self.evaluate_conditions(buy_conditions, day):
                current_position = "LONG"
                entry_price = day["close"]

            elif current_position and self.evaluate_conditions(sell_conditions, day):
                total += 1
                if day["close"] > entry_price:
                    wins += 1
                current_position = None

        if total == 0:
            return 0.0

        return (wins / total) * 100