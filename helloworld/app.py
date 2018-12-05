from chalice import Chalice
from chalice import BadRequestError, NotFoundError

app = Chalice(app_name='helloworld')
app.debug = True

CITIES_TO_STATE = {
    'seattle': 'WA',
    'portland': 'OR',
}

OBJECTS = {
}


@app.route('/')
def index():
    return {'hello': 'world', "name": "Vince"}


@app.route('/cities/{city}')
def state_of_city(city):
    try:
        return {'state': CITIES_TO_STATE[city]}
    except KeyError:
        raise BadRequestError("Unknown city '%s', valid choices are: %s" % (
            city, ', '.join(CITIES_TO_STATE.keys())))


@app.route('/resource/{value}', methods=['PUT'])
def put_test(value):
    return {"value": value}


@app.route('/resource/{value}', methods=['POST'])
def post_test(value):
    return {"value": value}


@app.route('/objects/{key}', methods=['GET', 'PUT'])
def myobject(key):
    request = app.current_request
    if request.method == 'PUT':
        OBJECTS[key] = request.json_body
    elif request.method == 'GET':
        try:
            return {key: OBJECTS[key]}
        except KeyError:
            raise NotFoundError(key)
        

@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()



