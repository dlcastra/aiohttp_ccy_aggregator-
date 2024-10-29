from aiohttp import web

from core.settings import service
from app.handlers import handle_get_rate

service.add_routes([
    web.post('/rate', handle_get_rate),

])

if __name__ == '__main__':
    web.run_app(service)
