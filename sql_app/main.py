from fastapi import FastAPI, UploadFile, Depends
from pydantic import BaseModel
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session


app = FastAPI()

# basic home_page
@app.get('/{id}/')
def home(id:int, num:str):
    if num:
        return f'home_num: {num}'
    return f'home_id: {id}'


#Request body
class Testitem(BaseModel):
    name:str=23
    id:int=1
    in_stock:bool=False

@app.post("/items/{id}/")
def update_item(id, item: Testitem, number:int=None):
    item.id=id
    result={**item.model_dump()}
    result.update({"number":number})
    return result

# Request files
@app.post('/files/')
async def upload_files(files:list[UploadFile]):
    return (file.filename for file in files)

#Put method
@app.put('/items/{id}/')
def update_item(name:str, id, in_stock:bool, item:Testitem):
    item.name=name
    item.id=id
    item.in_stock=in_stock
    return item

# Posting/Creating a table in database

models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db

    finally:
        db.close()


@app.post('/items/create/')
def create_table (db:Session=Depends(get_db)):
    new_blog=models.Item(title=models.Item.title,description=models.Item.description)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Get blog by query
@app.get('/items/query/{id}')
def get_item(id, db:Session=Depends(get_db)):
    new_item= db.query(models.Item).filter(models.Item.id==id).first()
    return new_item

# Delete body by query
@app.delete('/items/{id}')
def del_item(id, db:Session=Depends(get_db)):
    db.query(models.Item).filter(models.Item.id==id).delete(synchronize_session=False)
    db.commit()
    # db.refresh(db)
    all_blogs=db.query(models.Item).all()
    return all_blogs
