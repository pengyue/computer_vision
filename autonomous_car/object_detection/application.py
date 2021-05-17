from flask import Flask

# application factory, see: http://flask.pocoo.org/docs/patterns/appfactories/
def create_app():
    app = Flask(__name__)

    # import blueprints
    #from src.car.engine import car_engine_app
    from src.tracking.openvino.openvino import openvino_tracking_app

    # register blueprints
    #app.register_blueprint(car_engine_app)
    app.register_blueprint(openvino_tracking_app)

    return app