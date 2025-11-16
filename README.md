# parqueadero_
# Sistema de Parqueadero
## Backend en C++ + Frontend en Python/Flask

### Requisitos
```bash
# Python 3.7+
python3 --version

# Compilador C++
g++ --version

# pip
pip --version
```

### Instalación

#### 1. Instalar dependencias de Python
```bash
pip install flask pybind11
```

#### 2. Estructura de carpetas
Crea la siguiente estructura:
```
parqueadero/
├── cpp/
│   ├── parqueadero.hpp
│   ├── parqueadero.cpp
│   └── bindings.cpp
├── templates/
│   └── index.html
├── app.py
├── Makefile
└── setup.py
```

#### 3. Compilar el módulo C++

**Opción A: Usando Makefile (recomendado)**
```bash
make
```

**Opción B: Usando setup.py**
```bash
python setup.py build_ext --inplace
```

**Opción C: Compilación manual**
```bash
g++ -O3 -Wall -shared -std=c++11 -fPIC \
  $(python3 -m pybind11 --includes) \
  -Icpp \
  cpp/parqueadero.cpp cpp/bindings.cpp \
  -o parqueadero_cpp$(python3-config --extension-suffix)
```

### Ejecutar la aplicación

```bash
# Con Makefile
make run

# O directamente
python app.py
```

Abre tu navegador en: **http://localhost:5000**

### Características

✅ **Backend en C++:**
- Gestión de espacios de parqueadero
- Cálculo de tarifas por hora
- Control de entrada/salida de vehículos
- Alto rendimiento

✅ **Frontend en Python/Flask:**
- Interfaz web responsive
- Actualización en tiempo real
- API RESTful

### API Endpoints

- `GET /api/estado` - Estado del parqueadero
- `POST /api/entrada` - Registrar entrada
- `POST /api/salida` - Registrar salida
- `GET /api/vehiculo/<placa>` - Info del vehículo
- `GET /api/tarifa/<placa>` - Calcular tarifa

### Tarifas
- **Carros:** $3,000/hora
- **Motos:** $2,000/hora

### Capacidad
- **Carros:** 20 espacios
- **Motos:** 30 espacios

### Personalización

Para cambiar capacidad o tarifas, edita en `app.py`:
```python
parqueadero = parqueadero_cpp.Parqueadero(
    cap_carros=20,      # Espacios para carros
    cap_motos=30,       # Espacios para motos
    tarifa_carro=3000,  # Tarifa por hora
    tarifa_moto=2000    # Tarifa por hora
)
```

### Agregar persistencia con SQLite

Si quieres guardar el historial en base de datos, agrega:

```python
import sqlite3

# En app.py, después de crear el parqueadero
conn = sqlite3.connect('parqueadero.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS historial (
        id INTEGER PRIMARY KEY,
        placa TEXT,
        tipo TEXT,
        hora_entrada TEXT,
        hora_salida TEXT,
        tarifa REAL
    )
''')
conn.commit()
```

### Solución de problemas

**Error: "No module named 'parqueadero_cpp'"**
- Verifica que la compilación fue exitosa
- Ejecuta `make test`

**Error al compilar:**
- Verifica que tienes g++ instalado
- Instala build-essential: `sudo apt install build-essential`

**Puerto 5000 ocupado:**
- Cambia el puerto en app.py: `app.run(debug=True, port=8000)`