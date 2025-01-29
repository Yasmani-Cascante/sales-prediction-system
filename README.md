# Sistema de Predicción de Ventas

Sistema de predicción de ventas usando Prophet y FastAPI para análisis y pronósticos de ventas en restaurantes.

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
python app.py
```

2. Iniciar el frontend:
```bash
cd frontend
npm run dev
```

## Uso

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Documentación API: http://localhost:5000/docs

## Características

- Predicción de ventas usando Prophet
- Dashboard interactivo con gráficos
- API RESTful con FastAPI
- Documentación automática con Swagger
- Soporte para múltiples sucursales

## Desarrollo

- Backend: FastAPI + Prophet
- Frontend: Next.js + React + Recharts
- Documentación: Swagger/OpenAPI

## API Endpoints

- `GET /`: Mensaje de bienvenida
- `POST /api/predict`: Genera predicciones de ventas
  - Parámetros:
    - `branch_name`: Nombre de la sucursal
    - `periods`: Número de períodos a predecir (default: 30)
    - `frequency`: Frecuencia de predicción (default: "D" para diario)

## Licencia

MIT