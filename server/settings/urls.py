"""
Gestione Route
"""
from uuid import uuid4
from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, get_jwt_claims, jwt_refresh_token_required, fresh_jwt_required
)
from .config import app, jwt
from ..user import controller as ctl_user


@jwt.user_claims_loader
def add_claims_to_access_token(user: ctl_user.db.UserObj):
    return dict(roles=user.roles,
                sign_package=uuid4())  # Con questo sign_package, posso immaginare di firmare ogni access token?


@jwt.user_identity_loader
def user_identity_lookup(user: ctl_user.db.UserObj):
    return dict(user=user.username, val=user.token_randomize)


@jwt.user_loader_callback_loader
def user_load_callback(identity):
    if identity is None:
        return None
    print(identity)
    print(get_jwt_identity())
    print(get_jwt_claims())
    if identity["user"] == "test" and identity["val"] == "randomize_token":
        return ctl_user.db.UserObj(username="test", roles=["client", "admin"])
    return None


@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    ret = {
        "msg": "User not found"
    }
    return jsonify(ret), 404


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    identity = get_jwt_identity()
    if identity["user"] == "test" and identity["val"] == "randomize_token":
        current_user= ctl_user.db.UserObj(username="test", roles=["client", "admin"])
        print("current",current_user)
        ret = {
            'access_token': create_access_token(identity=current_user,fresh=False)
        }
        return jsonify(ret), 200
    return None


@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    status_code, response = ctl_user.login(**request.json)
    if status_code != 200:
        return jsonify(response), status_code
    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=response,fresh=True)
    response.access_token = access_token
    refresh_token = create_refresh_token(identity=response)
    response.refresh_token = refresh_token
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/protected-fresh', methods=['GET'])
@jwt_required
@fresh_jwt_required
def protected_fresh():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(fresh_logged_in_as=current_user), 200
