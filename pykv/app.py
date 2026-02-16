from fastapi import FastAPI
from pykv.features.store.kv_store import PyKVStore

app = FastAPI()
kv = PyKVStore(capacity=5)

@app.post("/set")
def set_kv(item: dict):
    kv.set(item["key"], item["value"])
    return {"message": "Stored"}

@app.get("/get/{key}")
def get_kv(key: str):
    val = kv.get(key)
    if val is None:
        return {"error": "Not found"}
    return {"value": val}

@app.delete("/delete/{key}")
def delete_kv(key: str):
    return {"deleted": kv.delete(key)}

@app.get("/all")
def show_all():
    return kv.all()
