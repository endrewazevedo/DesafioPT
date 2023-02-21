import uvicorn
import time
from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from aux_functions import *
from database import DB

db = DB() # Se não usar o Docker precisa definir as credenciais do banco

templates = Jinja2Templates(directory="templates")

app = FastAPI()

def authenticate(identification: str, password: str):
    """
    It takes an email and password, and returns a boolean indicating whether the user is authenticated

    """
    return db.validate_user(identification, password)

@app.get('/', include_in_schema=False)
def home(request: Request, response: Response):
    """
    If the user has a cookie, redirect them to the dashboard. Otherwise, show them the home page.

    """
    user_id = request.cookies.get("user_id")
    if user_id is not None:
        return RedirectResponse(url='/dashboard')
    return templates.TemplateResponse("home.html", {"request": request})

@app.post('/login', include_in_schema=False)
def login(request: Request, response: Response, login_user: str = Form(...), senha: str = Form(...)):
    """
    It receives a request, a response and two parameters (login_user and senha) and returns a response
    """

    user = authenticate(login_user, senha)

    if user is not None:
        response = RedirectResponse(url='/dashboard')
        response.set_cookie(key="user_id", value=user['email'])
        return response

    return {"message": "Login e/ou senha incorretos"}

@app.get('/dashboard', include_in_schema=False)
def dashboard(request: Request, response: Response):
    """
    If the user_id cookie is not set, redirect to the login page. Otherwise, render the dashboard page
    
    """

    user_id = request.cookies.get("user_id")

    if user_id is None:
        print('Redirecionando')
        return RedirectResponse(url='/')

    return templates.TemplateResponse("logado.html", {"request": request, "user_name": user_id})

@app.post('/dashboard', include_in_schema=False)
def dashboard_post(request: Request, response: Response):
    """
    If the user_id cookie is not set, redirect to the login page. Otherwise, render the dashboard page
    
    """
    user_id = request.cookies.get("user_id")

    if user_id is None:
        print('Redirecionando')
        return RedirectResponse(url='/')

    return templates.TemplateResponse("logado.html", {"request": request, "user_name": user_id})

@app.get('/cadastro_usuario', include_in_schema=False)
def cadastrar_usuario(request: Request, response: Response):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post('/insert_db', include_in_schema=False)
def insert_db(request: Request, response: Response, nome: str = Form(...), email: str = Form(...), pais: str = Form(...), estado: str = Form(...), municipio: str = Form(...), cep: str = Form(...), rua: str = Form(...), numero: str = Form(...), complemento: str = Form(...), cpf: str = Form(...), pis: str = Form(...), senha: str = Form(...)):

    if is_validCPF(cpf):
        print(cpf)
        data_usuario = (nome, email, pais, estado, municipio, cep, rua, numero, complemento, cpf, pis, senha)
        db.insert_new_user(data_usuario)
    
    else:
        return 'CPF Inválido'

    return templates.TemplateResponse("home.html", {"request": request})

@app.get('/alterar_informacoes', include_in_schema=False)
def alterar_info(request: Request, response: Response):

    user_id = request.cookies.get("user_id")

    if user_id is None:
        return RedirectResponse(url='/')

    user = db.search_user_to_edit(user_id)

    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})

@app.post('/edit_user_db', include_in_schema=False)
def edit_user_db(request: Request, response: Response, id: str = Form(...), nome: str = Form(...), email: str = Form(...), pais: str = Form(...), estado: str = Form(...), municipio: str = Form(...), cep: str = Form(...), rua: str = Form(...), numero: str = Form(...), complemento: str = Form(...), cpf: str = Form(...), pis: str = Form(...), senha: str = Form(...)):
    data_usuario = (nome, email, pais, estado, municipio, cep, rua, numero, complemento, cpf, pis, senha, id)
    db.edit_user_db(data_usuario)
    return templates.TemplateResponse("logado.html", {"request": request, "user_name": email})

@app.post('/delete_user', include_in_schema=False)
def exclude_user_db(request: Request, response: Response, id: str = Form(...)):
    """
    It deletes the user from the database and deletes the cookie.
    """
    db.exclude_user(id) 
    response = templates.TemplateResponse("home.html", {"request": request})
    response.set_cookie(key="user_id", value=None, expires = 0)
    return response

@app.get('/logout', include_in_schema=False)
def logout(request: Request, response: Response):
    """
    It redirects the user to the home page and deletes the cookie

    """
    response = templates.TemplateResponse("home.html", {"request": request})
    response.set_cookie(key="user_id", value=None, expires = 0)

    time.sleep(2)

    return response
@app.post('/get_users')
def get_users():
    """
    It takes in a user id, a field, and new information, and then it edits the user's information in the
    database
    
    :param id: the id of the user\n
    :param field: the field you want to edit (nome, email, país, estado, municipio, cep, rua, numero, complemento, cpf, pis, senha)\n
    :param new_info: the new info that the user wants to change\n
    """
    return db.get_users()

@app.post('/edit_user')
def edit_user(id, field, new_info):
    """
    It takes in a user id, a field, and new information, and then it edits the user's information in the
    database
    
    :param id: the id of the user\n
    :param field: the field you want to edit (nome, email, país, estado, municipio, cep, rua, numero, complemento, cpf, pis, senha)\n
    :param new_info: the new info that the user wants to change\n
    """
    return db.edit_some_info_user(id, field, new_info)

@app.post('/exclude_user')
def exclude_user(id):
    """
    It takes in a user id, a field, and new information, and then it edits the user's information in the
    database
    
    :param id: the id of the user\n
    :param field: the field you want to edit (nome, email, país, estado, municipio, cep, rua, numero, complemento, cpf, pis, senha)\n
    :param new_info: the new info that the user wants to change\n
    """
    return db.exclude_user(id)

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True) #No Docker 
#    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True) #Docker http://localhost:8000/
