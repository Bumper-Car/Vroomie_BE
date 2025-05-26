from fastapi import FastAPI
from app.api.routes import router
from app.api import websocket
app = FastAPI()
app.include_router(router)
app.include_router(websocket.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)