import importlib
import json
import traceback

from sqlalchemy.exc import SQLAlchemyError

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES


def load_handler(route):
    route_parts = route.split('/')
    filename = route_parts[-1]
    handler_name = route.replace("/", "_")
    handler_name = ''.join(
        [word.capitalize() if index > 0 else word for index, word in enumerate(handler_name.split('_'))])
    package_format = '.'.join(route_parts)
    module_name = 'backend.web.handlers.api.' + package_format + "." + filename
    handler_name = handler_name[0].upper() + handler_name[1:] + 'Handler'
    try:
        handler_module = importlib.import_module(module_name)
        handler_class = getattr(handler_module, handler_name)
        return handler_class
    except Exception as e:
        # Handle import or attribute errors
        return None


class RequestDispatcher:
    def __init__(self):
        self.routes = {}

    def add_route(self, route, handler):
        self.routes[route] = handler

    def dispatch_request(self, route, request) -> dict:
        handler_class = load_handler(route)
        if handler_class:
            handler_instance = handler_class(Authenticator())
            try:
                return handler_instance.handle_request(request)
            except SQLAlchemyError as e:
                return {'message': str(e)}
            except Exception as e:
                tb = traceback.TracebackException.from_exception(e)
                trace_info = ''.join(tb.format())
                error_details = {
                    'exception': str(e),
                    'trace': trace_info
                }
                return MESSAGES['AUTHENTICATION']['CUSTOM_MESSAGE'](
                    f'Error processing request for route: {route}',
                    error_details
                )
        else:
            return self.handle_not_found(route)

    def handle_not_found(self, route):
        return MESSAGES['AUTHENTICATION']['CUSTOM_MESSAGE']('error', f'Route {route} not found')

    def add_routes_from_json(self, json_file):

        with open(json_file, 'r') as f:
            data = json.load(f)
            base = data.get('base', '')
            self._add_routes(base, data)

    def _add_routes(self, base, data):
        routes = data.get('routes', [])
        for route in routes:
            self.add_route(base + route, None)

        for group, group_data in data.items():
            if group not in ['base', 'routes']:
                group_base = base + '/' + group
                self._add_routes(group_base, group_data)

    def snake_case(self, name):
        """
        Convert CamelCase to snake_case.
        """
        return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')
