import requests

API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjZhNmE4NmFjOTk4MjQ1YTliYTY2NzEwMWNkMjkyZTE0IiwiaCI6Im11cm11cjY0In0="
ORS_BASE_URL = "https://api.openrouteservice.org/v2/directions/"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

TRANSPORT_PROFILES = {
    "1": {"name": "Coche", "profile": "driving-car"},
    "2": {"name": "Bicicleta (Carretera)", "profile": "cycling-road"},
    "3": {"name": "Caminando", "profile": "foot-walking"},
    "4": {"name": "Camión", "profile": "driving-hgv"}
}

def get_coordinates(city_name):
    params = {'q': city_name, 'format': 'json', 'limit': 1}
    headers = {'User-Agent': 'PythonDistanceCalculator/1.0'}
    try:
        response = requests.get(NOMINATIM_URL, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]['lon']), float(data[0]['lat'])
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al obtener coordenadas para '{city_name}': {e}")
        return None

def get_route_info(start_coords, end_coords, profile):
    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json'
    }
    body = {
        "coordinates": [start_coords, end_coords]
    }
    try:
        response = requests.post(f"{ORS_BASE_URL}{profile}", headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        if data and 'routes' in data and data['routes']:
            route = data['routes'][0]
            distance_km = route['summary']['distance'] / 1000
            duration_seconds = route['summary']['duration']
            return distance_km, duration_seconds, route['segments'][0]['steps']
        return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al obtener ruta para el perfil '{profile}': {e}")
        print(f"Respuesta del servidor: {response.text if 'response' in locals() else 'No response'}")
        return None, None, None

def format_duration(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    if seconds: parts.append(f"{seconds}s")
    return " ".join(parts) if parts else "0s"

def display_narrative(steps):
    print("\n--- Narrativa del Viaje ---")
    if not steps:
        print("No hay pasos de ruta disponibles.")
        return
    for i, step in enumerate(steps):
        print(f"{i+1}. {step.get('instruction', 'Instrucción no disponible')}")
    print("--------------------------")

def main():
    while True:
        print("\n--- Calculadora de Viajes ---")
        origen = input("Introduce la Ciudad de Origen (o 's' para salir): ").strip()
        if origen.lower() == 's':
            print("Saliendo de la calculadora de viajes. ¡Hasta pronto!")
            break

        destino = input("Introduce la Ciudad de Destino: ").strip()

        print("\nSelecciona un medio de transporte:")
        for key, value in TRANSPORT_PROFILES.items():
            print(f"  {key}: {value['name']}")

        selected_profile = None
        while selected_profile is None:
            choice = input("Tu elección: ").strip()
            if choice in TRANSPORT_PROFILES:
                selected_profile = TRANSPORT_PROFILES[choice]
            else:
                print("Opción inválida. Por favor, elige un número de la lista.")

        print(f"\nBuscando ruta de {origen} a {destino} en {selected_profile['name']}...")

        coords_origen = get_coordinates(origen)
        coords_destino = get_coordinates(destino)

        if coords_origen and coords_destino:
            distance_km, duration_seconds, steps = get_route_info(
                coords_origen, coords_destino, selected_profile['profile']
            )

            if distance_km is not None:
                distance_miles = distance_km * 0.621371

                print(f"\n--- Resultados del Viaje ---")
                print(f"Origen: {origen}")
                print(f"Destino: {destino}")
                print(f"Medio de Transporte: {selected_profile['name']}")
                print(f"Distancia: {distance_km:.2f} Kilómetros")
                print(f"Distancia: {distance_miles:.2f} Millas")
                print(f"Duración del Viaje: {format_duration(duration_seconds)}")
                print("----------------------------")

                display_narrative(steps)
            else:
                print("No se pudo calcular la ruta. Por favor, verifica las ciudades y tu clave API.")
        else:
            print("No se pudieron obtener las coordenadas de una o ambas ciudades.")

if __name__ == "__main__":
    main()