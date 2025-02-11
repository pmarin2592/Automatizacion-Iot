from flask import Blueprint, request, jsonify
from flasgger import swag_from
from services.lecturas_services import LecturasService

# Definición del Blueprint para las rutas de lecturas
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
    """
    Endpoint para registrar una nueva lectura de sensor.

    Recibe un JSON con los datos de la lectura y la almacena en la base de datos.
    
    Parámetros:
    - tipoSensor (str): Tipo de sensor (Ejemplo: 'Temperatura').
    - fechaHora (str): Fecha y hora de la lectura (Formato: ISO 8601).

    Retorna:
    - JSON con mensaje de éxito o error en caso de datos faltantes.
    """
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
    """
    Endpoint para obtener las lecturas de un sensor en los últimos 3 minutos.

    Parámetros:
    - id (int): Identificador del sensor a consultar.

    Retorna:
    - JSON con los datos de las lecturas del sensor especificado.
    """
    return jsonify(LecturasService.obtener_lecturas_sensor(id))

@lecturas_bp.route('/consultaSensores/<string:fecInicio>/<string:fecFin>',methods = ['GET'])
@swag_from({
    'summary': 'Consultar 3 minutos de lectura de sensor',
    'description': 'Este endpoint consulta  las lecturas de todolos sensores en un rango de fechas.',
    'parameters': [
        {
            'name': 'fecInicio',
            'in': 'path',
            'required': True,
            'type': 'string'
        },
         {
            'name': 'fecFin',
            'in': 'path',
            'required': True,
            'type': 'string'
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
def obtener_lecturas_sensor_fechas(fecInicio, fecFin):
    """
        Obtiene las lecturas de todolos sensores en un rango de fechas.

        Parámetros:
        - fec_inicio (date): fecha de incio 
        - fec_fin (date): fecha de fin 

        Retorna:
        - list[dict]: Lista de lecturas en formato de diccionario o mensaje de error.
    """
    return jsonify(LecturasService.obtener_lecturas_sensor_fechas(fecInicio, fecFin))