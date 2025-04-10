from flask import Flask, render_template, request, redirect, jsonify, flash, url_for
import random
import os
from flask_mail import Mail, Message  # Adicionando suporte a e-mail (opcional)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'uma-chave-secreta-padrao')  # Necessário para flash messages

# Configurações do Flask-Mail (opcional - descomente se quiser enviar e-mails)
# app.config['MAIL_SERVER'] = 'smtp.seuprovedor.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# app.config['MAIL_DEFAULT_SENDER'] = 'contato@caixinha.com.br'
# mail = Mail(app)

# Configurações de segurança e redirecionamento
@app.before_request
def handle_redirections():
    """
    Gerencia redirecionamentos de forma segura, evitando loops.
    """
    # Só aplica redirecionamentos em produção (Render)
    if os.environ.get('RENDER', '').lower() not in ('true', '1', 'on'):
        return

    original_url = request.url
    new_url = None

    # 1. Redireciona HTTP para HTTPS
    if request.scheme == 'http':
        new_url = original_url.replace('http://', 'https://', 1)
    
    if new_url and new_url != original_url:
        return redirect(new_url, code=301)

def carregar_promessas():
    """Carrega as promessas dos arquivos de texto"""
    promessas = {
        'pt': [],
        'en': [],
        'es': []
    }
    
    try:
        with open('promessas_pt.txt', 'r', encoding='utf-8') as f:
            promessas['pt'] = [linha.strip() for linha in f if linha.strip()]
        
        with open('promessas_en.txt', 'r', encoding='utf-8') as f:
            promessas['en'] = [linha.strip() for linha in f if linha.strip()]
        
        with open('promessas_es.txt', 'r', encoding='utf-8') as f:
            promessas['es'] = [linha.strip() for linha in f if linha.strip()]
    
    except FileNotFoundError as e:
        print(f"Erro ao carregar arquivos: {e}")
    
    return promessas

# --- Rotas Principais ---
@app.route('/')
def home():
    """Rota principal que renderiza a página inicial"""
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar_promessa():
    """Rota para gerar promessas aleatórias"""
    idioma = request.form.get('idioma', 'pt')
    promessas = carregar_promessas()
    
    if not promessas[idioma]:
        return jsonify({'erro': 'Nenhuma promessa encontrada para o idioma selecionado'}), 400
    
    return jsonify({'promessa': random.choice(promessas[idioma])})

# --- Rotas Institucionais ---
@app.route('/politica-privacidade')
def politica_privacidade():
    """Página de Política de Privacidade"""
    return render_template('politica-privacidade.html')

@app.route('/termos-uso')
def termos_uso():
    """Página de Termos de Uso"""
    return render_template('termos-uso.html')

@app.route('/quem-somos')
def quem_somos():
    """Página Quem Somos"""
    return render_template('quem-somos.html')

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    """Página de Contato com formulário funcional"""
    if request.method == 'POST':
        # Captura os dados do formulário
        nome = request.form.get('nome')
        email = request.form.get('email')
        mensagem = request.form.get('mensagem')
        
        # Validação básica
        if not all([nome, email, mensagem]):
            flash('Por favor, preencha todos os campos do formulário.', 'danger')
            return redirect(url_for('contato'))
        
        # Aqui você pode:
        # 1. Salvar em um banco de dados (recomendado para produção)
        salvar_contato(nome, email, mensagem)
        
        # 2. Enviar por e-mail (opcional - requer configuração do Flask-Mail)
        # enviar_email_contato(nome, email, mensagem)
        
        # Mensagem de sucesso
        flash('Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.', 'success')
        return redirect(url_for('contato'))
    
    return render_template('contato.html')

def salvar_contato(nome, email, mensagem):
    """Salva o contato em um arquivo simples (substitua por banco de dados se necessário)"""
    try:
        with open('contatos.txt', 'a', encoding='utf-8') as f:
            f.write(f"{nome}|{email}|{mensagem}\n")
    except Exception as e:
        print(f"Erro ao salvar contato: {e}")

# Função opcional para enviar e-mail
# def enviar_email_contato(nome, email, mensagem):
#     try:
#         msg = Message(
#             subject=f"Novo contato de {nome}",
#             recipients=['seu-email@provedor.com'],
#             body=f"De: {nome} <{email}>\n\n{mensagem}"
#         )
#         mail.send(msg)
#     except Exception as e:
#         print(f"Erro ao enviar e-mail: {e}")

if __name__ == '__main__':
    # Configurações para deploy no Render
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Modo debug apenas em desenvolvimento
    debug = os.environ.get('DEBUG', 'false').lower() in ('true', '1', 'on')
    
    app.run(host=host, port=port, debug=debug)
