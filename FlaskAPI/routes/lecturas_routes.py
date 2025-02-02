from flask import Blueprint, request, jsonify
from flasgger import swag_from
from services.lecturas_services import LecturasService

lecturas_bp = Blueprint('lecturas',__name__)

@lecturas_bp.route('/registro',methods = ['POST'])
@swag_from({
    'summary': 'Registrar una nueva lectura de sensor',
    'description': 'Este endpoint registra una nueva lectura de un sensor en la base de datos.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'tipoSensor': {'type': 'string', 'example': 'Temperatura'},
                    'fechaHora': {'type': 'string', 'format': 'date-time', 'example': '2024-02-01T12:00:00'}
                },
                'required': ['tipoSensor', 'fechaHora']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Registro de lectura exitoso',
            'schema': {
                'type': 'object',
                'properties': {
                    'mensaje': {'type': 'string', 'example': 'Registro de lectura exitoso'}
                }
            }
        },
        400: {
            'description': 'Solicitud incorrecta',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Datos faltantes'}
                }
            }
        }
    }
})

def registro_lectura():
    data = request.json
    if not data or 'tipoSensor' not in data or 'fechaHora' not in data:
        return jsonify({"error": "Datos faltantes"}), 400
    return jsonify(LecturasService.registro_lectura(data["tipoSensor"],data["fechaHora"]))

@lecturas_bp.route('/consulta/<int:id>',methods = ['GET'])
@swag_from({
    'summary': 'Consultar 3 minutos de lectura de sensor',
    'description': 'Este endpoint consulta los últimos 3 minutos de lectura de un sensor en la base de datos.',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'example': 1
        }
    ],
    'responses': {
        200: {
            'description': 'Consulta de lectura exitosa',
            'schema': {
                'type': 'object',
                'properties': {
                    'mensaje': {'type': 'string', 'example': 'Consulta de lectura exitoso'}
                }
            }
        },
        400: {
            'description': 'Solicitud incorrecta',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Datos faltantes'}
                }
            }
        }
    }
})
def obtener_lecturas_sensor(id):
    return jsonify(LecturasService.obtener_lecturas_sensor(id))