from flask import Blueprint, request, jsonify
from services.sensores_services import SensoresService
from flasgger import swag_from

sensor_bp = Blueprint('sensores', __name__)

@sensor_bp.route('/', methods = ['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Lista de sensores obtenida exitosamente',
            'examples': {
                'application/json': {"sensores": ["sensor1", "sensor2"]}
            }
        }
    }
})
def get_sensores():
    return jsonify(SensoresService.get_all_sensores())