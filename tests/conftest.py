import pytest
from app import app
import mysql.connector
import os

# 🔹 Cria um cliente de teste Flask (usado para simular o uso do sistema)
@pytest.fixture
def cliente_teste():
    """Inicializa o cliente de teste do Flask para simular requisições HTTP."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'chave_teste'  # Chave usada apenas nos testes
    with app.test_client() as cliente:
        yield cliente


# 🔹 Cria uma conexão com o banco de dados de teste
@pytest.fixture(scope="module")
def conexao_banco_teste():
    """Conecta ao banco de dados de teste definido no .env."""
    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_TEST_NAME", "hackathon_teste")  # Banco exclusivo de testes
    )

    yield conexao  # Entrega a conexão aos testes
    conexao.close()  # Fecha após todos os testes do módulo terminarem
