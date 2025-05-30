import os
import time
import json
import csv

from random import random
from datetime import datetime
from sys import argv

import pandas as pd
import seaborn as sns
import requests

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

# Captando a taxa CDI do site do BCB

try:
  response = requests.get(url=URL)
  response.raise_for_status()
except requests.HTTPError as exc:
  print("Dado não encontrado, continuando.")
  cdi = None
except Exception as exc:
  print("Erro, parando a execução.")
  raise exc
else:
  dado = json.loads(response.text)[-1]['valor']

# Criando a variável data e hora

for _ in range(0, 10):

  data_e_hora = datetime.now()
  data = datetime.strftime(data_e_hora, '%Y/%m/%d')
  hora = datetime.strftime(data_e_hora, '%H:%M:%S')

  cdi = float(dado) + (random() - 0.5)

  # Verificando se o arquivo "taxa-cdi.csv" existe

  if os.path.exists('./taxa-cdi-analise.csv') == False:

    with open(file='./taxa-cdi-analise.csv', mode='w', encoding='utf8') as fp:
      fp.write('data,hora,taxa\n')

  # Salvando dados no arquivo "taxa-cdi.csv"

  with open(file='./taxa-cdi-analise.csv', mode='a', encoding='utf8') as fp:
    fp.write(f'{data},{hora},{cdi}\n')

  time.sleep(1)

print("Sucesso")

df = pd.read_csv('./taxa-cdi-analise.csv')

# Salvando no grafico

grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
_ = grafico.set_xticklabels(labels=df['hora'], rotation=90)
grafico.get_figure().savefig(f"{argv[1]}.png")

print(f'Gráfico salvo como {argv[1]}.png com sucesso!')
