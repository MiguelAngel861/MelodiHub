from flask import Flask
from .routes import auth_bp, main_bp
from config import Config

def create_app(config = Config) -> Flask:
    app: Flask = Flask(__name__, template_folder = config.TEMPLATE_FOLDER, static_folder = config.STATIC_FOLDER)

    app.config.from_object(config)

    # Registro de Blueprint
    
    app.register_blueprint(main_bp, url_prefix = "/")
    app.register_blueprint(auth_bp, url_prefix = "/auth")

    # Registro de Extensiones

    return app 