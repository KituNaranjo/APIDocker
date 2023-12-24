from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from databases import Database
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Configuración de la base de datos
DATABASE_URL = "postgresql://grupodos:1234@basededatosapi:5432/data_api"
database = Database(DATABASE_URL)

# Modelo de tabla
metadata = MetaData()
tareas = Table(
    "tareas",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(100)),
    Column("tarea", String(255), nullable=False),
)

# Modelo Pydantic para la entrada de la ruta create_tarea
class TareaCreateModel(BaseModel):
    nombre: str
    tarea: str

# Modelo Pydantic para la respuesta de una tarea
class TareaResponseModel(BaseModel):
    id: int
    nombre: str
    tarea: str

app = FastAPI()

# Rutas de la API
@app.on_event("startup")
async def startup_db_client():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()

# Rutas

# Ruta "Hello, World"
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Operaciones CRUD para la tabla "tareas"
@app.post("/tareas/", response_model=TareaResponseModel)
async def create_tarea(tarea_data: TareaCreateModel):
    query = tareas.insert().values(nombre=tarea_data.nombre, tarea=tarea_data.tarea)
    tarea_id = await database.execute(query)
    return TareaResponseModel(id=tarea_id, nombre=tarea_data.nombre, tarea=tarea_data.tarea)

@app.get("/tareas/", response_model=List[TareaResponseModel])
async def read_tareas():
    query = tareas.select()
    return await database.fetch_all(query)

@app.get("/tareas/{tarea_id}", response_model=TareaResponseModel)
async def read_tarea(tarea_id: int):
    query = tareas.select().where(tareas.c.id == tarea_id)
    tarea = await database.fetch_one(query)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return TareaResponseModel(**tarea)

@app.put("/tareas/{tarea_id}", response_model=TareaResponseModel)
async def update_tarea(tarea_id: int, tarea_data: TareaCreateModel):
    query = tareas.update().where(tareas.c.id == tarea_id).values(
        nombre=tarea_data.nombre, tarea=tarea_data.tarea
    )
    await database.execute(query)
    updated_tarea = await database.fetch_one(
        tareas.select().where(tareas.c.id == tarea_id)
    )
    return TareaResponseModel(**updated_tarea)

@app.delete("/tareas/{tarea_id}", response_model=dict)
async def delete_tarea(tarea_id: int):
    query = tareas.delete().where(tareas.c.id == tarea_id)
    deleted_rows = await database.execute(query)
    if not deleted_rows:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"message": "Tarea eliminada con éxito"}

# Nueva ruta para eliminar todas las tareas
@app.delete("/tareas/")
async def delete_all_tareas():
    query = tareas.delete()
    await database.execute(query)
    return {"message": "Todas las tareas han sido eliminadas"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
