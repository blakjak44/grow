from aiohttp import web

from werkzeug.security import generate_password_hash

from .models import *

routes = web.RouteTableDef()

@routes.post('/add')
async def add(request):
    user = request['user']
    body = await request.json()
    ssid = body['credentials']['ssid']
    password = body['credentials']['password']
    errors = []

    if not ssid:
        errors.append('SSID is required.')
    if not password:
        errors.append('Password is required.')
    if WifiNetworks.objects(ssid=ssid).first() is not None:
        errors.append(f'SSID is already a known network: {ssid}')

    if not len(errors):
        wifi_network = WifiNetworks(
                ssid=ssid,
                password=generate_password_hash(password),
                )
        try:
            wifi_network.save()
        except ValidationError as e:
            for v in e.to_dict().values():
                errors.append(v)
            return web.json_response(
                    {'success': False, 'errors': errors},
                    status=401
                    )
        message = f'Successfully registered new network: {ssid}'
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

@routes.put('/set')
async def set(request):
    pass

prov = web.Application()
prov.add_routes(routes)
