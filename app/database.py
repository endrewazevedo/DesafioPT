import mysql.connector
import os

# host='mysql-container',
# port=3307,

class DB():
    def __init__(self):

        self.cnx = mysql.connector.connect( #Docker Database
            user='root',
            password='Desafioponto123',
            host='172.17.0.2',
            database='desafio_ponto'
        )
        self.cursor = self.cnx.cursor()

        # self.cnx = mysql.connector.connect( ##Local Database
        #     user='root',
        #     password='Mundoazuleverde2121!!@',
        #     host='127.0.0.1',
        #     database='desafio_ponto'
        # )
        # self.cursor = self.cnx.cursor()

    def get_users(self):
        query = "SELECT * FROM usuarios"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def backup(self): #Used in docker
        backup_path = os.path.join(os.getcwd(), 'backup.sql')
        dumpcmd = f"mysqldump -u root -p desafio_ponto > {backup_path}"
        os.system(dumpcmd)
        print("Backup realizado com sucesso")

    def exclude_user(self,id):
        # Inserir as informações do formulário no banco de dados
        try:
            update_usuario = f"""DELETE FROM usuarios WHERE id='{id}'"""
            result = self.cursor.fetchone()
            self.cursor.execute(update_usuario)

            self.cnx.commit()
            
            return "Usuário com id {id} excluído com sucesso"
        except Exception as e:
            print(e)
            return f"Ocorreu um erro ao tentar excluir o usuário de id {id}"

    def edit_user_db(self, data_usuario):
        # Inserir as informações do formulário no banco de dados
        try:
            update_usuario = ("UPDATE usuarios SET "
                            "nome=%s, email=%s, pais=%s, estado=%s, municipio=%s, cep=%s, rua=%s, "
                            "numero=%s, complemento=%s, cpf=%s, pis=%s, senha=%s "
                            "WHERE id=%s")

            self.cursor.execute(update_usuario, data_usuario)

            self.cnx.commit()
            return "Alteração feita com sucesso"

        except Exception as e:
            return 'Não foi possível atualizar as informações, verifique se preenche todos os dados corretamente'

    def edit_some_info_user(self, id, field, info):
        # Inserir as informações do formulário no banco de dados
        try:
            print(id, field, info)

            update_usuario = f"""UPDATE usuarios SET {field}='{info}' WHERE id={id}"""

            self.cursor.execute(update_usuario)

            self.cnx.commit()
            return "Alteração feita com sucesso"

        except Exception as e:
            print(e)
            return 'Não foi possível atualizar as informações, verifique se preenche todos os dados corretamente'

    def insert_new_user(self, data_usuario):
        # Inserir as informações do formulário no banco de dados
        try:
            add_usuario = ("INSERT INTO usuarios "
                        "(nome, email, pais, estado, municipio, cep, rua, numero, complemento, cpf, pis, senha) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")


            self.cursor.execute(add_usuario, data_usuario)

            self.cnx.commit()
            return "Usuário cadastrado com sucesso"
        
        except Exception as e:
            return "Erro ao cadastrar"

    def validate_user(self, identification, senha):
        self.cursor = self.cnx.cursor()

        query = (f"""SELECT * FROM usuarios WHERE email = '{identification}' OR cpf = '{identification}' OR pis = '{identification}'""")
        self.cursor.execute(query)
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

    def search_user_to_edit(self, identification):

        query = (f"""SELECT * FROM usuarios WHERE email = '{identification}' OR cpf = '{identification}' OR pis = '{identification}'""")
        self.cursor.execute(query)
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

        return user

    def close_connection(self):
        # Fechar cursor e conexão com o banco de dados
        self.cursor.close()
        self.cnx.close()
