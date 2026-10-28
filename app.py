import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 1. Configuración de página
st.set_page_config(
    page_title="Turismo Sustentable Yucatán",
    page_icon="🌱",
    layout="wide"
)

# 2. Definición del Grafo con NetworkX
@st.cache_data
def obtener_grafo_yucatan():
    G = nx.Graph()
    # Conexiones con distancias en km y factor de tráfico/congestión
    conexiones = [
        ("Mérida Centro", "Progreso", 36, 0.9),       # Muy concurrido
        ("Mérida Centro", "Sisal", 53, 0.2),          # Alternativa tranquila
        ("Mérida Centro", "Celestún", 95, 0.3),       # Reserva natural
        ("Mérida Centro", "Izamal", 67, 0.4),         # Pueblo Mágico cultural
        ("Mérida Centro", "Santa Elena", 85, 0.2),    # Ruta Sur / Puuc
        ("Mérida Centro", "Valladolid", 160, 0.5),    # Oriente
        ("Izamal", "Valladolid", 110, 0.3),
        ("Valladolid", "Ek Balam", 30, 0.2),          # Arqueología alternativa
        ("Sisal", "Celestún", 75, 0.2)
    ]
    for origen, destino, km, congestion in conexiones:
        # El peso combina distancia y congestión para optimizar la ruta
        peso = km * (1 + congestion)
        G.add_edge(origen, destino, weight=peso, distancia_km=km)
    return G

G = obtener_grafo_yucatan()

# 3. Datos de itinerarios recomendados según el perfil
ITINERARIOS = {
    "🧘 Enfoque Calmado y Descanso (Haciendas y Paz)": {
        "Sisal": ["Paseo matutino por el muelle histórico", "Comida mariscada frente al mar tranquilo", "Atardecer en la reserva ecológica"],
        "Celestún": ["Paseo en lancha por la Ría de Celestún (avistamiento de flamencos)", "Descanso en playa virgen", "Cena en pescadería local"],
        "Izamal": ["Caminata por el Convento de San Antonio de Padua", "Paseo en bicicleta por calles amarillas", "Descanso en casona colonial"],
        "Valladolid": ["Visita matutina al Cenote Zací", "Café y lectura en la Calzada de los Frailes", "Cena en patio colonial"],
        "Ek Balam": ["Caminata tranquila por la selva", "Exploración relajada de la acrópolis", "Visita a talleres artesanales locales"],
        "Santa Elena": ["Recorrido por la iglesia histórica y museo", "Estancia en cabañas ecoturísticas", "Caminata por senderos bioculturales"]
    },
    "🍲 Tour Gastronómico y Tradición Culinaria": {
        "Sisal": ["Desayuno de pescado frito tradicional", "Taller de cocina marinera local", "Degustación de ceviches estilo yucateco"],
        "Celestún": ["Desayuno costeño", "Almuerzo de filete a la manchafiel en la playa", "Cena de mariscos frescos"],
        "Izamal": ["Desayuno de panuchos y salbutes en el mercado municipal", "Comida en restaurante especializado en Cochinita Pibil al hoyo", "Degustación de licores artesanales (Xtabentún)"],
        "Valladolid": ["Desayuno de Longaniza de Valladolid con huevos", "Tour de mercados y puestos tradicionales", "Cena gourmet de alta cocina yucateca en Calzada de los Frailes"],
        "Ek Balam": ["Desayuno en comunidad maya cercana", "Degustación de tortillas hechas a mano y recados mayas", "Comida de Poc Chuc"],
        "Santa Elena": ["Cena tradicional de manjar blanco y sopa de lima", "Visita a cocineras tradicionales de la Zona Puuc", "Taller de elaboración de recado negro"]
    },
    "🧗 Enfoque Extremo y Aventura al Aire Libre": {
        "Sisal": ["Recorrido en kayak por los manglares", "Paddleboarding en mar abierto", "Ciclismo de ruta costera"],
        "Celestún": ["Expedición nocturna en busca de cocodrilos en el manglar", "Kayak de velocidad en la ría", "Senderismo de observación de fauna"],
        "Izamal": ["Ruta en cuatrimoto por pirámides y senderos de tierra", "Ciclismo intermunicipal hacia cenotes", "Escalada en pirámide Kinich KakMó"],
        "Valladolid": ["Snorkel y salto de altura en Cenote Oxmán", "Ciclismo hasta cenotes escondidos", "Exploración de cavernas subterráneas"],
        "Ek Balam": ["Ascenso rápido a la cima de la Acrópolis Maya", "Senderismo de selva alta", "Recorrido en bicicleta de montaña hacia el Cenote Xcanché"],
        "Santa Elena": ["Ruta en Bici de Montaña por la Serranía Puuc", "Exploración de grutas no comerciales", "Senderismo extremo en selva baja"]
    }
}

# 4. Interfaz de usuario en Streamlit
st.title("🌱 Generador de Rutas e Itinerarios Turísticos en Yucatán")
st.markdown("---")

st.sidebar.header("🎛️ Personaliza tu Viaje")

perfil = st.sidebar.selectbox(
    "1. Selecciona tu estilo de viaje:",
    list(ITINERARIOS.keys())
)

origen = st.sidebar.selectbox(
    "2. Punto de partida:",
    ["Mérida Centro", "Izamal", "Valladolid", "Sisal"]
)

destino = st.sidebar.selectbox(
    "3. Destino al que deseas viajar:",
    ["Sisal", "Celestún", "Izamal", "Valladolid", "Ek Balam", "Santa Elena"]
)

st.sidebar.markdown("---")
st.sidebar.info("El algoritmo calcula la ruta óptima evitando congestión vehicular en arterias principales.")

# 5. Lógica del Algoritmo Dijkstra
if origen == destino:
    st.warning("⚠️ Selecciona un punto de partida y un destino diferentes.")
else:
    # Cálculo de la ruta más corta/óptima con NetworkX
    ruta_optima = nx.dijkstra_path(G, source=origen, target=destino, weight="weight")
    
    # Calcular distancia total estimada
    distancia_total = 0
    for i in range(len(ruta_optima) - 1):
        distancia_total += G[ruta_optima[i]][ruta_optima[i+1]]["distancia_km"]
    
    tiempo_estimado_min = int((distancia_total / 70) * 60) # Asumiendo 70 km/h prom.

    # Mostrar Resultados al Turista
    st.header(f"🗺️ Tu Itinerario Recomendado: De {origen} a {destino}")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Distancia Total", f"{distancia_total:.0f} km")
    m2.metric("Tiempo Estimado de Viaje", f"~{tiempo_estimado_min} min")
    m3.metric("Nivel de Congestión de la Ruta", "Bajo (Optimizado)")

    st.markdown("---")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("📍 Ruta Vial Recomendada paso a paso:")
        pasos = " ➡️ ".join(ruta_optima)
        st.success(f"**Camino óptimo:** {pasos}")

        st.subheader("📋 Sugerencias de Actividades para tu perfil:")
        actividades = ITINERARIOS[perfil].get(destino, ["Exploración libre del destino y apoyo al comercio local."])
        for act in actividades:
            st.write(f"• {act}")

    with col_right:
        st.subheader("🕸️ Esquema de la Red Vial")
        fig, ax = plt.subplots(figsize=(6, 4))
        
        pos = nx.spring_layout(G, seed=42)
        
        # Dibujar todos los nodos
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color="#d3d3d3", ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color="#a0a0a0", width=1, ax=ax)
        
        # Resaltar la ruta seleccionada
        edges_ruta = [(ruta_optima[i], ruta_optima[i+1]) for i in range(len(ruta_optima)-1)]
        nx.draw_networkx_nodes(G, pos, nodelist=ruta_optima, node_color="#2e7d32", node_size=600, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=edges_ruta, edge_color="#2e7d32", width=3, ax=ax)
        
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold", ax=ax)
        
        plt.axis("off")
        st.pyplot(fig)

st.markdown("---")
st.caption("Proyecto Académico de Ciencia de Datos - Modelo de Redistribución Turística Sustentable.")
