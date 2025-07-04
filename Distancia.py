import requests

API_KEY = "d50344fc-9679-47e4-b8e8-47f5ff47fcdd"

def geocodificar_ciudad(ciudad, pais):
    """Devuelve coordenadas 'lat,lng' de una ciudad en un país usando la API de GraphHopper."""
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": f"{ciudad}, {pais}",
        "limit": 1,
        "key": API_KEY
    }
    try:
        respuesta = requests.get(url, params=params, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()
        if datos["hits"]:
            punto = datos["hits"][0]["point"]
            return f"{punto['lat']},{punto['lng']}"
        return None
    except requests.RequestException as e:
        print(f"❌ Error al buscar ciudad: {e}")
        return None

def obtener_ruta(origen, destino, transporte):
    """Consulta la API de rutas de GraphHopper y devuelve los datos de ruta."""
    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [origen, destino],
        "vehicle": transporte,
        "locale": "es",
        "key": API_KEY,
        "instructions": "true",
        "calc_points": "true"
    }
    try:
        respuesta = requests.get(url, params=params, timeout=10)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.RequestException as e:
        print(f"❌ Error de comunicación: {e}")
        return None

def segundos_a_hms(segundos):
    """Convierte segundos a formato (horas, minutos, segundos)."""
    h = int(segundos // 3600)
    m = int((segundos % 3600) // 60)
    s = int(segundos % 60)
    return h, m, s

def km_a_millas(km):
    """Convierte kilómetros a millas."""
    return km * 0.621371

def main():
    print("=== Calculadora de Ruta entre Chile y Argentina ===")
    print("Puedes salir en cualquier momento escribiendo 's'\n")

    while True:
        origen = input("🟢 Ciudad de Origen (Chile): ").strip()
        if origen.lower() == "s":
            print("👋 Saliendo del programa.")
            break

        destino = input("🔵 Ciudad de Destino (Argentina): ").strip()
        if destino.lower() == "s":
            print("👋 Saliendo del programa.")
            break

        print("🚗 Selecciona el medio de transporte:")
        print("   1. Auto")
        print("   2. Bicicleta")
        print("   3. A pie")
        tipo = input("   Opción (1/2/3): ").strip()
        if tipo.lower() == "s":
            print("👋 Saliendo del programa.")
            break

        transporte = {"1": "car", "2": "bike", "3": "foot"}.get(tipo)
        if not transporte:
            print("❌ Medio de transporte no válido.")
            continue

        coord_origen = geocodificar_ciudad(origen, "Chile")
        coord_destino = geocodificar_ciudad(destino, "Argentina")

        if not coord_origen:
            print(f"❌ No se encontró la ciudad de origen: {origen}")
            continue
        if not coord_destino:
            print(f"❌ No se encontró la ciudad de destino: {destino}")
            continue

        datos_ruta = obtener_ruta(coord_origen, coord_destino, transporte)
        if not datos_ruta:
            print("❌ No se pudo obtener la ruta.")
            continue

        ruta = datos_ruta["paths"][0]
        distancia_km = ruta["distance"] / 1000
        distancia_millas = km_a_millas(distancia_km)
        duracion_seg = ruta["time"] / 1000
        h, m, s = segundos_a_hms(duracion_seg)

        print("\n🛣️  Resultados del viaje:")
        print(f"   - Distancia: {distancia_km:.2f} km")
        print(f"   - Distancia: {distancia_millas:.2f} millas")
        print(f"   - Duración:  {h}h {m}m {s}s")

        print("\n📍 Narrativa del viaje:")
        for paso in ruta["instructions"]:
            print(f"   ➤ {paso['text']} ({paso['distance']:.0f} m)")

        print("\n✅ Ruta calculada exitosamente.\n")

if __name__ == "__main__":
    main()

