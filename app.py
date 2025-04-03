from flask import Flask, render_template, request, redirect
import random
import os

from flask import Flask, render_template, request, redirect
import random
import os

app = Flask(__name__)

# Redirecionamento obrigatório para HTTPS e www
@app.before_request
def enforce_https_and_www():
    # Obter host e protocolo da requisição
    host = request.host.split(':')[0]  # Remove porta se existir
    scheme = request.scheme
    
    # Verificar se precisa redirecionar
    if host == 'caixinhadapromessa.com' or scheme == 'http':
        new_url = request.url.replace(
            'http://', 
            'https://'
        ).replace(
            'caixinhadapromessa.com', 
            'www.caixinhadapromessa.com'
        )
        return redirect(new_url, code=301)

def carregar_promessas():
    return {
        'pt': open('promessas_pt.txt').read().splitlines(),
        'en': open('promessas_en.txt').read().splitlines(),
        'es': open('promessas_es.txt').read().splitlines()
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar_promessa():
    idioma = request.form.get('idioma', 'pt')
    promessas = carregar_promessas()
    return {'promessa': random.choice(promessas[idioma])}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
