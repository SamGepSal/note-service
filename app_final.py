from fastapi import FastAPI

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

