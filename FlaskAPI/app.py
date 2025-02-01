from flask import Flask
from flask_cors import CORS
from routes.sensores_routes import sensor_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(sensor_bp, url_prefix = '/sensores')

@app.route('/')
def home():
    return {"mensaje": "API con Flask y SQL Server funcionando correctamente"}

if __name__ == '__main__':
    app.run(debug=True)