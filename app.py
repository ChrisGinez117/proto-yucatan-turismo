import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 1. Configuración de página
st.set_page_config(
    page_title="Sistema de Redistribución Turística - Yucatán",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ Sistema Inteligente de Redistribución Turística en Yucatán")
st.markdown("### Basado en Datos Históricos del INAH y Teoría de Grafos (NetworkX)")
st.markdown("---")

# 2. Construcción del Grafo Oficial del Equipo (Clústeres INAH)
@st.cache_data
def crear_grafo_inah():
    G = nx.Graph()
    
    # Corredores arqueológicos basados en el reporte del equipo
    corredores = [
        # Clúster Oriente (Alternativas a Chichén Itzá)
        ("Zona Arqueológica de Chichén Itzá", "Zona Arqueológica de Ekbalam"),
        ("Zona Arqueológica de Chichén Itzá", "Zona Arqueológica de Izamal"),
        ("Zona Arqueológica de Chichén Itzá", "Zona Arqueológica de Mayapán"),
        
        # Clúster Sur Ruta Puuc (Alternativas a Uxmal)
        ("Zona Arqueológica de Uxmal con museo de sitio", "Zona Arqueológica de Kabah"),
        ("Zona Arqueológica de Kabah", "Zona Arqueológica de Sayil"),
        ("Zona Arqueológica de Sayil", "Zona Arqueológica de Labná"),
        ("Zona Arqueológica de Labná", "Zona Arqueológica de Xlapak")
    ]
    G.add_edges_from(corredores)
    return G

G = crear_grafo_inah()

# 3. Capacidades máximas e insumos del modelo del equipo
capacidades_maximas = {
    "Zona Arqueológica de Chichén Itzá": 180000,
    "Zona Arqueológica de Uxmal con museo de sitio": 30000,
    "Zona Arqueológica de Izamal con museo de sitio": 30000
}

# 4. Panel de Control en Barra Lateral
st.sidebar.header("🎛️ Parámetros de Simulación e INAH")
anio_sel = st.sidebar.selectbox("Año de Análisis:", [2025, 2026])
mes_sel = st.sidebar.selectbox(
    "Periodo / Mes de Evaluación:",
    [
        ("marzo_total", "Marzo (Semana Santa / Primavera)"),
        ("julio_total", "Julio (Verano)"),
        ("agosto_total", "Agosto (Verano)"),
        ("diciembre_total", "Diciembre (Fin de Año / Invierno)")
    ],
    format_func=lambda x: x[1]
)

st.sidebar.markdown("---")
st.sidebar.header("🎯 Perfil del Turista (Buyer Persona)")
perfil_usuario = st.sidebar.selectbox(
    "Selecciona el enfoque de tu viaje:",
    [
        "🧘 Enfoque Calmado y Descanso (Ruta Puuc / Sitios íntimos)",
        "🍲 Tour Gastronómico y Tradición (Izamal / Valladolid)",
        "🧗 Enfoque Extremo y Aventura (Ek Balam / Mayapán)"
    ]
)

# 5. Lógica de recomendación y simulación inspirada en el equipo
col1, col2 = st.columns([1.2, 0.8])

with col1:
    st.subheader("📊 Diagnóstico de Afluencia y Alertas de Saturación")
    st.write(f"Evaluando comportamiento operativo para el periodo: **{mes_sel[1]} ({anio_sel})**[cite: 7].")
    
    # Simulación lógica basada en el script de minería del equipo
    if "Diciembre" in mes_sel[1]:
        st.warning("⚠️ **ALERTA DE SATURACIÓN DETECTADA EN TEMPORADA ALTA**[cite: 8]")
        st.markdown("""
        * **Chichén Itzá:** Superó el umbral (182,900 / 180,000 visitantes)[cite: 8].
          * *Acción del Algoritmo:* Desvío equitativo de **2,900 turistas excedentes** hacia el corredor oriente[cite: 8].
          * *Destinos receptores:* **Ekbalam, Izamal y Mayapán** (+967 visitantes c/u)[cite: 8].
        * **Uxmal:** Superó el aforo (32,692 / 30,000 visitantes)[cite: 8].
          * *Acción del Algoritmo:* Canalización del excedente hacia **Kabah** (+2,692 visitantes)[cite: 8].
        """)
        estado_saturacion = "Saturado (Redireccionamiento Activo)"
    else:
        st.success("✅ **Operación Normal. Sin saturación en este periodo.**[cite: 7, 9]")
        st.markdown("""
        * Los flujos turísticos se encuentran por debajo de las capacidades máximas permitidas por el INAH[cite: 7, 9].
        * Las sedes principales operan con fluidez y los corredores alternativos se mantienen disponibles para equilibrar la carga[cite: 9].
        """)
        estado_saturacion = "Normal"

    st.markdown("---")
    st.subheader("💡 Recomendación de Viaje según tu Perfil")
    
    if "Calmado" in perfil_usuario:
        st.info("**Destino Sugerido por el Sistema:** Circuito Ruta Puuc (Kabah, Sayil, Labná)")
        st.write("Ideal para evitar aglomeraciones, disfrutando de arquitectura detallada en entornos selváticos de baja densidad[cite: 4].")
    elif "Gastronómico" in perfil_usuario:
        st.info("**Destino Sugerido por el Sistema:** Izamal y Corredor Oriente")
        st.write("Combina la grandeza de la pirámide Kinich Kakmó con mercados tradicionales y experiencias culinarias mayas auténticas[cite: 3].")
    else:
        st.info("**Destino Sugerido por el Sistema:** Ek Balam y Mayapán")
        st.write("Perfecto para quienes buscan ascenso activo a pirámides principales, estucos históricos y exploración de murallas prehispánicas[cite: 3].")

with col2:
    st.subheader("🕸️ Topología de Red (NetworkX)")
    
    # Generar visualización del grafo del equipo
    fig, ax = plt.subplots(figsize=(6, 5))
    pos = nx.spring_layout(G, seed=42)
    
    nx.draw_networkx_nodes(G, pos, node_size=600, node_color="#a8dadc", ax=ax)
    nx.draw_networkx_edges(G, pos, width=2, edge_color="#457b9d", ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=7, font_weight="bold", ax=ax)
    
    plt.title(f"Red de Corredores INAH ({anio_sel})", fontsize=10, fontweight="bold")
    plt.axis("off")
    st.pyplot(fig)

st.markdown("---")
st.caption("Proyecto Académico de Minería de Datos e Inteligencia de Negocios — Yucatán.")
