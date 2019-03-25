from aiohttp import web

from threading import Timer

from .models import *
from .utils.raspi_provision import networking

from .auth import login_required

routes = web.RouteTableDef()

@login_required
@routes.post('/add')
async def add(request):
    """
    Adds a new WiFi configuration to database. Needs to be set to active to use.
    """
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
                password=password,
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

@routes.post('/set')
async def set(request):
    """
    Sets active wifi credentials. Requires reboot to activate.
    """
    body = await request.json()
    ssid = body.get('ssid')
    wifi_network_old = WifiNetworks.objects(active=True).first()
    wifi_network_new = WifiNetworks.objects(ssid=ssid).first()

    if wifi_network_new:
        success = networking.set_wifi(wifi_network_new.ssid, wifi_network_new.password)
        wifi_network_new.active = True
        wifi_network_new.save()
        if wifi_network_old:
            wifi_network_old.active = False
            wifi_network_old.save()
        return web.json_response(
                {
                 'success': True,
                 'message': f'WiFi network "{ssid}" now set. Reboot to connect.'
                },
                status=200
                )
    else:
        return web.json_response(
                {'success': False, 'errors': [f'Unkown WiFi network: {ssid}']},
                status=400
                )

@routes.post('/switch')
async def switch_mode(request):
    """
    Switches AP mode.
    """
    body = await request.json()
    active = body.get('active')
    success = await networking.switch_AP_mode(active)
    state = 'enabled' if active else 'disabled'
    return web.json_response(
            {
             'success': True,
             'message': f'AP mode {state}. Reboot now.'
            },
            status=200
            )

@routes.get('/reboot')
async def reboot(request):
    """
    Reboots device.
    """
    t = Timer(3, networking.reboot)
    t.start()
    return web.json_response(
            {
             'success': True,
             'message': 'System will now reboot.'
            },
            status=200
            )

prov = web.Application()
prov.add_routes(routes)
