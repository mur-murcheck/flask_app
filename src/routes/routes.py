from flask import Blueprint

from src.controllers import health_controller as healthContr

route = Blueprint("api_v2", __name__)

route.route("/healthCheck", methods=["GET"])(healthContr.health_check)
