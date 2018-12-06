import sys
import json
import boto3
from botocore.exceptions import ClientError
from chalice import Chalice, Response, CORSConfig
from chalice import BadRequestError, NotFoundError

if sys.version_info[0] == 3:
    # Python 3 imports.
    from urllib.parse import urlparse, parse_qs
else:
    # Python 2 imports.
    from urlparse import urlparse, parse_qs

app = Chalice(app_name='helloworld')
app.debug = True

S3 = boto3.client('s3', region_name='us-east-2')
BUCKET = 'testbucketvbloise3'

CITIES_TO_STATE = {
    'seattle': 'WA',
    'portland': 'OR',
}

OBJECTS = {
}

cors_config = CORSConfig(
    allow_origin='https://foo.example.com',
    allow_headers=['X-Special-Header'],
    max_age=600,
    expose_headers=['X-Special-Header'],
    allow_credentials=True
)


#@app.route('/')
#def index():
#    return {'hello': 'world', "name": "Vince"}


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
def s3objects(key):
    request = app.current_request
    if request.method == 'PUT':
        S3.put_object(Bucket=BUCKET, Key=key,
                      Body=json.dumps(request.json_body))
    elif request.method == 'GET':
        try:
            response = S3.get_object(Bucket=BUCKET, Key=key)
            return json.loads(response['Body'].read())
        except ClientError as e:
            raise NotFoundError(key)


@app.route('/introspect')
def introspect():
    return app.current_request.to_dict()


@app.route('/', methods=['POST', 'GET'],
           content_types=['application/x-www-form-urlencoded', 'application/json'])
def index():
    request = app.current_request
    if request.method == 'POST':
        parsed = parse_qs(app.current_request.raw_body.decode())
        return {
            'states': parsed.get('states', [])
        }
    elif request.method == 'GET':
        return Response(body='hello world!',
                        status_code=200,
                        headers={'Content-Type': 'text/plain'})


@app.route('/supports-cors', methods=['PUT'], cors=True)
def supports_cors():
    return {'CORS': 'SUPPORTED', "name": "Vince"}


@app.route('/custom_cors', methods=['GET'], cors=cors_config)
def supports_custom_cors():
    return {'cors': True}



