from aiohttp import web

from .models import *

routes = web.RouteTableDef()

@routes.post('/reboot')
async def reboot(request):
    print('Device rebooting.')
    return web.json_response(
            {'success':True},
            status=200
            )

raspi = web.Application()
raspi.add_routes(routes)
