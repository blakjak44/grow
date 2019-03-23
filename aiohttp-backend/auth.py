from aiohttp import web
import aiohttp_cors
from aiohttp_session import get_session

from werkzeug.security import check_password_hash, generate_password_hash

from mongoengine.errors import ValidationError
from .models import *

routes = web.RouteTableDef()

@routes.post('/register')
async def register(request):
    session = await get_session(request)
    body = await request.json()
    username = body['credentials']['username'].lower() # Ensure username is all lowercase
    password = body['credentials']['password']
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
            return web.json_response(
                    {'success': False, 'errors': errors},
                    status=401
                    )
        session.clear()
        session['user_id'] = str(user.id)
        message = f'Successfully registered: {user.username}'
        return web.json_response(
                {
                 'success': True,
                 'message': message,
                 'user': {'user_id': str(user.id), 'username': user.username}
                },
                status=201
                )

    return web.json_response(
            {'success': False, 'errors': errors},
            status=401
            )

@routes.post('/login')
async def login(request):
    session = await get_session(request)
    body = await request.json()
    username = body['credentials']['username'].lower()
    password = body['credentials']['password']
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
        return web.json_response(
                {
                 'success': True,
                 'message': message,
                 'user': {'user_id': str(user.id), 'username': user.username},
                 'device_provisioned': request.config_dict['PROVISIONED']
                },
                status=200
                )

    return web.json_response(
            {'success': False, 'errors': errors},
            status=401
            )

@routes.get('/logout')
async def logout(request):
    session = await get_session(request)
    username = request['user'].username
    session.invalidate()
    message = f'Successfully logged out user: {username}'

    return web.json_response(
            {'success': True, 'message': message},
            status=200
            )

@routes.post('/validate')
async def validate(request):
    user = request['user']
    if user is None:
        errors = ['Unauthorized.']

        return web.json_response(
                {'success': False, 'errors': errors},
                status=401

                )

    message = 'Authenticated.'
    return web.json_response(
            {
             'success': True,
             'message': message,
             'user': {'user_id': str(user.id), 'username': user.username}
            },
            status=200
            )

@web.middleware
async def load_logged_in_user(request, handler):
    session = await get_session(request)
    user_id = session.get('user_id')
    if user_id is None:
        request['user'] = None
    else:
        request['user'] = Users.objects(id=user_id).first()

    return await handler(request)

def login_required(view):
    async def wrapped_view(request, *args, **kwargs):
        if request['user'] is None:
            errors = ['Unauthorized.']
            return web.json_response(
                    {'success': False, 'error': error},
                    status=401
                    )

        return await view(request, *args, **kwargs)

    return wrapped_view


auth = web.Application()
auth.add_routes(routes)
