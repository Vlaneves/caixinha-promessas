from flask import Flask, render_template, request
import random
import os

app = Flask(__name__)

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
