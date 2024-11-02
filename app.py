import redis
from flask import Flask
from controllers.controllers import movies_blueprint
from settings import config

app = Flask(__name__)

# Configura Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Registrar el Blueprint
app.register_blueprint(movies_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
