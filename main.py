from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from datetime import timedelta

from db import create_tables, settings
from auth import auth
from strategy_crud import strategies

app = Flask(__name__)

app.config['SECRET_KEY'] = settings.get_secret_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(strategies, url_prefix="/strategies")

@app.route("/")
def home():
    return render_template("start.html")

if __name__ == "__main__":
    create_tables()
    app.run(debug=True, port=5000)
