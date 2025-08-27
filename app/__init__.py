from flask import Flask

def create_app(config = None) -> Flask:
    app: Flask = Flask(__name__, template_folder = "/views/templates", static_folder = "/views/static/")

    app.config.from_object(config)

    return app