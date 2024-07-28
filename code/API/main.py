from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from flasgger import Swagger, swag_from
import conexao as c

app = Flask(__name__)
swagger = Swagger(app)

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" 
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response

# Configurações AWS
S3_BUCKET = 'leitura-arquivo-teste'
AWS_ACCESS_KEY = 'ASIARTIHORATI27BL6VD'
AWS_SECRET_KEY = 'uZSpCl4247yX4jobWt8DvKBooNFXT6XZdgcceg8m'
AWS_SESSION_KEY = 'IQoJb3JpZ2luX2VjEKj//////////wEaCXVzLXdlc3QtMiJIMEYCIQD0/RdFNJAt92z97mZOk9sskJ8xOe6nxBUInen4pUlCRAIhANneKlbHBmhywkacu+jXmyytHU+ECFTmwvZ1qcHkI/0+KrQCCIH//////////wEQARoMMTEwMDc0MTY5MzgyIgxjUUwibdK+Ky143tUqiAJR0obiktZ0TVfWOgN0rglEMHcaMKBobUEvRDM6ruFH1PotlW/UpXLLDlQVVOjuK5/5pN1j5lkW5FrUOuYGFWbM+8srAk5lfmVFRwoE6d+psAiUqQV8q4Dg1o/BcEBNteNC8GbfTnv/XxorQZNO1/rWM3z4gCtepSbPE4ue6o+9jcHB/c8WaNPNDnovxi6NB7HhHsz/3UNsME0Q/LaO/65gARunZjjWO8Z0EH5Jz88zmZGcKA7bQ3LkNMDF2h+McNCERtfS/oY51K3q2SXh+NCsdtSUBikLCU7IVUnRx1ml09N6AlgQtcCOy3c7iYoSj+WkfbZTG50c6az2Y6zUIgL3Bob0kiYaYzgwrdv7tAY6nAFiE7DoMn25XAXKO1vQ9cyrOj4vIRDB/sP/1ZtH6ta1LQ3Z7zLRa1hvDhZoajA+3k+5Bk7Jp4E9gOybssP6GRnSJEw2cGF24M0QrwACqMm8Hj9EMnbz8UGOASLKGOnZ48ua/AHjh8U/J9X6XMIkP8cP+57ee8pG8103re0WhYifRMFyON0whU41soHFKGUNL83bug0UDtDarJYTFW0='

s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY,
                  aws_secret_access_key=AWS_SECRET_KEY,
                  aws_session_token=AWS_SESSION_KEY)

@app.route('/upload/<codigo>', methods=['POST'])
@swag_from({
    'summary': 'Upload de arquivo para o bucket S3',
    'description': 'Envia um arquivo para o bucket S3 especificado.',
    'responses': {
        200: {
            'description': 'Arquivo enviado com sucesso',
            'examples': {
                'application/json': {
                    'message': 'Arquivo <nome> enviado com sucesso para o bucket <bucket>'
                }
            }
        },
        400: {
            'description': 'Erro na requisição',
            'examples': {
                'application/json': {
                    'error': 'Nenhum arquivo encontrado na requisição'
                }
            }
        },
        500: {
            'description': 'Erro no servidor',
            'examples': {
                'application/json': {
                    'error': 'Descrição do erro'
                }
            }
        }
    },
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Arquivo para upload'
        }
    ],
    'tags': ['upload']
})
def upload_file(codigo):
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo encontrado na requisição'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    try:
        nome = file.filename.split('.')

        s3.upload_fileobj(file, S3_BUCKET, f'{nome[0]}_{codigo}.{nome[1]}')
        return jsonify({'message': f'Arquivo {file.filename} enviado com sucesso para o bucket {S3_BUCKET}'}), 200
    except NoCredentialsError:
        return jsonify({'error': 'Credenciais AWS não encontradas'}), 500
    except PartialCredentialsError:
        return jsonify({'error': 'Credenciais AWS incompletas'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/login', methods=['POST'])
@swag_from({
    'summary': 'Login de usuário',
    'description': 'Autentica o usuário.',
    'responses': {
        200: {
            'description': 'Login bem-sucedido',
        },
        404: {
            'description': 'Credenciais inválidas',
        },
        400: {
            'description': 'Campo(s) vazio(s)',
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'senha': {'type': 'string'}
                },
                'required': ['email', 'senha']
            }
        }
    ],
    'tags': ['auth']
})
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    resposta = c.logar(email, senha)
    if resposta[1]==200:
        return jsonify({'message':resposta[0], 'codigo':resposta[2], 'nome':resposta[3]}), 200
    else:
        return jsonify({'error':resposta[0]}), resposta[1] 

@app.route('/cadastro', methods=['POST'])
@swag_from({
    'summary': 'Cadastro de usuário',
    'description': 'Cadastro o usuário.',
    'responses': {
        200: {
            'description': 'Cadastro bem-sucedido',
        },
        404: {
            'description': 'Credenciais inválidas',
        },
        400: {
            'description': 'Campo(s) vazio(s)',
        },
        409: {
            'description': 'Email ja existente',
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'senha': {'type': 'string'},
                    'nascimento': {'type': 'string'},
                    'nome': {'type': 'string'}
                },
                'required': ['email', 'senha', 'nascimento', 'nome']
            }
        }
    ],
    'tags': ['auth']
})
def cadastro():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    nascimento = data.get('nascimento')
    nome = data.get('nome')
    resposta = c.cadastro(nome ,email, senha, nascimento)
    if resposta[1]==200:
        return jsonify({'message':resposta[0]}), 201
    else:
        return jsonify({'error':resposta[0]}), resposta[1] 
if __name__ == '__main__':
    app.run(debug=True)
