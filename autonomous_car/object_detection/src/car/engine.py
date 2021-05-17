from flask import (
    Blueprint, render_template
)
import explorerhat as eh

car_engine_app = Blueprint('car_engine_app', __name__)

@car_engine_app.route("/")
@car_engine_app.route("/<state>")
def update_robot(state=None):
    if state == 'forward':
        eh.motor.one.backwards(100)
        eh.motor.two.forwards(100)
    if state == 'back':
        eh.motor.one.forwards(100)
        eh.motor.two.backwards(100)
    if state == 'left':
        eh.motor.two.stop()
        eh.motor.one.backwards(100)
    if state == 'right':
        eh.motor.one.stop()
        eh.motor.two.forwards(100)
    if state == 'stop':
        eh.motor.one.stop()
        eh.motor.two.stop()
    if state == 'anti-clockwise':
        eh.motor.one.backwards(100)
        eh.motor.two.backwards(100)
    if state == 'clockwise':
        eh.motor.one.forwards(100)
        eh.motor.two.forwards(100)
    template_data = {
        'title': state,
    }
    return render_template('main.html', **template_data)
