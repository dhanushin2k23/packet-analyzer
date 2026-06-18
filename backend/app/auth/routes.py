from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app.database import db


auth = Blueprint(
    "auth",
    __name__
)

@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json(silent=True) or {}


    username = data.get("username")
    email = data.get("email")
    password = data.get("password")


    if not username or not email or not password:
        return jsonify({
            "error": "Missing fields"
        }), 400

    username = username.strip()
    email = email.strip().lower()

    if len(password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters"
        }), 400


    existing_user = User.query.filter_by(
        email=email
    ).first()


    if existing_user:
        return jsonify({
            "error": "User already exists"
        }), 409


    user = User(
        username=username,
        email=email
    )


    user.set_password(password)


    db.session.add(user)
    db.session.commit()


    return jsonify({
        "message": "User created successfully"
    }), 201

@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip().lower()
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Missing credentials"
        }), 400


    user = User.query.filter_by(
        email=email
    ).first()


    if not user:
        return jsonify({
            "error":"Invalid credentials"
        }),401


    if not user.check_password(password):
        return jsonify({
            "error":"Invalid credentials"
        }),401


    token = create_access_token(
        identity=user.id
    )


    return jsonify({
        "access_token":token
    })
