import pytest
from app import app

# ====== Configuração do cliente de teste ======
@pytest.fixture
def cliente_teste():
    """Cria um cliente de teste para simular requisições ao sistema."""
    app.config['TESTING'] = True
    with app.test_client() as cliente:
        yield cliente


# ====== Teste de login inválido ======
def test_login_invalido(cliente_teste):
    """Verifica se o sistema trata corretamente tentativas de login com dados incorretos."""
    resposta = cliente_teste.post('/', data={
        'email': 'teste@teste.com',
        'senha': 'errada'
    }, follow_redirects=True)

    # O sistema deve continuar funcionando e exibir a tela de login ou mensagem de erro
    assert resposta.status_code == 200
    assert (
        b'login' in resposta.data.lower() or
        b'falha' in resposta.data.lower() or
        b'email' in resposta.data.lower()
    )
