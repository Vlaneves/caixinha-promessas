from flask import Flask, render_template, request, redirect, jsonify, send_from_directory
import random
import os

app = Flask(__name__)

# Configurações de segurança e redirecionamento
@app.before_request
def handle_redirections():
    """
    Gerencia redirecionamentos de forma segura, evitando loops.
    """
    # Ignora requisições para favicon (evita redirecionamentos desnecessários)
    if request.path == '/favicon.ico':
        return
    
    # Só aplica redirecionamentos em produção (Render)
    if os.environ.get('RENDER', '').lower() not in ('true', '1', 'on'):
        return

    original_url = request.url
    new_url = None

    # 1. Redireciona HTTP para HTTPS
    if request.scheme == 'http':
        new_url = original_url.replace('http://', 'https://', 1)
    
    # 2. Remove www. se necessário (opcional - descomente se quiser forçar sem www)
    # elif request.host.startswith('www.'):
    #     new_url = original_url.replace('www.', '', 1)

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

# Nova rota para favicon (solução definitiva)
@app.route('/favicon.ico')
def favicon():
    """Rota para servir o favicon corretamente"""
    return send_from_directory(os.path.join(app.root_path, 'static'),
                             'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/gerar', methods=['POST'])
def gerar_promessa():
    """Rota para gerar promessas aleatórias"""
    idioma = request.form.get('idioma', 'pt')
    promessas = carregar_promessas()
    
    if not promessas[idioma]:
        return jsonify({'erro': 'Nenhuma promessa encontrada para o idioma selecionado'}), 400
    
    return jsonify({'promessa': random.choice(promessas[idioma])})

# --- Novas Rotas para AdSense ---
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

@app.route('/contato')
def contato():
    """Página de Contato (Opcional)"""
    return render_template('contato.html')

if __name__ == '__main__':
    # Configurações para deploy no Render
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Modo debug apenas em desenvolvimento
    debug = os.environ.get('DEBUG', 'false').lower() in ('true', '1', 'on')
    
    app.run(host=host, port=port, debug=debug)
