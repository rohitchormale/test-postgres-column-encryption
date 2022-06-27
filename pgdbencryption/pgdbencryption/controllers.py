"""
This module implements webapp controllers.

@author: Rohit Chormale
"""

from flask import request, render_template, jsonify, flash
from .extensions import csrf
from .models import *


def flash_errors(form):
    """Generate flashes for errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


# e.g. controllers
# def register():
#     context = {"title": "home"}
#     return render_template("foo.html", **context)
#
# def register_api():
#     return jsonify({"first_name": "foo"}), 200



def list_users():
    users = [user.as_dict() for user in UserModel.query.all()]
    resp = {"users": users, "count": len(users)}
    return jsonify(resp)


@csrf.exempt
def create_user():
    try:
        data = request.json
        user = UserModel(name=data["name"], password=data["password"], ccdetails=data["ccdetails"], ccdetails2=data["ccdetails"])
        print(user)
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg": "succeed"}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": str(e)}), 500


def get_user():
    user_id = request.args.get("user")
    try:
        user = UserModel.query.get(user_id)
        return jsonify(user.as_dict())
    except Exception as e:
        print(e)
        return jsonify({"msg": str(e)}), 500


@csrf.exempt
def update_user():
    user_id = request.args.get("user")
    data = request.json
    try:
        user = UserModel.query.get(user_id)
        user.password = data.get("password")
        ccdetails = data.get("ccdetails")
        if ccdetails:
            user.ccdetails = ccdetails
            user.ccdetails2 = ccdetails
        db.session.add(user)
        db.session.commit()
        return jsonify(user.as_dict())
    except Exception as e:
        print(e)
        return jsonify({"msg": str(e)}), 500


@csrf.exempt
def delete_user():
    user_id = request.args.get("user")
    try:
        user = UserModel.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "success"}), 200
    except Exception as e:
        print(e)
        return jsonify({"msg": str(e)}), 500