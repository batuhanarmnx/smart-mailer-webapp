import os
from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from pydantic import BaseModel
import pandas as pd
from utils.excel_reader import parse_excel
from utils.mail_sender import send_bulk_emails
import json

app = FastAPI(title="Smart Mailer")
app.add_middleware(SessionMiddleware, secret_key="super-secret-smart-mailer-key")

# OAuth Setup
oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=os.getenv('GOOGLE_CLIENT_ID', ''),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET', ''),
    client_kwargs={
        'scope': 'openid email profile https://www.googleapis.com/auth/gmail.send'
    }
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Storage paths
UPLOAD_DIR = "storage/uploads"
TEMPLATE_DIR = "storage/user_templates"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMPLATE_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login_via_google(request: Request):
    # Google Client ID ve Secret yoksa uyarı ver
    if not os.getenv('GOOGLE_CLIENT_ID'):
        return JSONResponse(content={"error": "Google Client ID ve Secret tanımlanmamış. Lütfen .env veya sistem ortam değişkenlerine ekleyin."}, status_code=400)
    
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
        request.session['access_token'] = token.get('access_token')
    return RedirectResponse(url='/')

@app.get("/logout")
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')

@app.get("/api/me")
async def get_current_user(request: Request):
    user = request.session.get('user')
    if user:
        return {"logged_in": True, "user": user, "has_google_token": bool(request.session.get('access_token'))}
    return {"logged_in": False}

@app.post("/api/upload")
async def upload_excel(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Parse excel
    data = parse_excel(file_path)
    return JSONResponse(content={"filename": file.filename, "data": data})

class SendMailRequest(BaseModel):
    subject: str
    body_template: str
    recipients: list
    smtp_settings: dict = None
    use_google: bool = False

@app.post("/api/send")
async def send_mails(req: SendMailRequest, request: Request, background_tasks: BackgroundTasks):
    google_token = None
    if req.use_google:
        google_token = request.session.get('access_token')
        if not google_token:
            return JSONResponse(status_code=401, content={"status": "error", "message": "Google girişi süresi dolmuş veya hatalı. Lütfen tekrar giriş yapın."})

    # BackgroundTasks will run this after the response is sent
    background_tasks.add_task(send_bulk_emails, req.recipients, req.subject, req.body_template, req.smtp_settings, google_token)
    return JSONResponse(content={"status": "success", "message": "Mail gönderim işlemi arka planda başlatıldı."})

class TemplateRequest(BaseModel):
    name: str
    subject: str
    body: str

@app.post("/api/templates")
async def save_template(req: TemplateRequest):
    template_path = os.path.join(TEMPLATE_DIR, f"{req.name}.json")
    with open(template_path, "w", encoding="utf-8") as f:
        json.dump(req.model_dump(), f, ensure_ascii=False)
    return {"status": "success", "message": "Şablon başarıyla kaydedildi."}

@app.get("/api/templates")
async def list_templates():
    saved_templates = []
    for filename in os.listdir(TEMPLATE_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(TEMPLATE_DIR, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
                saved_templates.append(data)
    return JSONResponse(content={"templates": saved_templates})

@app.get("/api/download-template")
async def download_template():
    # Return a dummy excel template
    path = "storage/sablon.xlsx"
    if not os.path.exists(path):
        df = pd.DataFrame(columns=["Sirket_Adi", "Yetkili_Bilgisi", "Mail_Adresi", "Sektor"])
        df.to_excel(path, index=False)
    return FileResponse(path, filename="sablon.xlsx")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
