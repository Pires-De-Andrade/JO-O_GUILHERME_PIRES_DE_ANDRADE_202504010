# PROVA – Introdução à Programação (BIA) 
#**Nome completo:** João Guilherme Pires de Andrade  
#**Matrícula:** 202504010 
#**E-mail institucional:** andrade_pires@discente.ufg.br

# Questão número 6

# É um programa que devolve dados climáticos do Brasil. Dividi tudo em funções
# Importei tkinter para fazer a interface gráfica do meu minissistema
# Achei mais coerente com a simplicidade da questão do que fazer um arquivo html
# Ao clicar em "Relatório do Tempo", os dados são facilmente atualizados

import tkinter as tk 
from tkinter import messagebox
import requests # Para pegar a url das apis

# Dicionário de códigos climáticos (da api open meteo)
weather_codes = {
    0: "Céu limpo", 1: "Principalmente claro", 2: "Parcialmente nublado", 3: "Nublado",
    45: "Névoa", 48: "Névoa com geada", 51: "Chuvisco leve", 53: "Chuvisco moderado",
    55: "Chuvisco intenso", 61: "Chuva leve", 63: "Chuva moderada", 65: "Chuva forte",
    71: "Neve leve", 73: "Neve moderada", 75: "Neve intensa", 80: "Pancadas de chuva leves",
    81: "Pancadas de chuva moderadas", 82: "Pancadas de chuva fortes", 95: "Trovoadas",
    96: "Trovoadas com granizo leve", 99: "Trovoadas com granizo forte"
}

def obter_coordenadas(municipio, estado, pais='Brasil'):
    # Aqui uso a api OpenSreetMap para pegar as coordenadas do município escolhido
    # Isso será importante para saber o clima, mais na frente
    url = "https://nominatim.openstreetmap.org/search"
    params = {'q': f"{municipio}, {estado}, {pais}", 'format': 'json', 'limit': 1}
    # Aqui em cima ficam os parâmetros da api. Primeiro, o que ela vai buscar, depois como vai devolver (json)
    # e um "limite" que faz devolver a primeira resposta encontrada pela api
    headers = {'User-Agent': 'João Guilherme (joaog.pa14@gmail.com)'}
    # Esse headers é parte da política da api, para contato etc
    response = requests.get(url, params=params, headers=headers) 
    dados = response.json() # Pego a resposta e transformo numa lista de dicionários
    if dados: # Se dados existir...
        lat = float(dados[0]['lat']) # Pego as coordenadas destacadas
        lon = float(dados[0]['lon'])
        return lat, lon
    else: # Se não... retorna None
        return None, None

def obter_clima(lat, lon):
    # Aqui uso a api Open Meteo para pegar dados climáticos
    url = "https://api.open-meteo.com/v1/forecast"
    params = {'latitude': lat, 'longitude': lon, 'current_weather': True, 'timezone': 'America/Sao_Paulo'}
    # Usando as coordenadas, um parâmetro do tempo atual e um fuso horário, consigo os dados
    response = requests.get(url, params=params)
    dados = response.json() # Pego a resposta e transformo numa lista de dicionários
    if 'current_weather' in dados: # Se a resposta do tempo atual existir...
        clima = dados['current_weather']
        codigo = clima['weathercode']
        descricao = weather_codes.get(codigo, "Código desconhecido")
        return {
            'temperatura': clima['temperature'],
            'vento': clima['windspeed'],
            'descricao': descricao
        }
    # Pego os dados e monto esse dicionário. A descrição pega o código em "dados" e traduz com aquele 1° dicionário
    return None # Se não tiver, retorna None

def buscar_clima():
    # Essa função será chamada quando clicar em "Relatório do Tempo"
    estado = estado_entry.get().upper() # Pega o input e deixa maiúsculo (sigla)
    municipio = municipio_entry.get().title() # Pega o input, deixa minúsculo e capitaliza

    if not estado or not municipio:
        # Mensagem para caso os campos não sejam preenchidos
        messagebox.showwarning("Entrada inválida", "Preencha ambos os campos!")
        return

    # Chamo as função de coordenadas para pegar os dados da cidade
    lat, lon = obter_coordenadas(municipio, estado)
    if lat and lon: # Se a resposta não for None, coloco na função obter_clima
        clima = obter_clima(lat, lon)
        if clima: # Se não for None, mostra essa mensagem formatada
            resultado_var.set(
                f"Temperatura: {clima['temperatura']}°C\n"
                f"Vento: {clima['vento']} km/h\n"
                f"Condição: {clima['descricao']}"
            )
        else: # Se for None, aparece isso
            resultado_var.set("Erro ao obter clima.")
        # Caso o local não seja encontrado, aparece isso
    else:
        resultado_var.set("Local não encontrado.")

# Aqui faço a interface gráfica usando o ttinker
janela = tk.Tk() # Crio a janela
janela.title("Dados Climáticos no Brasil") # Faço o título
janela.configure(bg="#E8F0F2")  # Cor de fundo azul clara

# Aqui vou criar uma janela de texto com as instruções de uso do minissistema
instrucoes = tk.Text(janela, height=5, width=60, bg="#D9EAF2", fg="#333333", font=("Arial", 10), wrap="word", borderwidth=0)
instrucoes.insert(tk.END,
    "- Bem-vindo, Usuário!\n"
    "- Digite a sigla do estado (ex: PE) e o nome do município (ex: Recife) para ver as condições climáticas em tempo real.\n"
    "- Clique em 'Relatório do Tempo' para iniciar."
    "\n- Obrigado por usar nosso serviço!"
)
instrucoes.config(state="disabled")  # Deixa o texto só de leitura
instrucoes.pack(pady=10) # O pady dá um espaçamento vertical de x pixels

# Crio um label para apresentar a caixa de input do estado (formtada com cor e fonte)
tk.Label(janela, text="Estado (sigla):", bg="#E8F0F2", fg="#003366", font=("Arial", 12, "bold")).pack()
estado_entry = tk.Entry(janela, font=('Arial', 12)) # Pego essa janela e coloco aquele input do estado
estado_entry.pack(pady=5)

# Crio um label para apresentar, agora, a caixa de input do município (também formatada)
tk.Label(janela, text="Município (nome):", bg="#E8F0F2", fg="#003366", font=("Arial", 12, "bold")).pack() # Melhoro a fonte e as cores
municipio_entry = tk.Entry(janela, font=('Arial', 12))  # Pego essa janela e coloco aquele input da cidade
municipio_entry.pack(pady=5)

# Crio o botão que vai acionar a função "buscar_clima" da api
tk.Button(janela, text='Relatório do Tempo', command=buscar_clima, bg='#3399FF', fg='white', font=('Arial', 12, 'bold')).pack(pady=10) # Crio esse botão para executar a função buscar_clima

resultado_var = tk.StringVar() # Essa variável serve para ligar os dados aos elementos da interface
resultado_label = tk.Label(janela, textvariable=resultado_var, justify="left", font=("Arial", 12), bg="#E8F0F2", fg="#000000")
# Essa variável mostra onde e como vão aparecer os dados climáticos contidos em resultado_var
resultado_label.pack(pady=10)

janela.mainloop() # E... inicio o looping de eventos!