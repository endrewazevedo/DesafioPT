import mysql.connector
import os

class DB():
    def __init__(self):

        self.cnx = mysql.connector.connect(
            user='root',
            password='Mundoazuleverde2121!!@',
            host='127.0.0.1',
            database='desafio_ponto'
        )
        self.cursor = self.cnx.cursor()

    def backup(self): #Used in docker
        backup_path = os.path.join(os.getcwd(), 'backup.sql')
        dumpcmd = f"mysqldump -u root -p desafio_ponto > {backup_path}"
        os.system(dumpcmd)
        print("Backup realizado com sucesso")

    def exclude_user(self,id):
        # Inserir as informações do formulário no banco de dados
        update_usuario = f"""DELETE FROM usuarios 
                        WHERE id={id}"""
        self.cursor.execute(update_usuario)

        self.cnx.commit()

        # Fechar cursor e conexão com o banco de dados
        self.cursor.close()
        self.cnx.close()

    def edit_user_db(self, data_usuario):
        # Inserir as informações do formulário no banco de dados
        update_usuario = ("UPDATE usuarios SET "
                        "nome=%s, email=%s, pais=%s, estado=%s, municipio=%s, cep=%s, rua=%s, "
                        "numero=%s, complemento=%s, cpf=%s, pis=%s, senha=%s "
                        "WHERE id=%s")

        self.cnxcursor.execute(update_usuario, data_usuario)

        self.cnxcnx.commit()

        # Fechar cursor e conexão com o banco de dados
        self.cnxcursor.close()
        self.cnxcnx.close()

    def insert_new_user(self, data_usuario):
        # Inserir as informações do formulário no banco de dados
        add_usuario = ("INSERT INTO usuarios "
                    "(nome, email, pais, estado, municipio, cep, rua, numero, complemento, cpf, pis, senha) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")


        self.cursor.execute(add_usuario, data_usuario)

        self.cnx.commit()

        # Fechar cursor e conexão com o banco de dados
        self.cursor.close()
        self.cnx.close()

def validate_user(self, email, senha):

    query = ("SELECT * FROM usuarios WHERE email = %s")
    self.cursor.execute(query, (email,))
    result = self.cursor.fetchone()
    if result is None:
        # Nenhum usuário foi encontrado com o email fornecido
        return None
    
    user = {
    "id": result[0],
    "nome": result[1],
    "email": result[2],
    "pais": result[3],
    "estado": result[4],
    "municipio": result[5],
    "cep": result[6],
    "rua": result[7],
    "numero": result[8],
    "complemento": result[9],
    "cpf": result[10],
    "pis": result[11],
    "senha": result[12]
    }

    if user["senha"] == senha:
        # A senha fornecida corresponde à senha armazenada no banco de dados
        return user

def search_user_to_edit(email):
    cnx = mysql.connector.connect(
    user='root',
    password='Mundoazuleverde2121!!@',
    host='127.0.0.1',
    database='desafio_ponto'
    )

    # Criar cursor para executar comandos no banco de dados
    cursor = cnx.cursor()

    query = ("SELECT * FROM usuarios WHERE email = %s")
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    if result is None:
        # Nenhum usuário foi encontrado com o email fornecido
        return None
    
    user = {
    "id": result[0],
    "nome": result[1],
    "email": result[2],
    "pais": result[3],
    "estado": result[4],
    "municipio": result[5],
    "cep": result[6],
    "rua": result[7],
    "numero": result[8],
    "complemento": result[9],
    "cpf": result[10],
    "pis": result[11],
    "senha": result[12]
    }

    return user

db = DB()

db.backup()