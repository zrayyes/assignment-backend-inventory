from sanic import Sanic
import os
from sanic.response import text
from config import DevelopmentConfig, ProductionConfig

app = Sanic("StoreBackendApp")

if os.getenv("SANIC_ENV") == "development":
    app.update_config(DevelopmentConfig)
else:
    app.update_config(ProductionConfig)

@app.get("/")
async def hello(request):
    return text("OK!")


if __name__ == "__main__":
    if os.getenv("SANIC_ENV") == "development":
        app.run(dev=True, host="0.0.0.0", port=8000)
    else:
        app.run(host="0.0.0.0", port=8000)
