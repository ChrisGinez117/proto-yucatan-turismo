import numpy as np
import pandas as pd

# Fijar semilla para reproducibilidad
np.random.seed(42)
num_usuarios = 300

# Generar datos simulados de encuestas a turistas
tranquilidad = np.random.randint(1, 11, size=num_usuarios)
actividad_fisica = np.random.randint(1, 11, size=num_usuarios)
adrenalina = np.random.randint(1, 11, size=num_usuarios)
presupuesto = np.random.randint(500, 3500, size=num_usuarios)

df_usuarios = pd.DataFrame({
    'id_usuario': range(1, num_usuarios + 1),
    'pref_tranquilidad': tranquilidad,
    'pref_actividad_fisica': actividad_fisica,
    'pref_adrenalina': adrenalina,
    'presupuesto_diario': presupuesto
})

# Guardar a CSV
df_usuarios.to_csv('usuarios_turismo_yucatan.csv', index=False)
print("✅ Dataset de usuarios generado exitosamente: usuarios_turismo_yucatan.csv")
print(df_usuarios.head())