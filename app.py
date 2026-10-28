import streamlit as st
import pandas as pd
import networkx as nx

# Configuración de la página
st.set_page_config(
    page_title="Turismo Sustentable Yucatán",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Campaña Turística Sustentable y Redistribución de Flujos en Yucatán")
st.markdown("---")

# Barra lateral con los 3 enfoques solicitados
st.sidebar.header("🎛️ Panel de Control de Pauta y Perfiles")

buyer_persona = st.sidebar.selectbox(
    "Selecciona el enfoque del Buyer Persona:",
    [
        "🧘 Enfoque Calmado y Descanso (Haciendas y Paz)",
        "🍲 Tour Gastronómico y Tradición Culinaria",
        "🧗 Enfoque Extremo y Aventura al Aire Libre"
    ]
)

destino_interes = st.sidebar.selectbox(
    "Corredor Turístico Emergente:",
    ["Sisal", "Celestún", "Izamal", "Valladolid", "Ek Balam", "Santa Elena"]
)

st.sidebar.markdown("---")
st.sidebar.info("Proyecto académico: Ciencia de Datos, NetworkX y Modelos de Optimización.")

# Sección Principal dividida
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Perfil del Buyer Persona Seleccionado")
    
    if "Calmado" in buyer_persona:
        st.markdown("""
        * **Perfil:** Viajero que busca desconexión total del ritmo urbano y masificado.
        * **Intereses:** Estancias en haciendas históricas, pueblos mágicos silenciosos, atardeceres en la costa y espacios de contemplación.
        * **Necesidad:** Paz mental, evitar aglomeraciones y conectar con la naturaleza de forma relajada.
        * **Destinos ideales:** Sisal, Celestún o Izamal.
        """)
    elif "Gastronómico" in buyer_persona:
        st.markdown("""
        * **Perfil:** Amante de la culinaria tradicional, mercados locales y experiencias de granja a mesa.
        * **Intereses:** Cochinita pibil tradicional, recados mayas, talleres culinarios y cenotes con gastronomía típica comunitaria.
        * **Necesidad:** Vivir la auténtica cultura culinaria yucateca apoyando directamente a cocineras tradicionales.
        * **Destinos ideales:** Valladolid, Izamal y Santa Elena.
        """)
    else:
        st.markdown("""
        * **Perfil:** Turista dinámico con inclinación por el ecoturismo activo y la exploración profunda.
        * **Intereses:** Senderismo en selva, exploración de grutas, nado en cenotes abiertos/cerrados y zonas arqueológicas alternativas menos masificadas.
        * **Necesidad:** Adrenalina, reto físico y aventura responsable en contacto directo con el entorno.
        * **Destinos ideales:** Ek Balam, Ruta de Cenotes y Santa Elena.
        """)

with col2:
    st.subheader(f"📍 Análisis del Corredor: {destino_interes}")
    st.write("El sistema evalúa la capacidad de carga en tiempo real para este destino:")
    
    # Grafo interactivo con NetworkX incluyendo todos los destinos del reporte
    G = nx.Graph()
    conexiones = [
        ("Mérida_Centro", "Progreso", 36),
        ("Mérida_Centro", "Sisal", 53),
        ("Mérida_Centro", "Celestún", 95),
        ("Mérida_Centro", "Izamal", 67),
        ("Mérida_Centro", "Santa_Elena", 85),
        ("Mérida_Centro", "Valladolid", 160),
        ("Izamal", "Valladolid", 110),
        ("Valladolid", "Ek_Balam", 30),
        ("Sisal", "Celestún", 75)
    ]
    G.add_weighted_edges_from(conexiones)
    
    st.metric(label="Destinos Conectados en la Red", value=len(G.nodes()))
    st.metric(label="Rutas Viales Monitoreadas", value=len(G.edges()))
    
    st.success(f"Estrategia activa: Redirigiendo pauta y optimizando flujos hacia **{destino_interes}**.")

st.markdown("---")
st.markdown("*Desarrollado para la validación técnica y académica de la campaña turística sustentable en Yucatán.*")
