import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def enviar_email(destinatario, assunto, corpo):
    remetente = os.getenv("EMAIL_USER")
    senha = os.getenv("EMAIL_PASS")
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "html"))
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(remetente, senha)
            server.send_message(msg)
        print(f"E-mail enviado para {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar e-mail para {destinatario}: {e}")

def buscar_vencimentos():
    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor = conexao.cursor(dictionary=True)
    hoje = datetime.now().date()
    limite_superior = hoje + timedelta(days=30)
    limite_inferior = hoje - timedelta(days=120)
    query = """
    SELECT 
        f.id AS frota_id,
        f.nome AS nome_frota,
        f.tipo AS tipo_frota,
        d.tipo_documento,
        d.data_vencimento,
        u.nome AS usuario_nome,
        u.email AS usuario_email
    FROM documentos d
    JOIN frotas f ON d.frota_id = f.id
    JOIN usuarios u ON f.usuario_id = u.id
    WHERE d.data_vencimento BETWEEN %s AND %s
    ORDER BY d.data_vencimento ASC
    """
    cursor.execute(query, (limite_inferior, limite_superior))
    dados = cursor.fetchall()
    cursor.close()
    conexao.close()
    return dados

def gerar_relatorio_email():
    vencimentos = buscar_vencimentos()
    usuarios = {}
    for v in vencimentos:
        if v["usuario_email"] not in usuarios:
            usuarios[v["usuario_email"]] = []
        usuarios[v["usuario_email"]].append(v)
    for email, docs in usuarios.items():
        corpo = f"<h2>📅 Olá, {docs[0]['usuario_nome']}!</h2>"
        corpo += "<p>Segue a lista de documentos <b>vencidos</b> e com <b>vencimento nos próximos 30 dias</b>:</p>"
        corpo += """
        <table border='1' cellspacing='0' cellpadding='6' style='border-collapse: collapse; font-family: Arial;'>
            <tr style='background-color: #f2f2f2;'>
                <th>Frota</th>
                <th>Tipo</th>
                <th>Documento</th>
                <th>Data de Vencimento</th>
                <th>Status</th>
            </tr>
        """
        hoje = datetime.now().date()
        for d in docs:
            data_venc = d['data_vencimento']
            dias_restantes = (data_venc - hoje).days
            if dias_restantes < 0:
                status = f"<span style='color:red;'>VENCIDO há {-dias_restantes} dias</span>"
                linha_cor = "#ffe5e5"
            elif dias_restantes == 0:
                status = "<span style='color:red;'>VENCE HOJE</span>"
                linha_cor = "#fff3cd"
            else:
                status = f"<span style='color:orange;'>Vence em {dias_restantes} dias</span>"
                linha_cor = "#fffbe5"
            corpo += f"""
            <tr style='background-color:{linha_cor};'>
                <td>{d['nome_frota']}</td>
                <td>{d['tipo_frota']}</td>
                <td>{d['tipo_documento']}</td>
                <td>{data_venc.strftime('%d/%m/%Y')}</td>
                <td>{status}</td>
            </tr>
            """
        corpo += "</table>"
        corpo += "<p>⚠️ Por favor, verifique e regularize os documentos o quanto antes.</p>"
        enviar_email(email, "📢 Relatório de Documentos Vencidos e a Vencer", corpo)