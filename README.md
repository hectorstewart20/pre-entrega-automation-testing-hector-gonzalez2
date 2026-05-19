# Proyecto SauceDemo - pruebas

README breve y sencilla, para que parezca mía.

Qué hay:
- Tests de login, navegación y carrito
- Reporte en `reports/reporte.html`

Instalación rápida:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Ejecutar:
```bash
pytest -v
```

Generar reporte:
```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

Estructura (lo básico):
```

utils/  
conftest.py
requirements.txt
reports/
```

Si algo falla, corre `pytest -v -s` para ver más info.
  - test_navigation.py (navegación, productos, interfaz)
