# PROVA – Introdução à Programação (BIA) 
#**Nome completo:** João Guilherme Pires de Andrade  
#**Matrícula:** 202504010 
#**E-mail institucional:** andrade_pires@discente.ufg.br

# Questão 1

# Criei uma função para fazer o tratamento de erro, para não fazer a mesma coisa duas vezes
def tratamento_erro(mensagem, min=None, max=None): # Aqui vão a mensagem e os valores máximo e mínimo
  while True:
    try:
      valor = float(input(mensagem))
      if (min is not None and valor < min) or (max is not None and valor > max): # Se o input não tiver dentro do intervalo
        print('\n\tDigite apenas números realistas para uso residencial diário.')
        print('\tO intervalo normal é de 0.1 a 15 KW.\n')
        continue # Volta para o input
      return valor # Se estiver tudo ok, retorna o valor
    except ValueError:
      print('\n\tDigite apenas valores númericos.\n')

# Função para calcular o consumo
def calcular_consumo_mensal(pot, horas):
  return pot * horas * 30

# Pego a função para tratar erros e coloco a mensagem e o intervalo para cada variável
potencia = tratamento_erro("- Digite aqui a potência elétrica do aparelho, em KW: ", min=0.01, max=15)
tempo = tratamento_erro("- Digite aqui o tempo médio de uso diário do aparelho, em horas: ", min=0.01, max=24)
# Pego a função de consumo e calculo, usando as variáveis
consumo = calcular_consumo_mensal(potencia, tempo)
print(f'- O consumo elétrico do aparelho é de {consumo} KWh.')