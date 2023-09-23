import os
import sys
import shutil
from typing import List
from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://0.0.0.0",
    "http://0.0.0.0:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title = "CSI API",
        version = "1.0.0",
        description = "This is a very custom OpenAPI schema",
        contact = {
            "name": "CL, Hsiao",
            "url": "https://github.com/thanatoszeroth",
            "email": "chinlunhsiao@ch-si.com.tw",
        },
        license_info = {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
        routes = app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/", tags = ["Index Docs"])
def index():
    SERVICE_IP = os.getenv("SERVICE_IP", default = "0.0.0.0:13939")
    return {"api_docs": f"http://{SERVICE_IP}/docs"}

@app.post("/vf/file", tags = ["Upload File API"])
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/vf/uploadfile", tags = ["Upload File API"])
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}


@app.post("/vf/uploadfile2save", tags = ["Upload File API"])
async def create_upload_file2save(file: UploadFile = File(...)):
    with open(f"./{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

@app.post("/vf/uploadfile2url", tags = ["Upload File API"])
async def create_upload_file2url(file: UploadFile = File(...)):
    SERVICE_IP = os.getenv("SERVICE_IP", default = "0.0.0.0:13939")
    with open(f"/tmp/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"FileUrl": f"http:/{SERVICE_IP}/tmp/{file.filename}"}


@app.post("/vf/files", tags = ["Upload Multiple File API"])
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/vf/uploadfiles", tags = ["Upload Multiple File API"])
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}
    
    
