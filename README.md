# Sistema de Predicción de Ventas

Sistema de predicción de ventas usando Prophet para análisis y pronósticos de ventas en restaurantes.

## Estructura del Proyecto

```
├── backend/           # API y lógica de predicción
├── frontend/          # Interfaz de usuario React
└── docs/              # Documentación
```

## Requisitos

- Python 3.8+
- Node.js 16+
- Prophet
- React

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
source venv/bin/activate  # En Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Configurar el frontend:
```bash
cd frontend
npm install
```

## Uso

1. Iniciar el backend:
```bash
cd backend
python app.py
```

2. Iniciar el frontend:
```bash
cd frontend
npm run dev
```

## Licencia

MIT