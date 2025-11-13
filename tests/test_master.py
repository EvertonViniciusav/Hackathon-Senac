# ====== Testes de variáveis de ambiente ======

# Verifica se a variável MASTER_EMAIL está configurada no arquivo .env
def test_variavel_master_email():
    import os
    assert 'MASTER_EMAIL' in os.environ, "A variável MASTER_EMAIL não está definida no .env"


# Verifica se a variável SECRET_KEY está configurada no arquivo .env
def test_variavel_secret_key():
    import os
    assert 'SECRET_KEY' in os.environ, "A variável SECRET_KEY não está definida no .env"
