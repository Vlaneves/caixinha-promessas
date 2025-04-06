from flask import Flask, render_template, request, redirect, jsonify
import random
import os

app = Flask(__name__)

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

if __name__ == '__main__':
    # Configurações para deploy no Render
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Modo debug apenas em desenvolvimento
    debug = os.environ.get('DEBUG', 'false').lower() in ('true', '1', 'on')
    
    app.run(host=host, port=port, debug=debug)
