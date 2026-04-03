
import time
import uvicorn

from fastapi import FastAPI, Request
from routers.auth_routes import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

# --- APP ---
app = FastAPI(title="FastAPI Project")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- Middleware -----
@app.middleware("http")
async def process_time_middleware(request: Request, call_next):
    """API Process Time"""

    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    process_time = end_time - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-App-Name"] = "Auth App"
    return response

# --- Adding Routes ---
app.include_router(auth_router)











if __name__ == '__main__':

    uvicorn.run("app.main:app", host="127.0.0.1", port=8004, reload=True)




