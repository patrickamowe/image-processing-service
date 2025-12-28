from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.image_routes import router as image_router
from routes.auth_routes import router as auth_router
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from db.database import Base, engine
from utils.limiter import limiter

app = FastAPI(
    title="Image Processing API",
    description="Backend service for image uploads and transformations",
    version="1.0.0"
)

# Essential setup for SlowAPI
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Create tables
Base.metadata.create_all(bind=engine)


# Routers
app.include_router(user_router)
app.include_router(image_router)
app.include_router(auth_router)

@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to Image Processing Service"}





