import shutil
from fastapi import FastAPI, UploadFile, File, Response, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from manager.manager import Manager
import os
import magic

app = FastAPI()

# Configure CORS settings
allowed_origins = [
    "https://audiocensor.com"
]

# # # Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# # Middleware to block origins
@app.middleware("http")
async def check_cors_origin(request: Request, call_next):
    origin = request.headers.get("origin")
    if origin not in allowed_origins:
        return Response("Not allowed", status_code=403)
    response = await call_next(request)
    response.headers["access-control-allow-origin"] = origin
    return response

@app.post("/censor/{userID}")
async def root(userID: str, file: UploadFile = File(...)):
    # Download file locally.
    file_path = os.path.join(f"uploads/{userID}/{file.filename}")
    os.makedirs(f"uploads/{userID}", exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Validate file type.
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path)

    if("audio" not in mime_type and "video" not in mime_type):
        shutil.rmtree(f"uploads/{userID}")
        return Response(content="Invalid File Format, the file must be either an audio or video file", status_code=400, media_type="text/plain")

    try:
        Manager.censor_file(file_path, mime_type)
    except Exception as error: 
        return Response(content=f"{error}", status_code=400, media_type="text/plain")
    
    return Response(status_code=200)


@app.post("/transcribe/{userID}")
async def root(userID: str, file: UploadFile = File(...)):
    # Download file locally.
    file_path = os.path.join(f"uploads/{userID}/{file.filename}")
    os.makedirs(f"uploads/{userID}", exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Validate file type.
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path)

    if("audio" not in mime_type and "video" not in mime_type):
        shutil.rmtree(f"uploads/{userID}")
        return Response(content="Invalid File Format, the file must be either an audio or video file", status_code=400, media_type="text/plain")

    transcript = ""
    try:
        transcript = Manager.transcribe_file(file_path)
    except Exception as error: 
        return Response(content=f"{error}", status_code=400, media_type="text/plain")
    
    return Response(content=transcript, status_code=200, media_type="text/plain")


@app.post("/caption/{userID}")
async def root(userID: str, file: UploadFile = File(...)):
    # Download file locally.
    file_path = os.path.join(f"uploads/{userID}/{file.filename}")
    os.makedirs(f"uploads/{userID}", exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Validate file type.
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path)

    if("video" not in mime_type):
        shutil.rmtree(f"uploads/{userID}")
        return Response(content="Invalid File Format, the file must be a valid video file", status_code=400, media_type="text/plain")
    
    try:
        Manager.add_closed_captions(file_path)
    except Exception as error: 
        return Response(content=f"{error}", status_code=400, media_type="text/plain")
    
    return Response(status_code=200)
