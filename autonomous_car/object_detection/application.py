from flask import Flask

# application factory, see: http://flask.pocoo.org/docs/patterns/appfactories/
def create_app():
    app = Flask(__name__)

    # import blueprints
    from src.car.engine import car_engine

    # register blueprints
    app.register_blueprint(car_engine)

    return app