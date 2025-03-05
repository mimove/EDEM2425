import importlib.util
import json
from datetime import datetime

# Cargar el archivo initial_info.py
file_path = "initial_info.py"
spec = importlib.util.spec_from_file_location("initial_info", file_path)
initial_info = importlib.util.module_from_spec(spec)
spec.loader.exec_module(initial_info)

# Extraer datos
flights = initial_info.flights
airplanes = initial_info.airplanes
passengers = initial_info.passengers

# Función para calcular días hasta el próximo mantenimiento
def days_until_maintenance(maintenance_date):
    """Calcula el número de días hasta el próximo mantenimiento."""
    today = datetime.today().date()
    maintenance_date = datetime.strptime(maintenance_date, "%Y-%m-%d").date()
    days_remaining = (maintenance_date - today).days
    return days_remaining

# Mostrar días restantes hasta el próximo mantenimiento de cada avión
print("\n🚨 Estado de mantenimiento de los aviones:")
for airplane in airplanes:
    days_remaining = days_until_maintenance(airplane["nextMaintenanceDate"])
    status = "✅ OK" if days_remaining > 30 else "⚠️ Próximo mantenimiento" if days_remaining > 0 else "❌ Mantenimiento vencido"
    
    print(f"- {airplane['plateNumber']} ({airplane['type']}) - {days_remaining} días hasta mantenimiento → {status}")
