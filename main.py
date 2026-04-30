from fastapi import FastAPI,Depends,HTTPException
import httpx
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from auth import hash_password
from auth import verify_password,create_access_token,get_current_user
from schemas import UserCreate,UserLogin
import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def home():
    return {"message":"Welcome please use /docs in url"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fetch_jisho_word(word:str):
    url = f"https://jisho.org/api/v1/search/words?keyword={word}"
    response = httpx.get(url)
    data = response.json()

    if not data["data"]:
        raise HTTPException(status_code=404,detail="Word not found")

    result = data["data"][0]

    return{
        "japanese" : result["japanese"][0].get("word",""),
        "reading" : result["japanese"][0].get("reading",""),
        "meaning" : ",".join(result["senses"][0]["english_definitions"])
    }   


@app.get("/search")
def search(word:str):
    data = fetch_jisho_word(word)

    return{
        "query":word,
        **data
    }

@app.post("/add")
def add_word(word:str,user_id:int = Depends(get_current_user),db:Session=Depends(get_db)):
    data = fetch_jisho_word(word)

    japanese = data["japanese"]
    reading = data["reading"]
    meaning = data["meaning"]

    check_value = japanese or reading
    already_exists = db.query(models.Word).filter(models.Word.japanese == check_value,models.Word.owner_id==user_id).first()

    if already_exists:
        raise HTTPException(status_code=409,detail="Word already exists")

    new_word = models.Word(
        japanese=japanese,
        reading=reading,
        meaning=meaning,
        owner_id = user_id
    )

    db.add(new_word)
    db.commit()

    return{
        "message":"word added",
        "word": word
    }

@app.get("/learning")
def get_learning(user_id:int=Depends(get_current_user),db:Session=Depends(get_db)):

    words = db.query(models.Word).filter(models.Word.status=="learning",models.Word.owner_id==user_id).all()
    
    return [
        {
            "id":w.id,
            "japanese":w.japanese,
            "reading":w.reading,
            "meaning":w.meaning
        }
        for w in words

    ]

@app.put("/mark-known")
def mark_known(id:int,user_id:int=Depends(get_current_user),db:Session=Depends(get_db)):

    word = db.query(models.Word).filter(models.Word.id==id,models.Word.owner_id==user_id).first()
    
    if not word:
        raise HTTPException(status_code=404,detail="Word not found")
    if word.status == "known":
        raise HTTPException(status_code=400,detail="Word already marked as known")
    
    word.status = "known"

    db.commit()

    return {"message":"Marked as known"}

@app.get("/known")
def get_known(user_id:int=Depends(get_current_user),db:Session=Depends(get_db)):

    words = db.query(models.Word).filter(models.Word.status=="known",models.Word.owner_id==user_id).all()

    return [
        {
            "japanese":w.japanese,
            "reading":w.reading,
            "meaning":w.meaning
        }
        for w in words
    ]

@app.delete("/delete")
def delete(id:int,user_id:int=Depends(get_current_user),db:Session=Depends(get_db)):

    word = db.query(models.Word).filter(models.Word.id==id,models.Word.owner_id==user_id).first()

    if not word:
        raise HTTPException(status_code=404,detail="Word not found")
    
    db.delete(word)
    db.commit()

    return{"message":"Word Deleted"}

@app.post("/register")
def register(data:UserCreate,db:Session=Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == data.email).first()

    if existing_user:
        raise HTTPException(status_code=409,detail="User already exists")
    
    hashed_password = hash_password(data.password)

    new_user = models.User(
        username=data.username,
        email=data.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return {"message":"Registered successfully"}

@app.post("/login")
def login(data:UserLogin,db:Session=Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    if not verify_password(data.password,user.password):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    
    token = create_access_token({"user_id":user.id})

    return {
        "access_token":token,
        "token_type":"bearer"
    }