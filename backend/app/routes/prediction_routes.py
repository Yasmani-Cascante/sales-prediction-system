from flask import Blueprint, request, jsonify
from ..services.prediction_service import PredictionService

prediction_bp = Blueprint('predictions', __name__)
prediction_service = PredictionService()

@prediction_bp.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint para generar predicciones de ventas
    Espera un JSON con:
    {
        "branch_name": "nombre_sucursal",
        "periods": 30  // opcional, default 30 días
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'branch_name' not in data:
            return jsonify({
                'error': 'Se requiere branch_name en el cuerpo de la petición'
            }), 400
            
        branch_name = data['branch_name']
        periods = data.get('periods', 30)
        
        # Obtener predicciones
        result = prediction_service.predict(branch_name, periods)
        
        # Obtener métricas de rendimiento del modelo
        performance = prediction_service.get_model_performance(branch_name)
        
        # Combinar resultados
        response = {
            **result,
            'model_performance': performance
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@prediction_bp.route('/performance/<branch_name>', methods=['GET'])
def get_performance(branch_name):
    """Endpoint para obtener métricas de rendimiento del modelo"""
    try:
        performance = prediction_service.get_model_performance(branch_name)
        return jsonify(performance)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500