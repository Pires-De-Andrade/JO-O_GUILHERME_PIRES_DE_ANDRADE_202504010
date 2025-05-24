# PROVA – Introdução à Programação (BIA) 
#**Nome completo:** João Guilherme Pires de Andrade  
#**Matrícula:** 202504010 
#**E-mail institucional:** andrade_pires@discente.ufg.br

# Questão 2

# Aqui estarão os dados de metas
metas = {}
# Aqui estarão os gastos, as despesas
despesas = []

# Número de categorias - com tratamento de erro e intervalo de 1 a 10 (para organizar)
while True:
    try:
        num_categorias = int(input("- Quantas categorias de despesas deseja inserir? "))
        if num_categorias <= 0 or num_categorias > 10:
            print("zn\tPor favor, insira um número entre 1 e 10.\n")
            continue
        break
    except ValueError: # Se for digitada uma string...
        print("\n\tDigite apenas números.\n")

# Aqui serão inseridas as metas em si
for i in range(num_categorias): # Isso vai se repetir "num_categorias" vezes
    nome = input(f"- Nome da categoria {i+1}: ").strip().lower()
    meta = float(input(f"- Meta de gastos para a categoria '{nome}': R$ "))
    metas[nome] = meta # Cria no dicionário algo assim: {"nome": meta}

# Aqui serão especificados os gastos
num_despesas = int(input("\n- Quantos lançamentos financeiros deseja registrar? "))

for i in range(num_despesas): # Vai se repetir "num_despesas" vezes
    descricao = input("\n- Descrição da despesa: ")
    valor = float(input("- Valor gasto: R$ "))
    categoria = input("- Categoria da despesa: ").strip().lower()
    despesas.append({"descricao": descricao, "valor": valor, "categoria": categoria})
    # Ao final, os dados, em dicionário, serão adicionados na lista

# Aqui vai um resumo dos gastos pro categoria
resumo = {}

for despesa in despesas: # Para cada elemento nas despesas...
  cat = despesa["categoria"] # Pego a categoria e o valor
  val = despesa["valor"]

  if cat not in resumo: # Se a despesa não estiver em "resumo", adiciona-se
    resumo[cat] = {"total": 0, "qtd": 0, "itens": []} # Cria um dicionário de dados para cada categoria
    
  resumo[cat]["total"] += val # Vai somar o valor da despesa
  resumo[cat]["qtd"] += 1 # Vai somar a quantidade 
  resumo[cat]["itens"].append(despesa["descricao"]) # Vai pegar a descrição da despesa

# Aqui vai encontrar a categoria com maior gasto
maior_categoria = None
maior_valor = 0

for cat, dados in resumo.items(): # Vai percorrer os items de "resumo"
  if dados["total"] > maior_valor: # Se o total gasto nas despesas for maior que 0...
    maior_valor = dados["total"] # O maior valor se torna a variável maior que 0
    maior_categoria = cat # E a categoria correspondente se torna a maior
    # A lógica é que o "for" vai percorrer todos os items e vendo qual é maior do que o outro

# Aqui vai o relatório de despesas
print("\n" + "="*60)
print("RELATÓRIO DE GASTOS".center(60))
print("="*60)

for cat, dados in resumo.items(): # Aqui faço um resumo por categoria
    print(f"\nCategoria: {cat}")
    print(f" - Meta: R$ {metas.get(cat, 0):.2f}") # Valor da meta
    print(f" - Gasto total: R$ {dados['total']:.2f}") # O que foi gasto no total
    print(f" - Média por despesa: R$ {dados['total'] / dados['qtd']:.2f}") # Média
    print(f" - Número de despesas: {dados['qtd']}") # Número de despesas
    print(f" - Descrições: {', '.join(dados['itens'])}") # Quais as despesas

print("\n" + "-"*60)
print(f"- A categoria com maior gasto foi '{maior_categoria}' com R$ {maior_valor:.2f}")
print("-"*60)

total_categorias = len(metas) # Quantidade de metas
meta_total = sum(metas.values()) # Soma dos valores estipulados para a meta
gasto_total = sum(dados["total"] for dados in resumo.values()) # Soma do total gasto com despesas
quantidade = sum(dados["qtd"] for dados in resumo.values()) # Soma da quantidade de despesas

print("\n" + "="*60)
print("RESUMO FINAL".center(60)) # Aqui vai um resumo de toda as informações, gerais
print("="*60)
print(f"- Total de categorias registradas: {total_categorias}")
print(f"- Soma de todas as metas: R$ {meta_total:.2f}")
print(f"- Soma total dos gastos: R$ {gasto_total:.2f}")
print(f"- Total de despesas registradas: {quantidade}")
print("="*60)

# No final, temos tudo que a questão pediu: comparação de metas, total de despesas, total gasto por categoria, média por categoria e categoria com maior valor gasto