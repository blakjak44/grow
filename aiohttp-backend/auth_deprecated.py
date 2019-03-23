import functools

import json
from flask import (
    Blueprint, g, request, session, jsonify
)

from werkzeug.security import check_password_hash, generate_password_hash

from mongoengine.errors import ValidationError
from .models import *

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    username = request.get_json()['credentials']['username'].lower() # Ensure username is all lowercase
    password = request.get_json()['credentials']['password']
    email = request.get_json()['credentials']['email']
    errors = []

    if not username:
        errors.append('Username is required.')
    if not password:
        errors.append('Password is required.')
    if not email:
        errors.append('Email is required.')
    if Users.objects(username=username).first() is not None:
        errors.append(f'User is already registered: {username}')

    if not len(errors):
        user = Users(
                username=username,
                password=generate_password_hash(password),
                email=email
                )
        try:
            user.save()
        except ValidationError as e:
            for v in e.to_dict().values():
                errors.append(v)
            return jsonify(success=False, errors=errors), 401
        session.clear()
        session['user_id'] = str(user.id)
        message = f'Successfully registered: {user.username}'
        return jsonify(success=True, message=message, user={'user_id': str(user.id), 'username': user.username}), 201

    return jsonify(success=False, errors=errors), 401

@bp.route('/login', methods=['POST'])
def login():
    username = request.get_json()['credentials']['username'].lower()
    password = request.get_json()['credentials']['password']
    errors = []

    user = Users.objects(username=username).first()

    if user is None:
        errors.append('Incorrect username/password combination.')
    elif not check_password_hash(user['password'], password):
        errors.append('Incorrect username/password combination.')

    if not len(errors):
        session.clear()
        session['user_id'] = str(user.id)
        message = f'Successfully logged in as user: {user.username}'
        return jsonify(success=True, message=message, user={'user_id': str(user.id), 'username': user.username}), 200

    return jsonify(success=False, errors=errors), 401

@bp.route('/logout', methods=['GET'])
def logout():
    username = g.user.username
    session.clear()
    message = f'Successfully logged out user: {username}'
    return jsonify(success=True, message=message), 200

@bp.route('/validate', methods=['POST'])
def validate():
    user = g.user
    if user is None:
        errors = ['Unauthorized.']
        return jsonify(success=False, errors=errors), 401
    message = 'Authenticated.'
    return jsonify(success=True, message=message, user={'user_id': str(user.id), 'username': user.username}), 200

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = Users.objects(id=user_id).first()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            errors = ['Unauthorized.']
            return jsonify(success=False, error=error), 401

        return view(**kwargs)

    return wrapped_view
