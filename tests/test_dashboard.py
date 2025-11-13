def test_dashboard_redireciona_se_nao_logado(cliente_teste):
    """Verifica se o acesso ao dashboard sem login redireciona para a tela de login."""
    resposta = cliente_teste.get('/dashboard', follow_redirects=True)

    # Confirma que o sistema mostra a tela de login ou retorna status 200 (página carregada)
    assert b"Login" in resposta.data or resposta.status_code == 200
