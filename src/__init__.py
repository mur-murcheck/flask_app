from dotenv import load_dotenv
from flask import Flask, jsonify

from src.configs.config import Config
from src.models.database import close_db
from src.routes.routes import route


def create_app():
  load_dotenv()

  app = Flask(__name__)
  app.config.from_object(Config)

  app.register_blueprint(route, url_prefix="/api/v2")

  app.teardown_appcontext(close_db)

  @app.errorhandler(404)
  def not_found(_error):
    return jsonify({"success": False, "message": "Resource not found"}), 404

  @app.errorhandler(500)
  def internal_error(_error):
    return jsonify({"success": False, "message": "Internal server error"}), 500

  return app
