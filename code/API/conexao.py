import mysql.connector

mydb = mysql.connector.connect(
    host="database-3.cpeta6jvoozv.us-east-1.rds.amazonaws.com",
    user='admin',
    password='urubu100',
    database="no_copy"
)
mycursor = mydb.cursor()

def logar(email, senha):
    if email == '' or senha == '':
        return ("Campo vazio!"), 400
    select = f"select case when count(*)=0 then 0 else idCliente end from usuario where email='{email}' and senha='{senha}';"
    mycursor.execute(select)
    codigo = mycursor.fetchone()[0]
    if(codigo>0):
        select = f"select nome from usuario where idCliente={codigo};"
        mycursor.execute(select)
        nome = mycursor.fetchone()[0]
        return ('Logado'), 200, codigo, nome
    else:
        return ('Senha ou Email errado'), 404

def cadastro(nome, email, senha, nascimento):
    select = f"select count(*) from usuario where email='{email}'"
    mycursor.execute(select)
    if email == '' or senha == '' or nome == '' or nascimento == '':
        return "Campo vazio!", 400
    if(mycursor.fetchone()[0]>0):
        return 'Email ja cadastrado', 409
    else:
        inserir = f"""insert into usuario (nome, email, senha, nascimento)
        values ('{nome}', '{email}', '{senha}', '{nascimento}');"""
        inserir = inserir.replace('\n',' ')
        try:
            mycursor.execute(inserir)
        except:
            return f"Erro encontrado {inserir}", 404
        else:
            mydb.commit()
            return 'inserido com sucesso', 201