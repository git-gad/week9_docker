from fastapi import FastAPI
from pydantic import BaseModel, Field
import json
from pathlib import Path
# from uuid import uuid4

app = FastAPI(title="Shopping List", version="1.0.0")

class Item(BaseModel):
    # id: str = Field(default_factory=lambda: uuid4().hex)
    name: str
    quantity: int

DB_PATH = Path('db/shopping_list.json')

def create_db_if_abscent() -> None:
    if not DB_PATH.exists():
        with open(DB_PATH, 'w') as f:
            json.dump([], f, indent=2)
            

def load_database() -> list:
    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ValueError("Database file is not valid JSON.")
  
    
def save_database(data: list) -> None:
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)
  
        
@app.on_event("startup")
async def startup_event():
    create_db_if_abscent()


@app.get('/items')
async def get_items():
    data = load_database()
    return data


@app.post('/items')
async def post_item(item: Item):
    data = load_database()
    item = item.model_dump()
    if not data:
        item_id = 1
    else:
        item_id = data[-1]['id'] + 1
    item['id'] = item_id
    data.append(item)
    save_database(data)
    return {
        'message': 'successful post'
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)