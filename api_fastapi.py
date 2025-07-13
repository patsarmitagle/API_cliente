from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import random
import uuid
import os
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
    id_cliente = str(uuid.uuid4())  # Generar UUID único
    nombre = random.choice(["Selena", "Carlos", "María", "Juan", "Lucía"])
    apellido1 = random.choice(["Gibert", "Pérez", "González", "Ramírez"])
    apellido2 = random.choice(["Vicente", "López", "Díaz", "Rodríguez"])
    nuevo = {
        "id_cliente": id_cliente,
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
        if os.path.exists(archivo):
            header = not pd.read_csv(archivo).empty
            df.to_csv(archivo, mode='a', header=header, index=False)
        else:
            df.to_csv(archivo, index=False)
    except Exception as e:
        print("Error al guardar el archivo:", e)
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {e}")

    return {
    "msg": "Cliente registrado",
    "id_cliente": id_cliente,
    "nombres": nuevo["nombres"],
    "primer_apellido": nuevo["primer_apellido"],
    "num_telefono": nuevo["num_telefono"]
    }

@app.get("/registros")
def obtener_registros():
    try:
        df = pd.read_csv(archivo)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        return []
        
@app.get("/registro/{telefono}")
def obtener_registro_por_telefono(telefono: str):
    try:
        df = pd.read_csv(archivo)

        # Filtrar registros válidos que coincidan con el número
        df_filtrado = df[
            (df["num_telefono"] == telefono)
            #&
            #(df["num_identificacion"] != "num_identificacion")
        ]
        print("Coincidencias:", len(df_filtrado))
        
        if df_filtrado.empty:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        # Tomar el último registro válido
        ultimo = df_filtrado.iloc[-1].to_dict()
        return ultimo

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
        print("Número recibido:", telefono)
        print("Cantidad de registros:", len(df))
    

@app.get("/ping")
def ping():
    return {"status": "ok"}
