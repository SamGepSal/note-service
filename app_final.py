from fastapi import FastAPI, HTTPException

app = FastAPI(title="Сервис заметок")
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
    raise HTTPException(status_code=404, detail="Заметка не найдена")
