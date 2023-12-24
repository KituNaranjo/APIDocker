from fastapi import FastAPI\napp = FastAPI()\n@app.get("/")\ndef read_root():\n    return {"Hello": "World"}
