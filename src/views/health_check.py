from sanic.response import json
from sanic.views import HTTPMethodView


class HealthCheckView(HTTPMethodView):
    def get(self, request):
        return json({"status": "success"})
