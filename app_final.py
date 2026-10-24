from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

class NoteCreate(BaseModel):
    title: str
    text: str

app_name = os.getenv("APP_NAME", "Сервис заметок")
app = FastAPI(title=app_name)
notes = [
    {
        "id": 1, 
        "title": "Первая заметка",
        "text": "тест заметка"
    },
    {
        "id": 2, 
        "title": "Вторая заметка",
        "text": "тест 2 заметка"
    }
]

@app.get("/health")
def health():
    return{"status": "ok"}

@app.get("/version")
def version():
    return{"version": "0.1.0"}

@app.get("/notes")
def get_notes():
    return notes

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    logger.warning("Заметка с id=%s не найдена", note_id)
    raise HTTPException(status_code=404, detail="Заметка не найдена")

@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    new_id = 1
    for existing_note in notes:
        if existing_note["id"] >= new_id:
            new_id = existing_note["id"] + 1

    new_note = {
        "id": new_id,
        "title": note.title,
        "text": note.text,
    }

    notes.append(new_note)
    logger.info("Создана заметка с id=%s", new_id)
    return new_note
