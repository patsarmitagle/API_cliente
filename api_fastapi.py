from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
archivo = "registro_campania.csv"

# Habilitar CORS para que Streamlit pueda acceder
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir si querés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Registro(BaseModel):
    num_telefono: str

@app.post("/registro")
def registrar_cliente(data: Registro):
    telefono = data.num_telefono.strip()
    nombre = random.choice(["Selena", "Carlos", "María", "Juan", "Lucía"])
    apellido1 = random.choice(["Gibert", "Pérez", "González", "Ramírez"])
    apellido2 = random.choice(["Vicente", "López", "Díaz", "Rodríguez"])
    nuevo = {
        "tipo_id": "C",
        "num_identificacion": str(random.randint(1000000000, 1999999999)),
        "num_telefono": telefono,
        "nombre_completo": f"{nombre} {apellido1} {apellido2}",
        "nombres": nombre,
        "primer_apellido": apellido1,
        "segundo_apellido": apellido2,
        "fecha_nacimiento": "06/03/1990",
        "genero_cliente": random.choice(["FEMENINO", "MASCULINO"]),
        "edad": "35",
        "grupo_pad": "0",
        "cod_ciudad": "0",
        "ciudad": "BOGOTA D.C.",
        "cod_depto": "11",
        "departamento": "BOGOTA D.C.",
        "productos_aprob": "PP/VEH_NUE/VEH_USA/VIV/ROTA/TC/LBZ60/LBZ72/LBZ84/LBZ96",
        "disponible": "1942461.13",
        "gastos_fliar": "1442461.13",
        "disponible_pp": "1692461.13",
        "plazo_pp": "60",
        "tasa_pp": "1.6",
        "monto_pp": "81091707.58",
        "cuota_pp": "1692461.13",
        "Monto_Lbz_60": "74617281.56",
        "Monto_Lbz_72": "80767861.54",
        "Monto_Lbz_84": "73908821.55",
        "Monto_Lbz_96": "77691769.76",
        "Cuota_Lbz_60": "1243621.36",
        "Cuota_Lbz_72": "1121775.85",
        "Cuota_Lbz_84": "879866.92",
        "Cuota_Lbz_96": "809289.27"
    }
    df = pd.DataFrame([nuevo])
    try:
        df.to_csv(archivo, mode='a', header=not pd.read_csv(archivo).shape[0], index=False)
    except:
        df.to_csv(archivo, index=False)
    return {"msg": "Cliente registrado"}

@app.get("/registros")
def obtener_registros():
    try:
        df = pd.read_csv(archivo)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        return []

@app.get("/ping")
def ping():
    return {"status": "ok"}
