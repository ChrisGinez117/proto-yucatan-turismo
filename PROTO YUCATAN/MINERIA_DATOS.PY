import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar el dataset de usuarios que acabamos de crear
df = pd.read_csv('usuarios_turismo_yucatan.csv')

# 2. Seleccionar las variables (features) que definirán los clusters
X = df[['pref_tranquilidad', 'pref_actividad_fisica', 'pref_adrenalina', 'presupuesto_diario']]

# 3. Normalizar los datos (Muy importante en Minería de Datos para que el presupuesto en miles no opaque a las escalas de 1 a 10)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Aplicar el algoritmo K-Means buscando 3 clústeres (nuestros 3 Buyer Persona)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X_scaled)

# 5. Etiquetar los clusters según sus características promedio para mayor claridad
# Mapearemos los clústeres basándonos en sus medias para nombrarlos correctamente
medias = df.groupby('cluster')[['pref_tranquilidad', 'pref_actividad_fisica', 'pref_adrenalina']].mean()
print("--- PROMEDIOS POR CLÚSTER ---")
print(medias)

# Guardar el resultado con la clasificación del Buyer Persona
df.to_csv('usuarios_con_clusters.csv', index=False)
print("\n✅ Archivo 'usuarios_con_clusters.csv' generado con la clasificación de los 3 perfiles.")

# 6. Opcional: Gráfica de dispersión para visualizar la minería de datos
plt.figure(figsize=(8, 6))
sns.scatterplot(
    x=df['pref_tranquilidad'], 
    y=df['pref_adrenalina'], 
    hue=df['cluster'], 
    palette='viridis', 
    s=60, 
    alpha=0.8
)
plt.title("Minería de Datos: Segmentación de Turistas (K-Means)")
plt.xlabel("Preferencia de Tranquilidad (1-10)")
plt.ylabel("Preferencia de Adrenalina (1-10)")
plt.legend(title="Buyer Persona (Cluster)")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("clusters_buyer_persona.png")
print("📊 Gráfica de clústeres guardada como 'clusters_buyer_persona.png'.")