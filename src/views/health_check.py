from sanic.views import HTTPMethodView
from sanic.response import json


class HealthCheckView(HTTPMethodView):
    def get(self, request):
        return json({"status": "success"})
