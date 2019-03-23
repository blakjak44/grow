import base64

from aiohttp import web
import aiohttp_cors
from aiohttp_session import setup, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

#import socketio

from cryptography import fernet
from werkzeug.security import generate_password_hash

from .auth import auth, load_logged_in_user
from .provision import prov
from .raspi import raspi

from mongoengine import *
from .models import *

#sio = socketio.AsyncServer()

if __name__ == '__main__':
    app = web.Application()

    # Secret_key must be 32 url-safe base64-encoded bytes
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))

    # Register middleware
    app.middlewares.append(load_logged_in_user)

    # Connect to mongodb
    connect('grow')

    app.add_subapp('/api/auth', auth)
    app.add_subapp('/api/prov', prov)
    app.add_subapp('/api/raspi', raspi)

    #sio.attach(app)

    # Create CORS config
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)

    # Create admin user if it does not exist
    admin = Users.objects(username='admin').first()
    if not admin:
        admin = Users(
                username='admin',
                password=generate_password_hash('admin'),
                email='admin@admin.com'
                )
        admin.save()

    # Initialize device provisioned state
    wifi_network = WifiNetworks.objects.first()
    app['PROVISIONED'] = True if wifi_network else False
    print(f'Provisioned status: {app["PROVISIONED"]}')

    web.run_app(app, port=5000)
