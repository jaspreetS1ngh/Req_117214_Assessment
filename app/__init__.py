from flask import Flask
from app.mqtt_client import start_mqtt_client

def create_app():
    app = Flask(__name__)

    # Loading configuration from config.py
    app.config.from_object('config.Config') 

    # Start the MQTT client
    start_mqtt_client()

    # Register Blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    app.logger.info("Flask app is starting...")

    return app
