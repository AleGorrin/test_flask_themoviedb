import redis
from flask import Flask, jsonify
from controllers.controllers import movies_blueprint
from settings import config

app = Flask(__name__)

# Configura Redis
redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

# Registrar el Blueprint
app.register_blueprint(movies_blueprint, url_prefix='/')

# Manejador para errores 404
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message": "Page not found"}), 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
