from flask import Flask, render_template, request, redirect, session, url_for, flash
from db import conectar
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.jinja_env.globals['now'] = datetime.now
app.secret_key = "segredo_fleet"

# ================= LOGIN =================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        db = conectar()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        db.close()

        if usuario and check_password_hash(usuario['senha'], senha):
            session['usuario_id'] = usuario['id']
            return redirect('/dashboard')
        else:
            return render_template('login.html', erro="Credenciais inválidas")

    return render_template('login.html')


# ================= DASHBOARD =================
@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')

    db = conectar()
    cursor = db.cursor(dictionary=True)
    usuario_id = session['usuario_id']

    # Lista de frotas do usuário
    cursor.execute("SELECT id, nome, tipo FROM frotas WHERE usuario_id = %s", (usuario_id,))
    frotas = cursor.fetchall()

    # Contagem por categoria
    cursor.execute("""
        SELECT tipo, COUNT(*) as total FROM frotas 
        WHERE usuario_id = %s GROUP BY tipo
    """, (usuario_id,))
    contagem = cursor.fetchall()

    # Documentos ordenados por vencimento
    cursor.execute("""
        SELECT f.nome, f.tipo, d.tipo_documento, d.data_vencimento,
               DATEDIFF(d.data_vencimento, CURDATE()) AS dias_restantes
        FROM documentos d
        JOIN frotas f ON f.id = d.frota_id
        WHERE f.usuario_id = %s
        ORDER BY dias_restantes ASC
    """, (usuario_id,))
    documentos = cursor.fetchall()

    db.close()

    return render_template('dashboard.html', frotas=frotas, contagem=contagem, documentos=documentos)

# ================= CADASTRAR FROTA =================
@app.route('/cadastrar_frota', methods=['GET', 'POST'])
def cadastrar_frota():
    if 'usuario_id' not in session:
        return redirect('/')

    if request.method == 'POST':
        nome = request.form['nome']
        tipo = request.form['tipo']

        db = conectar()
        cursor = db.cursor()
        cursor.execute("INSERT INTO frotas (usuario_id, nome, tipo) VALUES (%s,%s,%s)",
                       (session['usuario_id'], nome, tipo))
        db.commit()
        db.close()
        return redirect('/dashboard')

    return render_template('cadastro_frota.html')


# ================= DETALHES DA FROTA =================
@app.route('/frota/<int:frota_id>')
def frota(frota_id):
    if 'usuario_id' not in session:
        return redirect('/')

    db = conectar()
    cursor = db.cursor(dictionary=True)

    # Busca a frota específica do usuário logado
    cursor.execute("SELECT * FROM frotas WHERE id = %s AND usuario_id = %s", (frota_id, session['usuario_id']))
    frota = cursor.fetchone()

    if not frota:
        db.close()
        return redirect('/dashboard')

    # Busca os documentos dessa frota
    cursor.execute("""
        SELECT *, DATEDIFF(data_vencimento, CURDATE()) AS dias_restantes
        FROM documentos
        WHERE frota_id = %s
        ORDER BY data_vencimento ASC
    """, (frota_id,))
    documentos = cursor.fetchall()

    db.close()
    return render_template('frota.html', frota=frota, documentos=documentos)


# ================= CADASTRAR DOCUMENTO =================
@app.route('/cadastrar_documento/<int:frota_id>', methods=['GET', 'POST'])
def cadastrar_documento(frota_id):
    db = conectar()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM frotas WHERE id = %s", (frota_id,))
    frota = cursor.fetchone()

    lista_documentos = {
        'moto': ['IPVA', 'Licenciamento'],
        'carro': ['IPVA', 'Licenciamento'],
        'caminhao': ['IPVA', 'Licenciamento', 'CIV', 'CIPP', 'Inmetro', 'Tacógrafo', 'Cadastro Técnico Federal', 'Autorização Ambiental para o Transporte Interestadual de Produtos Perigosos'],
        'aviao': ['Certificado de Nacionalidade e Matrícula', 'Certificado de Aeronavegabilidade', 'Certificado de Tipo', 'Certificação de Operador Aéreo', 'Autorização de Projeto de Conversão', 'Programas de Manutenção', 'Vistoria', 'Seguro Aeronáutico', 'Documentação Técnica Completa', 'Cumprimento de RBAC 121/135'],
        'trem': ['Autorização de Uso da Infraestrutura', 'Concessão Ferroviária', 'Licença de Operação Ferroviária', 'Inspeção e Fiscalização de Infraestrutura', 'Segurança Operacional e Manutenção']
    }

    if request.method == 'POST':
        tipo_doc = request.form['tipo_documento']
        data_venc = request.form['data_vencimento']
        cursor.execute("INSERT INTO documentos (frota_id, tipo_documento, data_vencimento) VALUES (%s,%s,%s)",
                       (frota_id, tipo_doc, data_venc))
        db.commit()
        db.close()
        return redirect(f'/frota/{frota_id}')

    db.close()
    return render_template('cadastro_documento.html', frota=frota, documentos=lista_documentos[frota['tipo']])

# ================= EXCLUIR DOCUMENTO =================
@app.route('/excluir_documento/<int:documento_id>', methods=['POST'])
def excluir_documento(documento_id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    db = conectar()
    cursor = db.cursor()

    # pega frota_id antes de deletar
    cursor.execute("SELECT frota_id FROM documentos WHERE id = %s", (documento_id,))
    frota = cursor.fetchone()

    if frota:
        frota_id = frota[0]
        cursor.execute("DELETE FROM documentos WHERE id = %s", (documento_id,))
        db.commit()
        db.close()
        return redirect(f'/frota/{frota_id}')
    else:
        db.close()
        return redirect('/dashboard')

# ================= EXCLUIR FROTA =================    
@app.route('/excluir_frota/<int:frota_id>', methods=['POST'])
def excluir_frota(frota_id):
    db = conectar()
    cursor = db.cursor()

    # Exclui documentos vinculados primeiro (por integridade)
    cursor.execute("DELETE FROM documentos WHERE frota_id = %s", (frota_id,))

    # Depois exclui a frota
    cursor.execute("DELETE FROM frotas WHERE id = %s", (frota_id,))
    db.commit()
    db.close()

    return redirect(url_for('dashboard'))

# ================= EDITAR DOCUMENTO =================
@app.route("/editar_documento/<int:doc_id>", methods=["GET", "POST"])
def editar_documento(doc_id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    # Busca o documento no banco de dados
    cursor.execute("SELECT * FROM documentos WHERE id = %s", (doc_id,))
    documento = cursor.fetchone()

    if not documento:
        cursor.close()
        conexao.close()
        flash("Documento não encontrado.", "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        novo_vencimento = request.form["data_vencimento"]

        # Atualiza o vencimento no banco
        cursor.execute("UPDATE documentos SET data_vencimento = %s WHERE id = %s", (novo_vencimento, doc_id))
        conexao.commit()

        flash("Data de vencimento atualizada com sucesso!", "success")

        frota_id = documento.get("frota_id")  # ✅ pega o frota_id corretamente do dicionário
        cursor.close()
        conexao.close()
        return redirect(url_for("frota", frota_id=frota_id))

    cursor.close()
    conexao.close()
    return render_template("editar_documento.html", documento=documento)


if __name__ == "__main__":
    app.run(debug=True)
