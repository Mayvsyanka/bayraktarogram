from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.routes import auth, users, comments, tags, images, access, transform_photo, find, ratings, message

from src.conf.config import settings

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(images.router, prefix='/api')
app.include_router(ratings.router, prefix='/api')
app.include_router(transform_photo.router, prefix='/api')
app.include_router(message.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(comments.router, prefix='/api')
app.include_router(access.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(find.router, prefix='/api')


@app.get("/", tags=["Root"])
def read_root():
    """
    The read_root function returns a dictionary with the key &quot;message&quot; and value &quot;Welcome to Ghostgram&quot;.
    
    
    :return: A dictionary with a key of message and a value of &quot;welcome to ghostgram&quot;
    :rtype: dict
    """
    return {"message": "Welcome to Ghostgram"}


