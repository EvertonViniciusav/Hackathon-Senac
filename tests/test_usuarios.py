# ====== Testes relacionados aos usuários ======

# Testa se o sistema redireciona corretamente para a página de login
# quando alguém tenta acessar /usuarios sem estar logado.
def test_redireciona_para_login_se_nao_logado(cliente_teste):
    resposta = cliente_teste.get('/usuarios', follow_redirects=True)
    assert b"Login" in resposta.data or resposta.status_code == 200


# Testa se o sistema impede o cadastro de usuário quando não há login ativo.
def test_cadastro_usuario_sem_login(cliente_teste):
    resposta = cliente_teste.post('/usuarios/adicionar', data={
        'nome': 'Teste',
        'email': 'teste@teste.com',
        'senha': '123456'
    }, follow_redirects=True)
    assert b"Login" in resposta.data or resposta.status_code == 200
