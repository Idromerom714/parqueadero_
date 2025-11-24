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

# 📡 Sistema IoT de Parqueadero

Extensión del sistema de parqueadero que simula dispositivos IoT (cámaras de reconocimiento de placas) comunicándose con el servidor mediante TCP/IP.

## 🎯 Arquitectura

```
┌──────────────────────┐
│  Dispositivo IoT     │  Simula cámara que captura placas
│  (Cliente C++)       │  Envía: ENTRADA|ABC123|carro|CAMARA-01
└──────────┬───────────┘
           │ TCP/IP
           │ Puerto 8080
           ▼
┌──────────────────────┐
│  Servidor C++        │  Recibe eventos y procesa con
│  + Parqueadero Core  │  lógica del parqueadero
└──────────┬───────────┘
           │ pybind11
           ▼
┌──────────────────────┐
│  Python/Flask        │  Interfaz web + Base de datos
│  + Base de Datos     │  Persistencia y reportes
└──────────────────────┘
```

## 🚀 Compilación

### Linux/macOS

```bash
# Compilar todo (módulo Python + cliente)
make

# O por separado
make module   # Solo módulo Python
make cliente  # Solo cliente dispositivo
```

### Windows

```bash
# Con MinGW/MSYS2
make

# O compilación manual del cliente
g++ -O3 -Wall -std=c++11 cliente_dispositivo.cpp cpp/socket_utils.cpp -o cliente_dispositivo.exe -Icpp -lws2_32
```

## 📦 Componentes Nuevos

### 1. `socket_utils.hpp/cpp`
Abstracción multiplataforma para sockets:
- Windows: Winsock2
- Linux/Mac: POSIX sockets

### 2. `servidor_parqueadero.hpp/cpp`
Servidor TCP/IP que:
- Escucha conexiones en puerto 8080
- Recibe mensajes de dispositivos
- Procesa eventos (ENTRADA/SALIDA)
- Notifica a Python mediante callbacks

### 3. `cliente_dispositivo.cpp`
Simulador de dispositivo IoT que:
- Genera placas aleatorias
- Simula detección de entradas/salidas
- Se conecta al servidor vía TCP/IP
- Modo interactivo y automático

### 4. `servidor_iot.py`
Script Python que:
- Crea el servidor C++ desde Python
- Maneja callbacks de eventos
- Guarda en base de datos
- Interfaz de monitoreo

## 🎮 Uso

### Paso 1: Compilar

```bash
make
```

### Paso 2: Iniciar Servidor Python

**Terminal 1:**
```bash
python servidor_iot.py
```

Verás:
```
╔════════════════════════════════════════╗
║  Sistema de Parqueadero IoT            ║
║  Servidor de Dispositivos Remotos      ║
╚════════════════════════════════════════╝

🚀 INICIANDO SERVIDOR IoT
============================================================
✅ Servidor iniciado en puerto 8080
✅ Servidor escuchando en puerto 8080
📡 Esperando dispositivos IoT...
🅿️  Capacidad: 20 carros, 30 motos
============================================================
```

### Paso 3: Ejecutar Cliente (Dispositivo)

**Terminal 2:**

**Modo Interactivo:**
```bash
# Linux/Mac
./cliente_dispositivo

# Windows
cliente_dispositivo.exe
```

Menú:
```
┌─────────────────────────────┐
│  1. Simular ENTRADA         │
│  2. Simular SALIDA          │
│  3. Tráfico automático      │
│  4. Salir                   │
└─────────────────────────────┘
```

**Modo Automático:**
```bash
# Linux/Mac
./cliente_dispositivo CAMARA-01 127.0.0.1 8080 auto 20

# Windows
cliente_dispositivo.exe CAMARA-01 127.0.0.1 8080 auto 20

# O con Make
make run-cliente-auto
```

### Ejemplos de Flujo

**Cliente envía:**
```
ENTRADA|ABC123|carro|CAMARA-01
```

**Servidor procesa y responde:**
```
OK: Vehículo ABC123 registrado en espacio 5
```

**Python recibe evento y guarda en DB:**
```
🔔 EVENTO #1
============================================================
Tipo:     ENTRADA
Placa:    ABC123
Vehículo: carro
Estado:   ✅ ÉXITO
Hora:     2024-01-15 14:30:25
============================================================
```

## 🔧 Protocolo de Comunicación

### Formato de Mensaje

```
TIPO|PLACA|TIPO_VEHICULO|DISPOSITIVO
```

**Campos:**
- `TIPO`: "ENTRADA" o "SALIDA"
- `PLACA`: Placa del vehículo (ej: "ABC123")
- `TIPO_VEHICULO`: "carro" o "moto" (solo para ENTRADA)
- `DISPOSITIVO`: ID del dispositivo (ej: "CAMARA-01")

**Ejemplos:**
```
ENTRADA|ABC123|carro|CAMARA-01
SALIDA|DEF456||CAMARA-02
ENTRADA|GHI789|moto|CAMARA-NORTE
```

### Respuestas del Servidor

**Éxito:**
```
OK: Vehículo ABC123 registrado en espacio 5
OK: Vehículo DEF456 retirado. Tarifa: $6,000
```

**Error:**
```
ERROR: No hay espacios disponibles para carro
ERROR: El vehículo con placa XYZ999 no está en el parqueadero
```

## 📊 Menú Interactivo del Servidor

Mientras el servidor está ejecutando, puedes interactuar:

```
┌─────────────────────────────────┐
│  SERVIDOR IoT - MENÚ            │
├─────────────────────────────────┤
│  1. Mostrar estado              │  → Estado actual del parqueadero
│  2. Listar vehículos            │  → Lista de placas dentro
│  3. Info de vehículo            │  → Detalles de un vehículo
│  4. Estadísticas                │  → Stats de la BD
│  5. Salir                       │  → Detener servidor
└─────────────────────────────────┘
```

## 🌐 Integración con Flask

El servidor IoT es **independiente** de Flask, pero puede usarse junto a él:

**Terminal 1 - Servidor IoT:**
```bash
python servidor_iot.py
```

**Terminal 2 - Cliente Dispositivo:**
```bash
./cliente_dispositivo
```

**Terminal 3 - Flask (opcional):**
```bash
python app.py
```

Esto te permite:
- Dispositivos IoT envían eventos → Servidor C++
- Usuarios web registran manualmente → Flask
- Ambos usan el mismo parqueadero
- Todo se guarda en la misma BD

## 🔒 Seguridad

⚠️ **IMPORTANTE:** Este es un **sistema de demostración**.

Para producción necesitas:
- ✅ Autenticación de dispositivos
- ✅ Encriptación TLS/SSL
- ✅ Validación de mensajes
- ✅ Rate limiting
- ✅ Logs de auditoría
- ✅ Manejo de reconexiones

## 🧪 Testing

### Test del Módulo
```bash
make test
```

### Test del Cliente
```bash
# Modo auto con 5 eventos
./cliente_dispositivo CAMARA-TEST 127.0.0.1 8080 auto 5
```

### Test Completo
```bash
# Terminal 1
python servidor_iot.py

# Terminal 2 (esperar 2 segundos)
make run-cliente-auto
```

## 🐛 Troubleshooting

### Error: "Address already in use"
**Causa:** Puerto 8080 ocupado

**Solución:**
```bash
# Linux/Mac
lsof -ti:8080 | xargs kill -9

# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

### Error: "Connection refused"
**Causa:** Servidor no está ejecutando

**Solución:** Inicia el servidor primero

### Error: Winsock no funciona (Windows)
**Causa:** Falta librería ws2_32

**Solución:** Asegúrate de compilar con `-lws2_32`

## 📈 Casos de Uso

### 1. Sistema Real de Parqueadero
- Cámaras OCR en entradas/salidas
- Reconocimiento automático de placas
- Procesamiento centralizado

### 2. Testing y Desarrollo
- Simular múltiples dispositivos
- Probar carga del sistema
- Validar lógica de negocio

### 3. Demostración
- Mostrar sistema funcionando
- Presentaciones
- Pruebas de concepto

## 🔗 Ver También

- [README.md](README.md) - Documentación principal
- [Wiki - CPP Library](../../wiki/CPP-Library) - Detalles de la librería C++
- [Wiki - Simulator](../../wiki/Simulator) - Simulador Python original

## 💡 Próximas Mejoras

- [ ] Múltiples clientes simultáneos (threading)
- [ ] Autenticación de dispositivos
- [ ] Encriptación de mensajes
- [ ] Reconexión automática
- [ ] Dashboard web en tiempo real
- [ ] Soporte para imágenes de placas
- [ ] Configuración por archivo
- [ ] Logs estructurados