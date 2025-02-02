from flask import Flask
from flask_cors import CORS
from routes.sensores_routes import sensor_bp
from routes.lecturas_routes import lecturas_bp
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

swagger = Swagger(app)

app.register_blueprint(sensor_bp, url_prefix = '/sensores')
app.register_blueprint(lecturas_bp, url_prefix = '/lecturas')

@app.route('/')
def home():
    """
    Endpoint de prueba para verificar el estado de la API
    ---
    responses:
      200:
        description: API funcionando correctamente
    """
    return {"mensaje": "API con Flask y SQL Server funcionando correctamente"}

if __name__ == '__main__':
    app.run(debug=True)