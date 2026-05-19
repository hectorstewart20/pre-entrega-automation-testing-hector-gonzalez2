# Automatización de Pruebas - SauceDemo

## 📋 Propósito del Proyecto

Este proyecto implementa una suite de pruebas automatizadas para el sitio de demostración **SauceDemo** (https://www.saucedemo.com). El objetivo es validar las funcionalidades principales de la aplicación mediante automatización web, incluyendo:

- ✅ Automatización de login con credenciales válidas
- ✅ Validación de navegación y catálogo de productos
- ✅ Interacción con el carrito de compras
- ✅ Generación de reportes HTML de ejecución

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **Python** | 3.13+ | Lenguaje de programación |
| **Pytest** | 7.4.3+ | Framework de testing y ejecución de pruebas |
| **Selenium WebDriver** | 4.x+ | Automatización de navegador web |
| **pytest-html** | 4.1.1+ | Generación de reportes HTML |
| **Git** | Latest | Control de versiones |
| **GitHub** | - | Repositorio remoto |

## 📁 Estructura del Proyecto

```
DemoPytest/
├── conftest.py                 # Configuración de pytest y fixtures globales
├── README.md                   # Este archivo (documentación)
├── requirements.txt            # Dependencias del proyecto
├── .gitignore                  # Archivos a ignorar en Git
├── .git/                       # Repositorio Git local
│
├── tests/                      # Directorio de pruebas
│   ├── __init__.py
│   ├── test_login.py           # Pruebas de autenticación
│   ├── test_navigation.py      # Pruebas de navegación y catálogo
│   ├── test_cart.py            # Pruebas del carrito de compras
│   └── __pycache__/
│
├── utils/                      # Funciones auxiliares y utilidades
│   ├── __init__.py
│   └── saucedemo_pages.py      # Clases y selectores de elementos (POM)
│
├── datos/                      # Datos externos (si aplica)
│   └── (para archivos CSV/JSON con datos de prueba)
│
└── reports/                    # Reportes de pruebas
    ├── reporte.html            # Reporte HTML generado por pytest
    └── (capturas de pantalla en caso de fallos)
```

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.11 o superior
- Git instalado
- Navegador Google Chrome (versión compatible)

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/[tu-usuario]/pre-entrega-automation-testing-[nombre-apellido].git
cd pre-entrega-automation-testing-[nombre-apellido]
```

### Paso 2: Crear Entorno Virtual (Recomendado)
```bash
# En Windows
python -m venv .venv
.venv\Scripts\activate

# En macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

## 📦 Dependencias

El proyecto requiere los siguientes paquetes (incluidos en `requirements.txt`):

- `selenium>=4.0.0` - WebDriver para automatización web
- `pytest>=7.4.0` - Framework de testing
- `pytest-html>=4.1.0` - Plugin para reportes HTML
- `webdriver-manager>=4.0.0` - Gestión automática de drivers
- `python-dotenv>=1.0.0` - Carga de variables de entorno

## 🧪 Ejecución de Pruebas

### Ejecutar Todas las Pruebas
```bash
pytest -v
```

### Ejecutar Pruebas con Reporte HTML
```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

### Ejecutar Solo Pruebas de Login
```bash
pytest tests/test_login.py -v
```

### Ejecutar Solo Pruebas de Navegación
```bash
pytest tests/test_navigation.py -v
```

### Ejecutar Solo Pruebas del Carrito
```bash
pytest tests/test_cart.py -v
```

### Modo Verbose (Salida Detallada)
```bash
pytest -v -s
```

### Mostrar Print Statements
```bash
pytest -v -s --capture=no
```

## 📊 Generación de Reportes

### Reporte HTML Automático
Después de ejecutar las pruebas con el comando anterior, se genera un archivo `reporte.html` en la carpeta `reports/`.

Para abrir el reporte:
```bash
# Windows
start reports/reporte.html

# macOS
open reports/reporte.html

# Linux
xdg-open reports/reporte.html
```

### Contenido del Reporte HTML
- Resumen general de ejecución (Passed/Failed/Skipped)
- Detalles de cada prueba
- Duración de ejecución
- Stack traces de fallos
- Metadatos de sistema

## 🧬 Casos de Prueba Implementados

### 1. **Automatización de Login** 
**Archivo:** `tests/test_login.py`

#### Caso 1.1: Login Exitoso
- ✅ Navega a https://www.saucedemo.com
- ✅ Ingresa usuario: `standard_user`
- ✅ Ingresa contraseña: `secret_sauce`
- ✅ Valida redirección a página de inventario

#### Caso 1.2: Login con Credenciales Inválidas
- ✅ Intenta login con contraseña incorrecta
- ✅ Valida que aparezca mensaje de error

#### Caso 1.3: Login sin Ingresar Usuario
- ✅ Intenta login sin ingresar usuario
- ✅ Valida que aparezca mensaje de error específico

### 2. **Navegación y Verificación del Catálogo**
**Archivo:** `tests/test_navigation.py`

#### Caso 2.1: Validar Carga de Página de Inventario
- ✅ Verifica que el título de la página sea correcto
- ✅ Valida que la URL sea la esperada

#### Caso 2.2: Verificar Productos Visibles
- ✅ Confirma que existen productos en el catálogo
- ✅ Valida que al menos un producto sea visible
- ✅ Verifica acceso a detalles del producto

#### Caso 2.3: Validar Elementos Importantes de la Interfaz
- ✅ Verifica presencia del menú de usuario
- ✅ Valida que existan opciones de filtro
- ✅ Confirma que el carrito es accesible

### 3. **Interacción con Productos y Carrito**
**Archivo:** `tests/test_cart.py`

#### Caso 3.1: Agregar Producto al Carrito
- ✅ Hace clic en botón "Add to cart"
- ✅ Verifica que el contador se incremente
- ✅ Valida que aparezca el badge del carrito

#### Caso 3.2: Navegar al Carrito
- ✅ Accede al carrito de compras
- ✅ Verifica que los productos agregados aparezcan

#### Caso 3.3: Flujo Completo (Login → Carrito → Logout)
- ✅ Realiza login
- ✅ Agrega producto al carrito
- ✅ Navega al carrito
- ✅ Verifica el producto
- ✅ Realiza logout

## 🔍 Organización del Código

### Buenas Prácticas Implementadas

1. **Separación de Responsabilidades**
   - `conftest.py`: Configuración y fixtures de pytest
   - `tests/*.py`: Casos de prueba organizados por funcionalidad
   - `utils/`: Funciones auxiliares y utilitarios

2. **Nombres Significativos**
   - Métodos de prueba describen claramente qué validan
   - Variables tienen nombres auto-explicativos
   - Clases agrupan pruebas por contexto

3. **Comentarios Descriptivos**
   - Cada test incluye docstring explicativo
   - Comentarios inline en secciones complejas
   - Pasos numerados en la lógica de pruebas

4. **Independencia de Tests**
   - Cada prueba es independiente
   - No hay dependencias entre tests
   - Fallo de una prueba no afecta a las demás

## 📝 Control de Versiones

### Estructura de Commits

```bash
# Ver historial de cambios
git log --oneline

# Ver cambios pendientes
git status

# Ver diferencias
git diff
```

### Realizar Commits Descriptivos

```bash
# Agregar cambios
git add .

# Crear commit con mensaje descriptivo
git commit -m "feat: Agregar casos de prueba de login"
git commit -m "fix: Corregir esperas en carrito"
git commit -m "docs: Actualizar README con instrucciones"
git commit -m "refactor: Mejorar selectores en tests"
```

### Subir a GitHub

```bash
# Primera vez (configurar rama upstream)
git push -u origin main

# Siguientes veces
git push
```

## ✅ Funcionalidades Esperadas

- [x] Los casos de prueba se ejecutan correctamente en saucedemo.com
- [x] Las validaciones son claras y específicas para cada paso
- [x] El código es legible y está bien organizado
- [x] Los tests son independientes entre sí
- [x] Se genera reporte HTML con resultados
- [x] Repositorio en GitHub con commits descriptivos
- [x] README.md con instrucciones completas

## 🐛 Solución de Problemas

### Problema: "No tests ran"
**Solución:** Verificar que los archivos de test estén en la carpeta `tests/` y comiencen con `test_`.

### Problema: "WebDriver not found"
**Solución:** El proyecto usa Selenium Manager que descarga automáticamente el driver. Si falla, reinstalar:
```bash
pip install --upgrade webdriver-manager selenium
```

### Problema: Tests lentos o timeout
**Solución:** Aumentar timeout en `conftest.py`:
```python
WebDriverWait(driver, 15)  # Cambiar de 10 a 15 segundos
```

### Problema: Chrome muestra popups
**Solución:** ChromeOptions ya incluye flags para deshabilitar popups, notificaciones y password manager.

## 📞 Contacto y Soporte

Para reportar problemas o sugerencias, crea un "Issue" en el repositorio de GitHub.

## 📄 Licencia

Proyecto de demostración para fines educativos.

---

**Última actualización:** Mayo 2026  
**Estado:** ✅ Listo para entregar
