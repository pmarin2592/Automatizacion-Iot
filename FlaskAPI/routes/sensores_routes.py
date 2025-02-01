from flask import Blueprint, request, jsonify
from services.sensores_services import SensoresService

sensor_bp = Blueprint('sensores', __name__)

@sensor_bp.route('/', methods = ['GET'])
def get_sensores():
    return jsonify(SensoresService.get_all_sensores())