from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import aiosqlite

DB_PATH = "quran_bot.db"

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT channel_id, lang FROM channels")
        channels = await cur.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "channels": channels})

@app.post("/add_channel")
async def add_channel(channel_id: int = Form(...), lang: str = Form(...)):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO channels(channel_id, lang) VALUES (?,?)", (channel_id, lang))
        await db.commit()
    return RedirectResponse("/", status_code=303)
