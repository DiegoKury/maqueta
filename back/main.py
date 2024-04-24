from fastapi import FastAPI, Security, HTTPException, UploadFile, File, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import APIKeyHeader, Depends
import pandas as pd
from io import StringIO
from pydantic import BaseModel
from typing import List

API_KEY = "your_api_key"
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class ItemCreate(BaseModel):
    name: str
    description: str

class Item(ItemCreate):
    id: int

db: List[Item] = []

api_router = APIRouter()

@api_router.get("/items", response_model=List[Item])
async def read_items():
    print('here!')
    return db

@api_router.post("/items", response_model=Item)
async def create_item(item: ItemCreate):
    new_item = Item(id=len(db) + 1, **item.dict())
    db.append(new_item)
    return new_item

@api_router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    for i, db_item in enumerate(db):
        if db_item.id == item_id:
            db[i] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@api_router.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for i, db_item in enumerate(db):
        if db_item.id == item_id:
            del db[i]
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        file_location = f"files/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        return {"info": f"file '{file.filename}' saved at '{file_location}'"}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/items/csv")
def get_items_csv():
    df = pd.DataFrame(db)
    stream = StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]),
                                 media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response
    
@app.get("/secure-endpoint/")
def secure_endpoint(api_key: str = Depends(get_api_key)):
    return {"message": "Secure endpoint reached"}

@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "title": "HTTPException",
            "status": exc.status_code,
            "detail": exc.detail,
        },
    )


app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
