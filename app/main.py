import uvicorn
import time
from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, Response, Form
from fastapi import Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import DB

db = DB()

templates = Jinja2Templates(directory="templates")

users = [{'email' : 'teste', 'password' : '123'}]
app = FastAPI()

app.mount("/static", StaticFiles(directory="css"), name="css")

def auter(email: str, password: str):
    print(email, password)

    return db.validate_user(email, password)

@app.get('/')
def home(request: Request, response: Response):
    user_id = request.cookies.get("user_id")
    if user_id is not None:
        return RedirectResponse(url='/dashboard')
    return templates.TemplateResponse("home.html", {"request": request})

@app.post('/login')
def login(request: Request, response: Response, login_user: str = Form(...), senha: str = Form(...)):

    user =  auter(login_user, senha)
    if user is not None:
        response = RedirectResponse(url='/dashboard')
        response.set_cookie(key="user_id", value=login_user)
        return response

    return {"message": "Login e/ou senha incorretos"}

@app.get('/dashboard')
def dashboard(request: Request, response: Response):

    user_id = request.cookies.get("user_id")

    if user_id is None:
        print('Redirecionando')
        return RedirectResponse(url='/')

    return templates.TemplateResponse("logado.html", {"request": request, "user_name": user_id})

@app.post('/dashboard')
def dashboard_post(request: Request, response: Response):

    user_id = request.cookies.get("user_id")

    if user_id is None:
        print('Redirecionando')
        return RedirectResponse(url='/')

    return templates.TemplateResponse("logado.html", {"request": request, "user_name": user_id})

@app.get('/cadastro_usuario')
def cadastrar_usuario(request: Request, response: Response):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post('/insert_db')
def insert_db(request: Request, response: Response, nome: str = Form(...), email: str = Form(...), pais: str = Form(...), estado: str = Form(...), municipio: str = Form(...), cep: str = Form(...), rua: str = Form(...), numero: str = Form(...), complemento: str = Form(...), cpf: str = Form(...), pis: str = Form(...), senha: str = Form(...)):
    data_usuario = (nome, email, pais, estado, municipio, cep, rua, numero, complemento, cpf, pis, senha)
    db.insert_new_user(data_usuario)

    return templates.TemplateResponse("home.html", {"request": request})

@app.get('/alterar_informacoes')
def alterar_info(request: Request, response: Response):

    user_id = request.cookies.get("user_id")

    if user_id is None:
        return RedirectResponse(url='/')

    user = db.search_user_to_edit(user_id)

    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})

@app.post('/edit_user_db')
def edit_user_db(request: Request, response: Response, id: str = Form(...), nome: str = Form(...), email: str = Form(...), pais: str = Form(...), estado: str = Form(...), municipio: str = Form(...), cep: str = Form(...), rua: str = Form(...), numero: str = Form(...), complemento: str = Form(...), cpf: str = Form(...), pis: str = Form(...), senha: str = Form(...)):
    """
    It takes a request, response, and a bunch of form data, and then passes that data to a function
    called edit_db
    
    """
    data_usuario = (nome, email, pais, estado, municipio, cep, rua, numero, complemento, cpf, pis, senha, id)
    db.edit_user_db(data_usuario)

@app.post('/delete_user')
def exclude_user_db(request: Request, response: Response, id: str = Form(...)):
    """
    It deletes the user from the database and deletes the cookie.
    </code>
    
    :param request: Request
    :type request: Request
    :param response: Response
    :type response: Response
    :param id: str = Form(...)
    :type id: str
    """
    db.exclude_user(id) 
    response.set_cookie(key="user_id", value=None, expires = 0)

@app.get('/logout')
def logout(request: Request, response: Response):
    """
    It redirects the user to the home page and deletes the cookie
    
    :param request: Request
    :type request: Request
    :param response: Response
    :type response: Response
    :return: A response object.
    """

    response = RedirectResponse(url='/')

    response.set_cookie(key="user_id", value=None, expires = 0)

    return response

if __name__ == "__main__":
#    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) #No Docker 
   uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) #Docker http://localhost:8000/
