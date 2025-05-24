# PROVA – Introdução à Programação (BIA) 
#**Nome completo:** João Guilherme Pires de Andrade  
#**Matrícula:** 202504010 
#**E-mail institucional:** andrade_pires@discente.ufg.br

# Questão 4

import numpy as np  # Uso numpy para fazer os arrays
import pandas as pd  # Usada aqui só pra deixar o tabuleiro bonito
import os  # Para limpar a tela do terminal entre cada atualização
import random  # Para sortear uma peça aleatória

ALTURA = 20  # Altura do tabuleiro (20 linhas)
LARGURA = 10  # Largura do tabuleiro (10 colunas)

# Lista com os formatos das peças. Cada uma é uma matriz com o "1" representando blocos. O "0" é vazio
pecas = [
    np.array([[1, 1, 1, 1]]),               # Peça reta
    np.array([[1, 1], [1, 1]]),             # Quadrado
    np.array([[0, 1, 0], [1, 1, 1]]),       # T invertido
]

# Cria o tabuleiro vazio (só zeros , ou seja, só espaços vazios)
tabuleiro = np.zeros((ALTURA, LARGURA), dtype=int)

# Verifica se a peça pode se mover pra uma posição nova
def pode_mover(peca, lin, col):
    for i in range(peca.shape[0]): # Vê o número de linhas da peça
        for j in range(peca.shape[1]): # Vê o número de colunas da peça
            if peca[i, j] == 1: # Se houver um bloco visível (1)
                x = lin + i # Soma a posição atual da peça com seu deslocamento interno
                y = col + j
                if x >= ALTURA or y < 0 or y >= LARGURA:
                    return False  # Passou dos limites do tabuleiro
                if tabuleiro[x, y] == 1:
                    return False  # Tem outra peça ali (não pode se mover)
    return True  # Pode mover sim

# Função pra mostrar o tabuleiro na tela, com a peça atual (se houver)
def mostrar_tabuleiro(tab, peca=None, lin=0, col=0):
    tab_temp = tab.copy()  # Faz uma cópia do tabuleiro para não mexer no original
    
    # Se tiver uma peça atual, coloca ela "por cima" do tabuleiro (usando 2)
    if peca is not None:
        for i in range(peca.shape[0]): # Percorre os blocos da peça
            for j in range(peca.shape[1]):
                if peca[i, j] == 1:
                    x = lin + i
                    y = col + j
                    if 0 <= x < ALTURA and 0 <= y < LARGURA:
                        tab_temp[x, y] = 2 # Se o bloco está certo, marca ele como visível

    # Limpa o terminal 
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Transforma o tabuleiro num DataFrame pra ficar mais fácil formatar
    df = pd.DataFrame(tab_temp)
    # Troca os números por símbolos visuais (0 = espaço, 1 = [], 2 = <> (peça não colocada))
    visual = df.replace(0, '  ').replace(1, '[]').replace(2, '<>')
    # Coloca as bordas laterais
    visual.insert(0, '', '<')
    visual[' '] = '>'
    
    # Mostra o tabuleiro no terminal
    print(visual.to_string(index=False, header=False)) # Sai de pandas para string
    # Tutorial de como jogar
    print("\nControles: a = esquerda | d = direita | s = descer | w = rotacionar | q = sair\n")

# Giro a peça no sentido horário, se possível
def rotacionar_peca(peca, lin, col):
    nova_peca = np.rot90(peca, -1)  # Gira 90 graus no sentido horário
    if pode_mover(nova_peca, lin, col):
        return nova_peca  # Retorna a peça girada
    return peca  # Se não der pra girar, mantém como tava

# Coloca a peça no tabuleiro "de verdade"
def fixar_peca(peca, lin, col):
    for i in range(peca.shape[0]): # De novo vai percorrer a peça
        for j in range(peca.shape[1]):
            if peca[i, j] == 1:
                tabuleiro[lin + i, col + j] = 1  # Marca com 1 onde a peça caiu

# Remove as linhas cheias e adiciona novas vazias no topo
def limpar_linhas():
    global tabuleiro # Altera a variável que está fora da função (por isso usar global)
    novas_linhas = []
    for linha in tabuleiro:
        if np.all(linha == 1): # Se a linha estiver toda cheia, vai apagar (colocar 0)
            novas_linhas.insert(0, np.zeros(LARGURA, dtype=int)) 
        else:
            novas_linhas.append(linha)  # As linhas antigas são atualizadas com a nova
    tabuleiro = np.array(novas_linhas)  # Atualiza o tabuleiro

# Sorteio a primeira peça e define posição inicial
peca = random.choice(pecas)
lin = 0
col = (LARGURA - peca.shape[1]) // 2  # Centralizo a peça no topo, no meio

# Loop principal do jogo
while True:
    mostrar_tabuleiro(tabuleiro, peca, lin, col)  # Mostra o estado atual
    comando = input("Digite comando: ").lower()  # Pede comando do jogador

    extra_descida = 0  # Pra detectar se o jogador apertou 's' (aí vai abaixar duas vezes)

    if comando == 'q':
        print("\nJogo encerrado.")
        break  # Sai do loop e encerra o jogo
    elif comando == 'a':
        if pode_mover(peca, lin, col - 1):
            col -= 1  # Move pra esquerda
    elif comando == 'd':
        if pode_mover(peca, lin, col + 1):
            col += 1  # Move pra direita
    elif comando == 's':
        extra_descida = 1  # Desce mais uma linha além da automática
    elif comando == 'w':
        peca = rotacionar_peca(peca, lin, col)  # Gira a peça
    else:
        continue  # Se o comando for inválido, ignora e pede de novo

    # Desce a peça 1 linha (mais 1 extra se o jogador pediu)
    for _ in range(1 + extra_descida): # O "_" é porque quero que se repita "range" vezes
        if pode_mover(peca, lin + 1, col):
            lin += 1  # Desce a peça
        else:
            fixar_peca(peca, lin, col)  # Gruda a peça no tabuleiro
            limpar_linhas()  # Limpa as linhas completas
            # Sorteia uma nova peça
            peca = random.choice(pecas)
            lin = 0
            col = (LARGURA - peca.shape[1]) // 2
            if not pode_mover(peca, lin, col):
                mostrar_tabuleiro(tabuleiro)
                print("\nFIM DE JOGO!\n")
                exit()  # Sai do jogo se a nova peça não couber
            break  # Para o loop de descida
