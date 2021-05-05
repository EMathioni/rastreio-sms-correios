from flask import *
from twilio.rest import Client
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
account_sid = 'AC552db2b868861a0d8f21fc3f0cee615b'
auth_token = 'ff17eb32c96d12391847b1d437fae65f'
client = Client(account_sid, auth_token)

code_list = []
rastreio = {
  }
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/enviado')
def search_code():
  code = request.args.get('rastreio')
  tel = request.args.get('tel')
  if len(tel) != 14 or tel == None or code == None or len(code) != 13:
    return redirect('/')
  busca_by_code = f'https://www.linkcorreios.com.br/?id={code}'
  req_code = requests.get(busca_by_code)
  html_page = req_code.text
  html_formated = BeautifulSoup(html_page, 'html.parser')
  status_code = html_formated.find('ul', class_='linha_status m-0')
  modified = ""
  if status_code == None:
    return render_template('index.html', success=False)
  else:
    if 'DistribuiÃ§Ã£o' in status_code.text or 'destinatÃ¡rio' in status_code.text or 'PaÃ­s' in status_code:
      modified = status_code.text.replace('DistribuiÃ§Ã£o', 'Distribuição').replace('destinatÃ¡rio', 'destinatário')\
        .replace('PaÃ­s', 'País').replace('trÃ¢nsito', 'trânsito')
    #client.messages.create(body=f'Último Status do Objeto:\n{modified}', from_='+15035126289', to=f'{tel}')
    rastreio = {
      'code': code,
      'tel': tel
   }
    if rastreio not in code_list:
      code_list.append(rastreio)
    print(code_list)

  return render_template('index.html', success=True, tel=tel)

@app.route('/remover')
def remove_code():
  code = request.args.get('code')
  if code == None or code not in code_list:
    redirect('/remover')

  return render_template('remover.html', code_list=code_list)

@app.route('/removido')
def removed():
  code = request.args.get('code')
  if code in code_list:
    code_list.pop(code)


if __name__ == "__main__":
    app.run()