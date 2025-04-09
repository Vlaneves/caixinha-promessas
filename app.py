from flask import Flask, render_template, request, jsonify
import random
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ======================
# CONFIGURAÇÕES
# ======================
# Define o caminho absoluto para a pasta do projeto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Pasta onde estão os arquivos de promessas
PROMESSAS_DIR = os.path.join(BASE_DIR, 'data')
# Cria a pasta se não existir
os.makedirs(PROMESSAS_DIR, exist_ok=True)

# ======================
# FUNÇÕES PRINCIPAIS
# ======================
def carregar_promessas():
    """Carrega promessas com tratamento robusto de erros"""
    promessas = {
        'pt': ['Deus é o nosso refúgio e fortaleza (Salmos 46:1)'],
        'en': ['The Lord is my shepherd (Psalm 23:1)'],
        'es': ['Jehová es mi pastor (Salmo 23:1)']
    }
    
    try:
        for lang in ['pt', 'en', 'es']:
            filepath = os.path.join(PROMESSAS_DIR, f'promessas_{lang}.txt')
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    promessas[lang] = [linha.strip() for linha in f if linha.strip()]
            else:
                # Cria arquivo padrão se não existir
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(promessas[lang]))
                print(f"Arquivo {filepath} criado com promessas padrão")
                
    except Exception as e:
        print(f"ERRO ao carregar promessas: {str(e)}")
        # Fallback para promessas padrão
        promessas = {
            'pt': ['Deus nunca te abandonará (Isaías 41:10)'],
            'en': ['God will never leave you (Isaiah 41:10)'],
            'es': ['Dios nunca te abandonará (Isaías 41:10)']
        }
    
    return promessas

# ======================
# ROTAS PRINCIPAIS
# ======================
@app.route('/')
def home():
    """Rota principal"""
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar_promessa():
    """Gera uma promessa aleatória"""
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
# ROTAS DO BLOG
# ======================
@app.route('/blog/promessas-ansiedade')
def promessas_ansiedade():
    """Rota para o artigo sobre ansiedade"""
    return render_template('blog/promessas-ansiedade.html')

# ======================
# INICIALIZAÇÃO
# ======================
if __name__ == '__main__':
    # Verifica estrutura de arquivos
    print("\n=== ESTRUTURA DE ARQUIVOS ===")
    print(f"Diretório raiz: {BASE_DIR}")
    print(f"Conteúdo da pasta templates: {os.listdir(os.path.join(BASE_DIR, 'templates'))}")
    print(f"Promessas carregadas (PT): {carregar_promessas()['pt'][:3]}")
    
    # Inicia o servidor
    print("\n=== SERVIDOR INICIADO ===")
    app.run(host='0.0.0.0', port=5000, debug=True)
