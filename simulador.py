import random
import time
import parqueadero_cpp

# Lista de placas disponibles para simular
PLACAS_DISPONIBLES = [
    'ABC123', 'DEF456', 'GHI789', 'JKL012', 'MNO345',
    'PQR678', 'STU901', 'VWX234', 'YZA567', 'BCD890',
    'EFG123', 'HIJ456', 'KLM789', 'NOP012', 'QRS345',
    'TUV678', 'WXY901', 'ZAB234', 'CDE567', 'FGH890'
]

class SimuladorParqueadero:
    def __init__(self, parqueadero):
        self.parqueadero = parqueadero
        self.placas_disponibles = PLACAS_DISPONIBLES.copy()
        self.estadisticas = {
            'entradas_exitosas': 0,
            'entradas_rechazadas': 0,
            'salidas_exitosas': 0,
            'salidas_rechazadas': 0,
            'total_recaudado': 0
        }
    
    def obtener_placa_disponible(self):
        """Obtiene una placa que NO esté en el parqueadero"""
        vehiculos_dentro = self.parqueadero.listar_vehiculos()
        placas_libres = [p for p in self.placas_disponibles if p not in vehiculos_dentro]
        
        if placas_libres:
            return random.choice(placas_libres)
        return None
    
    def obtener_tipo_vehiculo(self):
        """Genera tipo de vehículo aleatorio"""
        return random.choice(['carro', 'moto'])
    
    def simular_entrada(self):
        """Simula la entrada de un vehículo"""
        # Verificar si hay espacio disponible
        espacios_carros = self.parqueadero.espacios_disponibles_carros()
        espacios_motos = self.parqueadero.espacios_disponibles_motos()
        
        if espacios_carros == 0 and espacios_motos == 0:
            print("❌ Parqueadero LLENO - No se puede registrar entrada")
            self.estadisticas['entradas_rechazadas'] += 1
            return
        
        # Obtener placa que no esté dentro
        placa = self.obtener_placa_disponible()
        if not placa:
            print("❌ No hay placas disponibles para simular")
            self.estadisticas['entradas_rechazadas'] += 1
            return
        
        # Determinar tipo basado en espacios disponibles
        if espacios_carros == 0:
            tipo = 'moto'
        elif espacios_motos == 0:
            tipo = 'carro'
        else:
            tipo = self.obtener_tipo_vehiculo()
        
        # Registrar entrada
        resultado = self.parqueadero.registrar_entrada(placa, tipo)
        
        if resultado.startswith('OK'):
            print(f"✅ ENTRADA: {placa} ({tipo.upper()}) - {resultado[4:]}")
            self.estadisticas['entradas_exitosas'] += 1
        else:
            print(f"❌ ENTRADA RECHAZADA: {placa} - {resultado[7:]}")
            self.estadisticas['entradas_rechazadas'] += 1
    
    def simular_salida(self):
        """Simula la salida de un vehículo"""
        vehiculos_dentro = self.parqueadero.listar_vehiculos()
        
        if not vehiculos_dentro:
            print("⚠️  No hay vehículos para sacar")
            self.estadisticas['salidas_rechazadas'] += 1
            return
        
        # Seleccionar vehículo aleatorio
        placa = random.choice(vehiculos_dentro)
        
        # Calcular tarifa antes de sacar
        tarifa = self.parqueadero.calcular_tarifa(placa)
        
        # Registrar salida
        resultado = self.parqueadero.registrar_salida(placa)
        
        if resultado.startswith('OK'):
            print(f"🚗 SALIDA: {placa} - Tarifa: ${tarifa:,.0f}")
            self.estadisticas['salidas_exitosas'] += 1
            self.estadisticas['total_recaudado'] += tarifa
        else:
            print(f"❌ SALIDA RECHAZADA: {placa} - {resultado[7:]}")
            self.estadisticas['salidas_rechazadas'] += 1
    
    def decidir_accion(self):
        """Decide si hacer entrada o salida basado en el estado actual"""
        vehiculos_dentro = len(self.parqueadero.listar_vehiculos())
        espacios_carros = self.parqueadero.espacios_disponibles_carros()
        espacios_motos = self.parqueadero.espacios_disponibles_motos()
        
        # Si está vacío, solo entrada
        if vehiculos_dentro == 0:
            return 'entrada'
        
        # Si está lleno, solo salida
        if espacios_carros == 0 and espacios_motos == 0:
            return 'salida'
        
        # Si hay pocos vehículos, favorecer entradas (70%)
        if vehiculos_dentro < 5:
            return random.choices(['entrada', 'salida'], weights=[70, 30])[0]
        
        # Si está casi lleno, favorecer salidas
        if espacios_carros + espacios_motos < 5:
            return random.choices(['entrada', 'salida'], weights=[30, 70])[0]
        
        # En estado medio, 50-50
        return random.choice(['entrada', 'salida'])
    
    def mostrar_estado(self):
        """Muestra el estado actual del parqueadero"""
        print("\n" + "="*60)
        print("📊 ESTADO DEL PARQUEADERO")
        print("="*60)
        print(f"🚗 Espacios disponibles CARROS: {self.parqueadero.espacios_disponibles_carros()}")
        print(f"🏍️  Espacios disponibles MOTOS: {self.parqueadero.espacios_disponibles_motos()}")
        print(f"📍 Vehículos dentro: {len(self.parqueadero.listar_vehiculos())}")
        print("="*60 + "\n")
    
    def mostrar_estadisticas_finales(self):
        """Muestra las estadísticas de la simulación"""
        print("\n" + "="*60)
        print("📈 ESTADÍSTICAS DE LA SIMULACIÓN")
        print("="*60)
        print(f"✅ Entradas exitosas: {self.estadisticas['entradas_exitosas']}")
        print(f"❌ Entradas rechazadas: {self.estadisticas['entradas_rechazadas']}")
        print(f"🚗 Salidas exitosas: {self.estadisticas['salidas_exitosas']}")
        print(f"❌ Salidas rechazadas: {self.estadisticas['salidas_rechazadas']}")
        print(f"💰 Total recaudado: ${self.estadisticas['total_recaudado']:,.0f}")
        print("="*60 + "\n")
    
    def ejecutar(self, num_operaciones=50, intervalo=1):
        """
        Ejecuta la simulación
        
        Args:
            num_operaciones: Número de operaciones a simular
            intervalo: Segundos de espera entre operaciones (0 para sin espera)
        """
        print("\n🚀 Iniciando simulación del parqueadero...")
        self.mostrar_estado()
        
        try:
            for i in range(1, num_operaciones + 1):
                print(f"\n--- Operación #{i} ---")
                
                # Decidir acción basada en estado actual
                accion = self.decidir_accion()
                
                # Ejecutar acción
                if accion == 'entrada':
                    self.simular_entrada()
                else:
                    self.simular_salida()
                
                # Mostrar estado cada 10 operaciones
                if i % 10 == 0:
                    self.mostrar_estado()
                
                # Esperar antes de la siguiente operación
                if intervalo > 0:
                    time.sleep(intervalo)
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Simulación interrumpida por el usuario")
        
        finally:
            # Mostrar estado final
            self.mostrar_estado()
            self.mostrar_estadisticas_finales()
            
            # Mostrar vehículos que quedaron dentro
            vehiculos_restantes = self.parqueadero.listar_vehiculos()
            if vehiculos_restantes:
                print("🚗 Vehículos que quedaron en el parqueadero:")
                for placa in vehiculos_restantes:
                    tarifa_actual = self.parqueadero.calcular_tarifa(placa)
                    print(f"   • {placa} - Tarifa actual: ${tarifa_actual:,.0f}")


def main():
    # Crear instancia del parqueadero (20 carros, 30 motos)
    print("🏗️  Creando parqueadero...")
    parqueadero = parqueadero_cpp.Parqueadero(20, 30, 3000.0, 2000.0)
    
    # Crear simulador
    simulador = SimuladorParqueadero(parqueadero)
    
    # Ejecutar simulación
    # Parámetros: número de operaciones, segundos entre operaciones
    simulador.ejecutar(num_operaciones=50, intervalo=0.5)
    
    # Si quieres simulación más rápida sin esperas:
    # simulador.ejecutar(num_operaciones=100, intervalo=0)
    
    # Si quieres simulación lenta y detallada:
    # simulador.ejecutar(num_operaciones=30, intervalo=2)


if __name__ == "__main__":
    main()