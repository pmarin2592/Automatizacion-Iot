from flask import Blueprint, request, jsonify
from services.sensores_services import SensoresService
from flasgger import swag_from

# Definición del Blueprint para las rutas de sensores
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
    """
    Endpoint para obtener la lista de sensores disponibles.

    Retorna:
    - JSON con un listado de sensores disponibles en la base de datos.
    """
    return jsonify(SensoresService.get_all_sensores())