from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import auth, users, comments, tags, images, access, transform_photo
from src.conf.config import settings

app = FastAPI()

app.include_router(transform_photo.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(comments.router, prefix='/api')
app.include_router(access.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(images.router, prefix='/api')

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to Ghostgram"}


