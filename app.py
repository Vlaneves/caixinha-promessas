from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

# --- Carregamento das Promessas (Método garantido) ---
def carregar_promessas():
    promessas = {'pt': [], 'en': [], 'es': []}
    try:
        for lang in promessas.keys():
            with open(f'promessas_{lang}.txt', 'r', encoding='utf-8') as f:
                promessas[lang] = [linha.strip() for linha in f if linha.strip()]
    except Exception as e:
        print(f"ERRO CRÍTICO: {str(e)}")
    return promessas

# --- Rotas Principais (Idênticas à versão original) ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar_promessa():
    idioma = request.form.get('idioma', 'pt')
    promessas = carregar_promessas()
    
    if not promessas[idioma]:
        return jsonify({'erro': 'Nenhuma promessa encontrada'}), 400
    
    return jsonify({'promessa': random.choice(promessas[idioma])})

# --- Rotas AdSense (Opcionais) ---
@app.route('/politica-privacidade')
def politica_privacidade():
    return render_template('politica-privacidade.html')

# ... (mantenha as outras rotas legais)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
