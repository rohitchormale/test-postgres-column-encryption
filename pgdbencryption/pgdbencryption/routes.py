"""
This module implements routes.

author: Rohit Chormale

"""
from flask import Blueprint
from . import controllers


# e.g blueprint and routes
# auth_blueprint = Blueprint("auth", "auth", url_prefix="/auth")
# auth_blueprint.add_url_rule("register", "register", controllers.register)


user_blueprint = Blueprint("users", "users", url_prefix="/users")
user_blueprint.add_url_rule("list", "/list", controllers.list_users, methods=["GET"])
user_blueprint.add_url_rule("get", "/get", controllers.get_user, methods=["GET"])
user_blueprint.add_url_rule("create", "/create", controllers.create_user, methods=["POST"])
user_blueprint.add_url_rule("update", "/update", controllers.update_user, methods=["PUT"])
user_blueprint.add_url_rule("delete", "/delete", controllers.delete_user, methods=["DELETE"])


