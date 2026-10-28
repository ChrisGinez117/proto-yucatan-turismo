import networkx as nx
import matplotlib.pyplot as plt

def crear_red_yucatan():
    # Crear el grafo vial de Yucatán enfocado en redistribución turística
    G = nx.Graph()

    # Definir nodos principales (Nodos saturados vs Corredores emergentes del reporte)
    nodos_atractivos = {
        # Zonas saturadas base
        "Mérida_Centro": {"tipo": "Urbano_Saturado", "lat": 20.967, "lon": -89.623},
        "Progreso": {"tipo": "Playa_Saturada", "lat": 21.284, "lon": -89.663},
        
        # Corredor Poniente / Costa y Ría
        "Sisal": {"tipo": "Pueblo_Magico_Playa", "lat": 21.166, "lon": -90.046},
        "Celestún": {"tipo": "Naturaleza_Reserva", "lat": 20.864, "lon": -90.395},
        
        # Corredor Central / Cultural
        "Izamal": {"tipo": "Pueblo_Magico_Cultural", "lat": 20.933, "lon": -89.016},
        "Ruta_Cenotes_Homun": {"tipo": "Naturaleza_Cenotes", "lat": 20.733, "lon": -89.283},
        
        # Corredor Sur / Biocultural (Mencionado en el reporte)
        "Santa_Elena": {"tipo": "Turismo_Comunitario", "lat": 20.332, "lon": -89.633},
        
        # Corredor Oriente / Arqueología y Cenotes (Mencionado en el reporte)
        "Valladolid": {"tipo": "Pueblo_Magico_Cenotes", "lat": 20.689, "lon": -88.203},
        "Ek_Balam": {"tipo": "Arqueologia_Alternativa", "lat": 20.893, "lon": -88.132}
    }

    # Agregar nodos al grafo
    for nodo, datos in nodos_atractivos.items():
        G.add_node(nodo, **datos)

    # Definir aristas (carreteras) con distancias (km) y factor de congestión base
    conexiones = [
        # Conexiones desde Mérida (Nodo central saturado)
        ("Mérida_Centro", "Progreso", 36.0, 0.9),       # Alta congestión
        ("Mérida_Centro", "Sisal", 53.0, 0.3),          # Alternativa costa poniente
        ("Mérida_Centro", "Celestún", 95.0, 0.4),       # Alternativa ría y flamencos
        ("Mérida_Centro", "Izamal", 67.0, 0.4),         # Ruta cultural amarilla
        ("Mérida_Centro", "Ruta_Cenotes_Homun", 45.0, 0.4),
        ("Mérida_Centro", "Santa_Elena", 85.0, 0.3),    # Ruta sur / Puuc
        ("Mérida_Centro", "Valladolid", 160.0, 0.6),    # Conexión oriente principal
        
        # Conexiones regionales secundarias (Redistribución sin pasar por Mérida)
        ("Izamal", "Valladolid", 110.0, 0.3),
        ("Valladolid", "Ek_Balam", 30.0, 0.2),          # Desvío hacia alternativa arqueológica
        ("Sisal", "Celestún", 75.0, 0.2),               # Corredor costero poniente
        ("Santa_Elena", "Ruta_Cenotes_Homun", 70.0, 0.3)
    ]

    for origen, destino, distancia, congestion in conexiones:
        # El peso efectivo combina la distancia real y la penalización por tráfico en tiempo real
        peso_total = distancia * (1 + congestion)
        G.add_edge(origen, destino, weight=peso_total, distancia_km=distancia, congestion=congestion)

    return G

if __name__ == "__main__":
    grafo = crear_red_yucatan()
    print(f"Red cargada exitosamente con {grafo.number_of_nodes()} destinos y {grafo.number_of_edges()} rutas viales.")
