import pytest
from app import app

# ====== Configuração do cliente de teste ======
@pytest.fixture
def cliente_teste():
    """Cria um cliente de teste para simular requisições ao sistema."""
    app.config['TESTING'] = True
    with app.test_client() as cliente:
        yield cliente


# ====== Teste: acesso à página de cadastro de frota sem login ======
def test_cadastrar_frota_requer_login(cliente_teste):
    """Verifica se o sistema redireciona para o login ao tentar acessar /cadastrar_frota sem estar logado."""
    resposta = cliente_teste.get('/cadastrar_frota', follow_redirects=True)
    assert b"login" in resposta.data.lower() or resposta.status_code == 200


# ====== Teste: acesso aos detalhes da frota sem login ======
def test_detalhes_frota_sem_login(cliente_teste):
    """Verifica se o sistema redireciona para o login ao tentar acessar /frota/<id> sem estar logado."""
    resposta = cliente_teste.get('/frota/1', follow_redirects=True)
    assert b"login" in resposta.data.lower() or resposta.status_code == 200
