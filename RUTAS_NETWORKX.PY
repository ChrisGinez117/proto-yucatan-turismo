import networkx as nx

def calcular_ruta_optima(perfil, duracion):
    """
    Calcula la ruta óptima usando NetworkX según el perfil del usuario 
    y la duración de la experiencia ('1_dia' o '3_dias').
    """
    G = nx.Graph()
    
    # -------------------------------------------------------------------------
    # 1. PERFIL: RELAJACIÓN (Naturaleza, haciendas y comunidades tranquilas)
    # -------------------------------------------------------------------------
    if perfil == 'Relajacion':
        if duracion == '1_dia':
            # Micro-circuito local (Zona Centro-Sur)
            conexiones = [
                ("Hacienda Yaxcopoil", "Cenote Dzonbacal (Tekit)", 28.1),
                ("Cenote Dzonbacal (Tekit)", "Pueblo Mágico Maní", 42.5)
            ]
            inicio = "Hacienda Yaxcopoil"
            fin = "Pueblo Mágico Maní"
        else:
            # Road Trip de 3 Días (Circuito extendido desde la costa oeste)
            conexiones = [
                ("Celestún (Ría)", "Hacienda Yaxcopoil", 75.4),
                ("Hacienda Yaxcopoil", "Cenote Dzonbacal (Tekit)", 28.1),
                ("Cenote Dzonbacal (Tekit)", "Pueblo Mágico Maní", 42.5),
                ("Celestún (Ría)", "Cenote Dzonbacal (Tekit)", 95.0)
            ]
            inicio = "Celestún (Ría)"
            fin = "Pueblo Mágico Maní"

    # -------------------------------------------------------------------------
    # 2. PERFIL: AVENTURERO (Arqueología, historia y senderos)
    # -------------------------------------------------------------------------
    elif perfil == 'Aventurero':
        if duracion == '1_dia':
            # Micro-circuito arqueológico rápido
            conexiones = [
                ("Zona Arqueológica Mayapán", "Acanceh (Pirámides)", 18.5),
                ("Acanceh (Pirámides)", "Tecoh (Sedes Mayas)", 22.0)
            ]
            inicio = "Zona Arqueológica Mayapán"
            fin = "Tecoh (Sedes Mayas)"
        else:
            # Road Trip de 3 Días (Costa norte y sur profundo)
            conexiones = [
                ("Xcambó", "Dzibilchaltún", 45.2),
                ("Dzibilchaltún", "Grutas de Loltún", 115.0),
                ("Xcambó", "Grutas de Loltún", 140.5)
            ]
            inicio = "Xcambó"
            fin = "Grutas de Loltún"

    # -------------------------------------------------------------------------
    # 3. PERFIL: EXTREMO (Cenotes profundos, grutas y ecoturismo costero)
    # -------------------------------------------------------------------------
    elif perfil == 'Extremo':
        if duracion == '1_dia':
            # Micro-circuito de cenotes y cavernas
            conexiones = [
                ("Cenote San Ignacio (Chocholá)", "Cuzamá (Grutas)", 24.1),
                ("Cuzamá (Grutas)", "Cenotes de Homún", 16.2)
            ]
            inicio = "Cenote San Ignacio (Chocholá)"
            fin = "Cenotes de Homún"
        else:
            # Road Trip de 3 Días (De poniente a oriente extremo)
            conexiones = [
                ("Cenote San Ignacio (Chocholá)", "Cenotes de Homún", 55.3),
                ("Cenotes de Homún", "El Cuyo (Reserva)", 185.4),
                ("Cenote San Ignacio (Chocholá)", "El Cuyo (Reserva)", 210.0)
            ]
            inicio = "Cenote San Ignacio (Chocholá)"
            fin = "El Cuyo (Reserva)"

    # Construir el grafo ponderado
    for u, v, w in conexiones:
        G.add_edge(u, v, weight=w)

    # Calcular ruta óptima con el algoritmo de Dijkstra
    try:
        ruta_optima = nx.shortest_path(G, source=inicio, target=fin, weight='weight')
        distancia_total = nx.shortest_path_length(G, source=inicio, target=fin, weight='weight')
        return ruta_optima, distancia_total
    except nx.NetworkXNoPath:
        return ["Ruta no disponible para estos parámetros"], 0.0


if __name__ == "__main__":
    print("==================================================")
    print("   SIMULACIÓN DE RUTAS MULTI-ESCALA (YUCATÁN)      ")
    print("==================================================\n")
    
    # Pruebas de simulación para ambos modos
    perfiles = ['Relajacion', 'Aventurero', 'Extremo']
    modalidades = ['1_dia', '3_dias']
    
    for p in perfiles:
        for m in modalidades:
            ruta, dist = calcular_ruta_optima(p, m)
            tipo_viaje = "Escapada 1 Día" if m == '1_dia' else "Road Trip 3 Días"
            print(f"[{p.upper()} - {tipo_viaje}]")
            print(f"  📍 Ruta: {' -> '.join(ruta)}")
            print(f"  📏 Distancia: {dist} km\n")
            
    print("==================================================")