from flask import Flask, render_template, request, jsonify
import random
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ======================
# CONFIGURAÇÕES CRÍTICAS
# ======================
PROMESSAS_PATH = os.path.join(os.path.dirname(__file__))  # Pasta atual

# ======================
# FUNÇÕES PRINCIPAIS
# ======================
def carregar_promessas():
    """Carrega promessas com tratamento robusto de erros"""
    promessas = {'pt': ['Erro: Arquivo não encontrado'], 
                 'en': ['Error: File not found'],
                 'es': ['Error: Archivo no encontrado']}
    
    try:
        for lang in ['pt', 'en', 'es']:
            filepath = os.path.join(PROMESSAS_PATH, f'promessas_{lang}.txt')
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    promessas[lang] = [linha.strip() for linha in f if linha.strip()]
            else:
                print(f"AVISO: Arquivo {filepath} não encontrado!")
                
    except Exception as e:
        print(f"ERRO GRAVE em carregar_promessas: {str(e)}")
    
    return promessas

# ======================
# ROTAS PRINCIPAIS
# ======================
@app.route('/')
def home():
    """Rota principal garantida"""
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar_promessa():
    """Rota crítica com fallback"""
    try:
        idioma = request.form.get('idioma', 'pt')
        if idioma not in ['pt', 'en', 'es']:
            idioma = 'pt'
            
        promessas = carregar_promessas()
        versiculo = random.choice(promessas[idioma])
        
        return jsonify({
            'promessa': versiculo,
            'status': 'sucesso'
        })
        
    except Exception as e:
        print(f"ERRO em /gerar: {str(e)}")
        return jsonify({
            'promessa': 'Deus nunca te abandona (Is 41:10)',
            'status': 'erro'
        })

# ======================
# INICIALIZAÇÃO
# ======================
if __name__ == '__main__':
    # DEBUG: Mostra o caminho dos arquivos
    print(f"DEBUG - Diretório atual: {os.listdir(PROMESSAS_PATH)}")
    print(f"DEBUG - Conteúdo PT: {carregar_promessas()['pt'][:2]}")
    
    app.run(host='0.0.0.0', port=5000)
