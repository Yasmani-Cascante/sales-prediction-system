# Sistema de Predicción de Ventas

Sistema de predicción de ventas usando scikit-learn (RandomForestRegressor) y FastAPI para análisis y pronósticos de ventas en restaurantes.

## Estructura del Proyecto

```
sales-prediction-system/
├── backend/
│   ├── app/
│   │   ├── models/         # Modelos Pydantic para validación de datos
│   │   ├── routes/         # Rutas de la API
│   │   └── services/       # Lógica de negocio y predicciones
│   ├── requirements.txt    # Dependencias del backend
│   └── app.py             # Punto de entrada del backend
└── frontend/
    ├── app/               # Componentes y páginas Next.js
    ├── components/        # Componentes React reutilizables
    └── package.json       # Dependencias del frontend
```

## Modelo de Predicción

El sistema utiliza RandomForestRegressor de scikit-learn para las predicciones de ventas, incorporando:
- Análisis de tendencias temporales
- Patrones estacionales (diarios, semanales, mensuales)
- Intervalos de confianza basados en la variabilidad del modelo
- Métricas de rendimiento (MAE, MAPE, Accuracy)

## Requisitos

- Python 3.11+
- Node.js 16+
- npm 8+

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/Yasmani-Cascante/sales-prediction-system.git
cd sales-prediction-system
```

2. Configurar el backend:
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # En Windows
pip install -r requirements.txt
```

3. Configurar el frontend:
```bash
cd frontend
npm install
```

## Ejecución

1. Iniciar el backend:
```bash
cd backend
.\venv\Scripts\activate  # En Windows
uvicorn app.main:app --reload
```

2. Iniciar el frontend:
```bash
cd frontend
npm run dev
```

## Uso

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Documentación API: http://localhost:8000/docs

## Características

- Predicción de ventas usando RandomForestRegressor
- Análisis de tendencias y estacionalidad
- Intervalos de confianza para predicciones
- Dashboard interactivo con gráficos
- API RESTful con FastAPI
- Documentación automática con Swagger
- Soporte para múltiples sucursales

## API Endpoints

- `GET /`: Mensaje de bienvenida
- `POST /api/predict`: Genera predicciones de ventas
  - Parámetros:
    - `branch_name`: Nombre de la sucursal
    - `periods`: Número de períodos a predecir (default: 30)
    - `frequency`: Frecuencia de predicción (default: "D" para diario)
  - Respuesta:
    - Predicciones diarias con intervalos de confianza
    - Métricas de rendimiento del modelo
    - Estadísticas de ventas

## Dashboard

El dashboard incluye:
- Selector de sucursales
- Gráfico de predicciones con intervalos de confianza
- Métricas clave:
  - Ventas totales
  - Precisión del modelo
  - Tendencia de ventas
- Visualización responsiva y adaptable

## Tecnologías

- Backend:
  - FastAPI
  - scikit-learn
  - pandas
  - numpy
- Frontend:
  - Next.js
  - React
  - Recharts
  - Tailwind CSS
- Documentación:
  - Swagger/OpenAPI

## Licencia

MIT