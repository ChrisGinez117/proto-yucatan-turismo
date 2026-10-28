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
    conexiones = [
        ("Mérida Centro", "Progreso", 36, 0.9),
        ("Mérida Centro", "Sisal", 53, 0.2),
        ("Mérida Centro", "Celestún", 95, 0.3),
        ("Mérida Centro", "Izamal", 67, 0.4),
        ("Mérida Centro", "Santa Elena", 85, 0.2),
        ("Mérida Centro", "Valladolid", 160, 0.5),
        ("Izamal", "Valladolid", 110, 0.3),
        ("Valladolid", "Ek Balam", 30, 0.2),
        ("Sisal", "Celestún", 75, 0.2)
    ]
    for origen, destino, km, congestion in conexiones:
        peso = km * (1 + congestion)
        G.add_edge(origen, destino, weight=peso, distancia_km=km)
    return G

G = obtener_grafo_yucatan()

# 3. Mapeo inteligente: Asignar un destino recomendado automático según el Perfil/Buyer Persona
RECOMENDACION_POR_PERFIL = {
    "🧘 Enfoque Calmado y Descanso (Haciendas y Paz)": {
        "destino_sugerido": "Sisal",
        "razon": "Ideal para escapar del bullicio urbano, disfrutar de playas vírgenes y atardeceres tranquilos lejos de la masificación de Progreso.",
        "itinerario": [
            "Paseo matutino por el muelle histórico de Sisal",
            "Comida de mariscos frescos frente al mar",
            "Atardecer de contemplación en la reserva natural"
        ]
    },
    "🍲 Tour Gastronómico y Tradición Culinaria": {
        "destino_sugerido": "Izamal",
        "razon": "Seleccionado por su profunda tradición culinaria, mercados locales auténticos y el arte de la cochinita pibil tradicional.",
        "itinerario": [
            "Desayuno de panuchos y salbutes tradicionales en el mercado municipal",
            "Visita cultural al Convento de San Antonio de Padua",
            "Comida de Cochinita Pibil al horno subterráneo y degustación de Xtabentún"
        ]
    },
    "🧗 Enfoque Extremo y Aventura al Aire Libre": {
        "destino_sugerido": "Ek Balam",
        "razon": "Perfecto para combinar arqueología profunda, caminata en selva alta y aventura activa con menor saturación turística.",
        "itinerario": [
            "Ascenso guiado a la cima de la Acrópolis Maya",
            "Recorrido en bicicleta de montaña rumbo al Cenote Xcanché",
            "Ecoturismo activo y tirolesa en la selva"
        ]
    }
}

# 4. Interfaz de usuario en Streamlit
st.title("🌱 Sistema Inteligente de Recomendación Turística en Yucatán")
st.markdown("### Te ayudamos a descubrir tu destino ideal según lo que buscas experimentar")
st.markdown("---")

st.sidebar.header("🎯 ¿Qué tipo de viaje buscas?")
perfil_seleccionado = st.sidebar.selectbox(
    "Selecciona tu estilo:",
    list(RECOMENDACION_POR_PERFIL.keys())
)

# El sistema toma el control y decide por el usuario basándose en su perfil
datos_recomendacion = RECOMENDACION_POR_PERFIL[perfil_seleccionado]
destino = datos_recomendacion["destino_sugerido"]
origen = "Mérida Centro" # Punto de partida estratégico estándar

# 5. Cálculo de la ruta con Dijkstra
ruta_optima = nx.dijkstra_path(G, source=origen, target=destino, weight="weight")

distancia_total = 0
for i in range(len(ruta_optima) - 1):
    distancia_total += G[ruta_optima[i]][ruta_optima[i+1]]["distancia_km"]

tiempo_estimado_min = int((distancia_total / 70) * 60)

# 6. Despliegue en pantalla
st.success(f"🤖 **Recomendación Inteligente del Sistema:** Basado en tu perfil, el destino perfecto para ti es **{destino}**.")

col_info, col_metrics = st.columns([2, 1])

with col_info:
    st.subheader(f"💡 ¿Por qué te recomendamos {destino}?")
    st.write(datos_recomendacion["razon"])
    
    st.subheader("📋 Itinerario Sugerido para tu Experiencia:")
    for act in datos_recomendacion["itinerario"]:
        st.write(f"• {act}")

with col_metrics:
    st.subheader("🚗 Datos de Trayecto")
    st.metric("Origen", origen)
    st.metric("Destino", destino)
    st.metric("Distancia estimada", f"{distancia_total:.0f} km")
    st.metric("Tiempo de viaje", f"~{tiempo_estimado_min} min")

st.markdown("---")

# Visualización gráfica de la ruta óptima
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🗺️ Ruta Vial Optimizada (Evitando Congestión)")
    pasos_str = " ➡️ ".join(ruta_optima)
    st.info(f"**Camino a seguir:** {pasos_str}")
    st.write("Esta ruta desvía el flujo turístico de las zonas saturadas hacia corredores emergentes sustentables.")

with col_right:
    st.subheader("🕸️ Mapa de Conectividad en la Red")
    fig, ax = plt.subplots(figsize=(5, 3.5))
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw_networkx_nodes(G, pos, node_size=400, node_color="#d3d3d3", ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color="#a0a0a0", width=1, ax=ax)
    
    edges_ruta = [(ruta_optima[i], ruta_optima[i+1]) for i in range(len(ruta_optima)-1)]
    nx.draw_networkx_nodes(G, pos, nodelist=ruta_optima, node_color="#2e7d32", node_size=500, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=edges_ruta, edge_color="#2e7d32", width=3, ax=ax)
    
    nx.draw_networkx_labels(G, pos, font_size=7, font_weight="bold", ax=ax)
    plt.axis("off")
    st.pyplot(fig)

st.markdown("---")
st.caption("Modelo de Ciencia de Datos aplicado a la redistribución turística sustentable en Yucatán.")
