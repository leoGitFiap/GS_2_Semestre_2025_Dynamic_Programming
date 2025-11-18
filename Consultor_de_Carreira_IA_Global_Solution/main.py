# --- Importações de Bibliotecas ---

# 're' é a biblioteca de Expressões Regulares (Regex).
# Usaremos para "ler" e "extrair" dados do texto que a IA nos enviar.
import re

# 'sys' é a biblioteca de Sistema.
# Usaremos para (1) Sair do programa se a API não carregar e (2) Aumentar o limite de recursão.
import sys

# 'time' é a biblioteca de Tempo.
# Usaremos para criar pausas dramáticas com 'time.sleep()', melhorando a experiência do usuário.
import time

# 'os' é a biblioteca de Sistema Operacional.
# Usaremos para ler Variáveis de Ambiente e gerenciar input seguro,
# eliminando a necessidade de escrever a senha no código.
import os

# --- Importações Específicas do Google ---

try:
    # Tenta importar a biblioteca principal 'genai' do 'google-generativeai'.
    from google import genai
except ImportError:
    # Se a biblioteca não estiver instalada, informa o usuário e encerra o script.
    print("Erro: Biblioteca 'google-generativeai' não encontrada.")
    print("Instale com: pip install google-generativeai")
    sys.exit()  # Encerra o programa

# --- Configurações Globais ---

# O Mergesort (que usaremos) é um algoritmo recursivo.
# Se a lista for muito grande (ex: 2000 itens), ela pode atingir o limite padrão de recursão do Python (que é 1000).
# Estamos aumentando preventivamente esse limite para 2000 para evitar um 'RecursionError'.
sys.setrecursionlimit(2000)


# --- Funções Utilitárias (Interface) ---

def exibir_titulo(texto):
    """
    Função simples de formatação para imprimir um título destacado.
    """
    # Imprime uma linha de 40 sinais de '='
    print(f"\n{'=' * 40}")
    # Imprime o texto centralizado (com espaços) e em maiúsculas
    print(f"   {texto.upper()}")
    # Imprime outra linha de 40 sinais de '='
    print(f"{'=' * 40}\n")


def configurar_chave_api():
    """
    Gerencia a obtenção da chave de API de forma segura e interativa.
    Evita que o usuário precise editar o código fonte.
    """
    exibir_titulo("Configuração de Acesso")

    # 1. Tenta buscar nas Variáveis de Ambiente do sistema (Melhor prática de segurança).
    # Isso permite que desenvolvedores configurem o ambiente sem digitar a senha toda vez.
    chave_env = os.getenv("GOOGLE_API_KEY")
    if chave_env:
        print("✅ Chave de API encontrada nas variáveis de ambiente.")
        return chave_env

    # 2. Se não encontrar no sistema, solicita via terminal (Input Interativo).
    print("⚠️  Nenhuma chave de ambiente encontrada.")
    print("Este sistema utiliza a IA do Google Gemini.")
    print("Você precisa de uma chave válida (obtida em aistudio.google.com).\n")

    # Loop infinito até o usuário fornecer uma chave.
    while True:
        try:
            # .strip() remove espaços acidentais no início ou fim (ex: erro de colar).
            chave_input = input("➤ Cole sua API Key aqui e tecle ENTER: ").strip()

            if chave_input:
                # Validação visual simples (chaves do Google geralmente não são curtas).
                print("\n✅ Chave recebida. Testando conexão...")
                time.sleep(1) # Pequena pausa para feedback visual.
                return chave_input
            else:
                print("❌ A chave não pode estar vazia. Tente novamente.")
        except KeyboardInterrupt:
            # Permite sair graciosamente com Ctrl+C.
            print("\nOperação cancelada pelo usuário.")
            sys.exit()


def obter_escolha_usuario(opcoes, nome_nivel):
    """
    Função auxiliar para listar opções e capturar a escolha de forma robusta.
    'opcoes' é uma LISTA de strings (ex: ["Opção 1", "Opção 2"]).
    'nome_nivel' é um TEXTO (ex: "Grande Área").
    """
    print(f"Selecione uma opção de {nome_nivel}:")

    # 'enumerate' nos dá o índice (i) e o valor (opcao) ao mesmo tempo.
    # Começa em 0, por isso somamos +1 para exibir ao usuário (1, 2, 3...).
    for i, opcao in enumerate(opcoes):
        # Exibe a opção formatada, ex: "[1] ➤ Engenharia"
        print(f"   [{i + 1}] ➤ {opcao}")

    print("-" * 40)

    # Loop infinito 'while True' para garantir que o usuário digite uma entrada válida.
    # O loop só é quebrado por um 'return'.
    while True:
        try:
            # Captura a entrada do teclado do usuário.
            entrada = input(f"Digite o número da sua escolha (1-{len(opcoes)}): ")
            # Tenta converter a entrada (que é texto) para um número inteiro.
            escolha = int(entrada)

            # Verifica se o número está dentro do intervalo de opções válidas.
            if 1 <= escolha <= len(opcoes):
                # Se for válido, retorna o NOME da opção escolhida.
                # (Lembre-se: 'escolha' é 1-indexado, 'opcoes' é 0-indexado, por isso 'escolha - 1')
                return opcoes[escolha - 1]
            else:
                # Se o número estiver fora do intervalo (ex: 99).
                print(f"❌ Opa! O número {escolha} não está na lista. Tente entre 1 e {len(opcoes)}.")
        except ValueError:
            # Se a conversão 'int(entrada)' falhar (ex: usuário digitou "abc").
            print("❌ Por favor, digite apenas números.")


# --- Função Principal da Interface (Menu) ---

def menu_selecao_amigavel():
    """
    Função principal que guia o usuário por 3 menus aninhados.
    Não recebe parâmetros, mas RETORNA uma string (o prompt final).
    """
    # --- DADOS DO SISTEMA ---
    # Esta é a nossa "Base de Dados" estática para o menu.
    # É um DICIONÁRIO de DICIONÁRIOS de LISTAS (estrutura aninhada).
    dados_profissoes = {
        "Exatas": {
            "Engenharia": ["Civil", "Mecânica", "Elétrica", "Software", "Produção"],
            "Tecnologia": ["Dev. Web", "Data Science", "Cibersegurança", "Redes", "IA"],
            "Física": ["Teórica", "Astrofísica", "Médica", "Nuclear", "Óptica"],
            "Matemática": ["Pura", "Estatística", "Aplicada", "Atuária", "Criptografia"],
            "Química": ["Orgânica", "Industrial", "Farmacêutica", "Eng. Química", "Forense"]
        },
        "Humanas": {
            "Direito": ["Civil", "Penal", "Trabalhista", "Tributário", "Internacional"],
            "Psicologia": ["Clínica", "Organizacional", "Escolar", "Hospitalar", "Esportiva"],
            "História": ["Arqueologia", "História da Arte", "Patrimônio", "Docência", "Pesquisa"],
            "Sociologia": ["Política2", "Antropologia", "Urbana", "Mercado", "RH"],
            "Letras": ["Tradução", "Revisão", "Literatura", "Pedagogia0", "Idiomas"]
        },
        "Artes": {
            "Música": ["Composição", "Performance", "Canto", "Produção", "Regência"],
            "Artes Visuais": ["Pintura", "Escultura", "Fotografia", "Gravura", "Ilustração"],
            "Teatro": ["Atuação", "Direção", "Dramaturgia", "Cenografia", "Figurino"],
            "Cinema": ["Direção", "Roteiro", "Edição", "Fotografia", "Som"],
            "Design": ["Gráfico", "Produto", "Interiores", "UX/UI", "Moda"]
        },
        "Biológicas": {
            "Medicina": ["Cardiologia", "Pediatria", "Neurologia", "Ortopedia", "Psiquiatria"],
            "Biologia": ["Marinha", "Botânica", "Genética", "Microbiologia", "Zoologia"],
            "Enfermagem": ["UTI", "Obstetrícia", "Saúde Pública", "Pediatria", "Gestão Hospitalar"],
            "Fisioterapia": ["Esportiva", "Respiratória", "Neurofuncional", "Ortopédica", "Quiropraxia"],
            "Meio Ambiente": ["Gestão Ambiental", "Ecologia", "Agronomia", "Veterinária", "Eng. Florestal"]
        },
        "Negócios": {
            "Administração": ["Estratégia", "Operações", "Logística", "Empreendedorismo", "Consultoria"],
            "Marketing": ["Digital", "Branding", "Conteúdo", "Performance", "Endomarketing"],
            "Finanças": ["Investimentos", "Contabilidade", "Auditoria", "Bancária", "Controladoria"],
            "Economia": ["Macroeconomia", "Microeconomia", "Econometria", "Internacional", "Setor Público"],
            "Comércio Exterior": ["Importação", "Exportação", "Logística Int.", "Aduaneira", "Negociação"]
        }
    }

    # Dicionário auxiliar para exibir descrições amigáveis no Passo 1.
    descricoes_areas = {
        "Exatas": "Foco em lógica, cálculos, números e sistemas.",
        "Humanas": "Foco em sociedade, cultura, comportamento e leis.",
        "Artes": "Foco em criatividade, estética, expressão e design.",
        "Biológicas": "Foco em vida, saúde, natureza e meio ambiente.",
        "Negócios": "Foco em gestão, mercado, finanças e estratégia."
    }

    # Lista vazia que VAMOS CONSTRUIR com as escolhas do usuário.
    # Ex: ["Exatas", "Tecnologia", "IA"]
    lista_prompt = []

    # --- INÍCIO DO PROGRAMA ---
    exibir_titulo("Consultor de Carreira IA")
    print("Olá! Vou ajudar você a definir seu perfil profissional em 3 passos.")
    time.sleep(1.5)  # Pausa de 1.5s para leitura.

    # --- PASSO 1: Grande Área ---
    print("\n📊 PASSO 1: A GRANDE ÁREA")
    print("Primeiro, onde você se encaixa melhor?\n")

    # Itera sobre o dicionário de descrições para mostrá-las.
    for area, descricao in descricoes_areas.items():
        print(f"🔹 {area}: {descricao}")
    print("")

    # Pega as chaves (keys) do dicionário principal.
    # Resultado: ["Exatas", "Humanas", "Artes", "Biológicas", "Negócios"]
    opcoes_nivel_1 = list(dados_profissoes.keys())
    # Chama nossa função auxiliar para obter a escolha.
    escolha_1 = obter_escolha_usuario(opcoes_nivel_1, "Grande Área")

    # Adiciona a primeira escolha à nossa lista.
    lista_prompt.append(escolha_1)
    print(f"\n✅ Entendido! Vamos focar em **{escolha_1}**.")
    time.sleep(1)  # Pausa de 1s

    # --- PASSO 2: Subcategoria ---
    print(f"\n📂 PASSO 2: ESPECIALIDADE EM {escolha_1.upper()}")
    print("Qual destes campos mais te atrai?\n")

    # "Navega" para dentro do dicionário usando a escolha anterior como chave.
    # Ex: subcategorias = dados_profissoes["Exatas"]
    subcategorias = dados_profissoes[escolha_1]
    # Pega as chaves desse sub-dicionário.
    # Ex: ["Engenharia", "Tecnologia", "Física", "Matemática", "Química"]
    opcoes_nivel_2 = list(subcategorias.keys())
    # Obtém a segunda escolha do usuário.
    escolha_2 = obter_escolha_usuario(opcoes_nivel_2, "Campo de Atuação")

    # Adiciona a segunda escolha à nossa lista.
    lista_prompt.append(escolha_2)
    print(f"\n✅ Ótima escolha: **{escolha_2}**.")
    time.sleep(1)  # Pausa de 1s

    # --- PASSO 3: Nicho Específico ---
    print(f"\n🎯 PASSO 3: NICHO EM {escolha_2.upper()}")
    print("Para finalizar, qual é o seu foco específico?\n")

    # Navega mais um nível para dentro do dicionário.
    # Ex: areas_finais = dados_profissoes["Exatas"]["Tecnologia"]
    # O resultado agora é a LISTA final.
    # Ex: ["Dev. Web", "Data Science", "Cibersegurança", "Redes", "IA"]
    areas_finais = subcategorias[escolha_2]
    # Obtém a terceira e última escolha.
    escolha_3 = obter_escolha_usuario(areas_finais, "Nicho Específico")

    # Adiciona a terceira escolha à nossa lista.
    lista_prompt.append(escolha_3)

    # --- FINALIZAÇÃO ---
    time.sleep(0.5)
    exibir_titulo("Resultado Gerado")

    # Constrói a string final (prompt de contexto) usando as 3 escolhas da 'lista_prompt'.
    prompt_final = (
        f"Atuo na área de {lista_prompt[0]}, "
        f"especificamente no campo de {lista_prompt[1]}, "
        f"com foco profissional em {lista_prompt[2]}."
    )

    # Mostra ao usuário o perfil que ele montou.
    print("Aqui está o resumo do seu perfil:\n")
    print(f"📝 \"{prompt_final}\"")
    print("\nObrigado por usar o sistema!")

    # Retorna a string de contexto, que será usada no 'if __name__ == "__main__"'.
    return prompt_final


# --- Funções de Processamento de Dados (API e Mergesort) ---

def prompt_para_ia(prompt_texto):
    """
    Envia um prompt para a API Gemini e retorna a resposta em texto.
    """
    print(f"\n-> Enviando prompt para a API...")
    try:
        # Chama o cliente da API (a variável 'client' deve estar globalmente disponível
        # após a inicialização no main).
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Modelo específico que estamos usando
            contents=prompt_texto  # O prompt que construímos
        ).text  # Pega APENAS o texto da resposta
        print("-> Resposta recebida.")
        return response
    except Exception as e:
        # Se a chamada da API falhar (ex: sem internet, cota excedida)
        print(f"ERRO ao chamar a API: {e}")
        return None  # Retorna 'None' (nada) para sinalizar o erro


def coletar_dados_da_api(response_text):
    """
    Recebe o TEXTO de resposta da API (em tópicos)
    e o converte para a estrutura de dados (lista de dicionários).
    Esta é a etapa de "Extração e Transformação" (ETL).
    """
    print("-> Formatando dados da API (Tópicos)...")
    # Se a função anterior (prompt_para_ia) retornou None, não faz nada.
    if not response_text:
        print("ERRO: Resposta da API está vazia.")
        return []

    # Nosso "dataframe" será uma lista de dicionários.
    dataframe_lista = []

    # Divide a resposta inteira (um único bloco de texto) em linhas individuais.
    linhas = response_text.strip().split('\n')

    # Processa cada linha individualmente.
    for linha in linhas:
        # Remove espaços em branco do início e do fim da linha.
        linha_limpa = linha.strip()

        # --- A MÁGICA DO REGEX ---
        # Estamos procurando um padrão específico que pedimos à IA.
        # O regex deve capturar 3 GRUPOS: Área, Curso e Salário.
        #
        # Explicação:
        # ^\* -> Começa com asterisco
        # (.*?)    -> Grupo 1: Captura a Área (até o próximo :)
        # \s*:\s* -> Separador ':'
        # (.*?)    -> Grupo 2: Captura o Curso (até o próximo :)
        # \s*:\s* -> Separador ':'
        # ([\d,.]+) -> Grupo 3: Captura o Salário (números e pontuações)
        match = re.match(r'^\*\s*(.*?)\s*:\s*(.*?)\s*:\s*([\d,.]+)', linha_limpa)

        # Se o padrão da linha CORRESPONDER ao nosso Regex...
        if match:
            try:
                # Extrai os grupos capturados.
                area = match.group(1).strip()  # Grupo 1 (Área)
                curso = match.group(2).strip()  # Grupo 2 (Curso)
                salario_str = match.group(3).strip()  # Grupo 3 (Salário como texto)

                # --- Lógica de Limpeza do Salário ---
                # A IA pode retornar "15.000" ou "15.000,50"
                # 1. Pega só a parte ANTES da vírgula (ex: "15.000,50" vira "15.000")
                parte_inteira_str = salario_str.split(',')[0]
                # 2. Remove os pontos (separadores de milhar) (ex: "15.000" vira "15000")
                salario_limpo_str = parte_inteira_str.replace(".", "")

                # 3. Converte a string limpa para um número inteiro.
                salario_int = int(salario_limpo_str)
                # --- Fim da limpeza ---

                # Cria um dicionário para esta linha
                item_dicionario = {
                    'area': area,
                    'curso': curso,
                    'salario_estimado_mensal': salario_int  # Salva o NÚMERO
                }
                # Adiciona o dicionário à nossa lista (dataframe).
                dataframe_lista.append(item_dicionario)

            except ValueError:
                # Se 'int(salario_limpo_str)' falhar (ex: a IA mandou "abc")
                print(f"-> Linha ignorada (salário não é número): {linha}")
            except Exception as e:
                # Outro erro inesperado no processamento desta linha.
                print(f"-> Erro ao processar linha {linha}: {e}")
        else:
            # Se a linha NÃO CORRESPONDER ao padrão Regex (ex: linha em branco, título)
            if linha_limpa:  # Só reporta se não for uma linha totalmente em branco
                print(f"-> Linha ignorada (formato de tópico não reconhecido): {linha}")

    # Se, após tudo isso, a lista estiver vazia, algo deu muito errado.
    if not dataframe_lista:
        print("\nERRO: Nenhum tópico válido foi encontrado na resposta da API.")
        print("Resposta recebida:", response_text)

    # Sucesso!
    print(f"-> {len(dataframe_lista)} tópicos convertidos para o dataframe.")
    return dataframe_lista  # Retorna a lista de dicionários


def mostrar_dados(dados_lista, titulo="Dados da API"):
    """
    (Função Atualizada)
    Função utilitária para imprimir a lista de dicionários.
    Ela calcula dinamicamente a largura de cada coluna para não quebrar a tabela.
    """
    print(f"\n--- {titulo} ---")
    # Validação: se a lista estiver vazia, não faz nada.
    if not dados_lista:
        print("Nenhum dado para mostrar.")
        return

    # --- INÍCIO DA LÓGICA DE FORMATAÇÃO ---

    # 1. Definir os nomes dos cabeçalhos
    header_area = "Área de Atuação"
    header_curso = "Curso Exemplo"
    header_salario = "Salário Mensal (R$)"

    # 2. Calcular a largura máxima dos DADOS em cada coluna
    # O 'max()' varre toda a lista para encontrar o texto mais longo.
    try:
        max_w_area = max(len(item.get('area', '')) for item in dados_lista)
        max_w_curso = max(len(item.get('curso', '')) for item in dados_lista)
        # Para o salário, calcula o tamanho do NÚMERO FORMATADO (ex: 15.000 tem 6 chars)
        max_w_salario_num = max(len(f"{item.get('salario_estimado_mensal', 0):,}") for item in dados_lista)

    except Exception as e:
        print(f"ERRO ao calcular larguras: {e}. Verifique os dados: {dados_lista}")
        return

    # 3. A largura final da coluna é o MÁXIMO entre o cabeçalho e o dado mais longo.
    # Isso garante que o cabeçalho não fique cortado, nem os dados.
    w_area = max(len(header_area), max_w_area)
    w_curso = max(len(header_curso), max_w_curso)
    w_salario = max(len(header_salario), max_w_salario_num)

    # 4. Definir o separador
    sep = " | "

    # --- FIM DA LÓGICA DE FORMATAÇÃO ---

    # 5. Imprimir o Cabeçalho
    # f-string: {valor:<{largura}} alinha à esquerda.
    # f-string: {valor:>{largura}} alinha à direita.
    print(
        f"{header_area:<{w_area}}" + sep +
        f"{header_curso:<{w_curso}}" + sep +
        f"{header_salario:>{w_salario}}"  # Salário alinhado à direita
    )

    # 6. Imprimir a linha separadora
    # O tamanho total é a soma das larguras + separadores
    total_width = w_area + w_curso + w_salario + len(sep) * 2
    print("-" * total_width)

    # 7. Imprimir os Dados (item por item)
    for item in dados_lista:
        try:
            area = item.get('area', 'N/A')
            curso = item.get('curso', 'N/A')
            # Formata o número com vírgulas/pontos
            salario_f = f"{item.get('salario_estimado_mensal', 0):,}"

            # Imprime a linha de dados, respeitando as larguras calculadas
            print(
                f"{area:<{w_area}}" + sep +
                f"{curso:<{w_curso}}" + sep +
                f"{salario_f:>{w_salario}}"  # Salário alinhado à direita
            )
        except KeyError as e:
            print(f"ERRO: Item {item} não contém a chave {e}")
        except ValueError:
            print(f"ERRO: Salário {item.get('salario_estimado_mensal')} não é um número.")


def organizar_dados(lista_de_dados, chave_para_ordenar):
    """
    Função principal que organiza a LISTA DE DICIONÁRIOS (Mergesort).
    Recebe a lista e a 'chave' (ex: 'salario_estimado_mensal') pela qual ordenar.
    Esta função usa duas "funções aninhadas" (funções dentro de funções).
    """

    print(f"\nIniciando organização (Maior -> Menor) por '{chave_para_ordenar}'...")

    # --- Início das Funções Aninhadas ---

    def merge(esquerda, direita):
        """
        Função ANINHADA (1) - "Conquistar".
        Recebe duas listas JÁ ORDENADAS (esquerda e direita)
        e as mescla em uma única lista ordenada.
        """
        # Lista final
        resultado_mesclado = []
        # Índices para percorrer as listas 'esquerda' e 'direita'
        idx_esq, idx_dir = 0, 0

        # Loop enquanto AINDA houver itens em AMBAS as listas
        while idx_esq < len(esquerda) and idx_dir < len(direita):
            try:
                # --- O PONTO DA COMPARAÇÃO ---
                # Pega o item (dicionário) na 'esquerda' e compara seu salário...
                # ...com o item (dicionário) na 'direita'.
                # Usamos '>=' para ordenar do MAIOR para o MENOR (ordem descendente).
                if esquerda[idx_esq][chave_para_ordenar] >= direita[idx_dir][chave_para_ordenar]:
                    # Se o da esquerda for maior, adiciona ele ao resultado.
                    resultado_mesclado.append(esquerda[idx_esq])
                    idx_esq += 1  # Avança o índice da esquerda
                else:
                    # Se o da direita for maior, adiciona ele.
                    resultado_mesclado.append(direita[idx_dir])
                    idx_dir += 1  # Avança o índice da direita
            except KeyError:
                # Tratamento de erro caso um dicionário não tenha a chave (ex: erro na API)
                print(f"ERRO no Mergesort: Chave '{chave_para_ordenar}' não encontrada.")
                # Pula os itens problemáticos
                if idx_esq < len(esquerda) and chave_para_ordenar not in esquerda[idx_esq]:
                    idx_esq += 1
                if idx_dir < len(direita) and chave_para_ordenar not in direita[idx_dir]:
                    idx_dir += 1

        # --- Fim do loop principal ---
        # Neste ponto, uma das listas (ou ambas) acabou.
        # Mas podem ter sobrado itens na outra lista.
        # As linhas abaixo pegam "o que sobrou" e adicionam ao final.
        resultado_mesclado.extend(esquerda[idx_esq:])
        resultado_mesclado.extend(direita[idx_dir:])

        # Retorna a lista totalmente mesclada e ordenada.
        return resultado_mesclado

    def mergesort_interno(lista):
        """
        Função ANINHADA (2) - "Dividir".
        Esta é a função recursiva que quebra a lista.
        """
        # --- CASO BASE DA RECURSÃO ---
        # Se a lista tiver 1 item (ou 0), ela já está "ordenada".
        # Isso impede a recursão infinita.
        if len(lista) <= 1:
            return lista

        # --- Etapa de Divisão ---
        # Encontra o índice do meio da lista.
        meio = len(lista) // 2
        # Fatiamento (slicing): pega a primeira metade
        lado_esquerdo = lista[:meio]
        # Fatiamento: pega a segunda metade
        lado_direito = lista[meio:]

        # --- Chamadas Recursivas ---
        # Chama a si mesma para ordenar a metade esquerda
        esquerdo_ordenado = mergesort_interno(lado_esquerdo)
        # Chama a si mesma para ordenar a metade direita
        direito_ordenado = mergesort_interno(lado_direito)

        # --- Etapa de Conquista ---
        # Quando as duas metades voltam ordenadas, chama a função 'merge'
        # para juntá-las.
        return merge(esquerdo_ordenado, direito_ordenado)

    # --- Fim das Funções Aninhadas ---

    # Validação simples de tipo
    if not isinstance(lista_de_dados, list):
        print("ERRO: 'organizar_dados' esperava uma lista.")
        return []

    # Validação de lista vazia
    if not lista_de_dados:
        return []

    # --- Ponto de Partida ---
    # Chama a função recursiva interna pela primeira vez
    # para iniciar o processo de divisão.
    dados_ordenados = mergesort_interno(lista_de_dados)

    print("Organização concluída.")
    return dados_ordenados


# --- Execução Principal do Programa ---

# Esta verificação garante que o código abaixo SÓ rode
# quando o script é executado diretamente (ex: 'python seu_script.py'),
# e não quando ele é importado por outro script.
if __name__ == "__main__":

    # 1. CONFIGURAÇÃO DA API (NOVO PASSO)
    # Solicitamos a chave antes de qualquer coisa.
    minha_chave = configurar_chave_api()

    # Inicializamos o cliente da API com a chave fornecida pelo usuário.
    try:
        client = genai.Client(api_key=minha_chave)
    except Exception as e:
        print(f"Erro fatal ao inicializar o cliente: {e}")
        sys.exit()

    # 2. CONSTRUÇÃO DO PROMPT
    # Estamos usando uma f-string (f"") e 'triple quotes' (""") para
    # criar um texto de múltiplas linhas.
    prompt_detalhado = f"""
    {menu_selecao_amigavel()}.
    Apresente as 20 melhores áreas mais relevantes no futuro da tecnologia, com maiores salários mensais, no Brasil, de acordo com as minhas capacidades.
    Apresente também um exemplo de site, curso simples, por onde posso começar.

    Responda **APENAS** com tópicos (bullet points).
    Não inclua nenhum texto antes ou depois dos tópicos.

    Use o formato exato:
    * [Nome da Área]: [Curso de exemplo]: [Salário mensal como número inteiro]

    Exemplo:
    * Engenharia de Software: FIAP: 2.500
    * Engenharia de Petróleo: Curso Hipotético: 2.750
    """
    # {menu_selecao_amigavel()} chama a função do menu, e o texto que ela
    # RETORNA (ex: "Atuo em Exatas...") é inserido aqui.
    # O "Exemplo:" é crucial, pois "ensina" a IA (few-shot learning)
    # qual o formato exato que esperamos.

    # 3. CHAMA A API
    # 'prompt_detalhado' é enviado para a IA.
    # 'resposta_em_texto' é o que a IA devolve (um bloco de texto).
    resposta_em_texto = prompt_para_ia(prompt_detalhado)

    # 4. CONVERTE OS DADOS (ETL)
    # 'resposta_em_texto' é processada pelo Regex.
    # 'minha_lista_api' é a LISTA DE DICIONÁRIOS (nosso dataframe).
    minha_lista_api = coletar_dados_da_api(resposta_em_texto)

    # 5. PROCESSA E EXIBE
    # Se a lista não estiver vazia (ou seja, o parsing funcionou)...
    if minha_lista_api:
        # Mostra os dados na ordem original que a API enviou.
        mostrar_dados(minha_lista_api, "DataFrame Original (Ordem da API)")

        # Chama o Mergesort para organizar pela chave 'salario_estimado_mensal'.
        lista_ordenada_salario = organizar_dados(minha_lista_api, 'salario_estimado_mensal')

        # Mostra os dados ordenados.
        mostrar_dados(lista_ordenada_salario, "DataFrame Ordenado (Maior Salário)")
    else:
        # Se 'minha_lista_api' estiver vazia, o programa avisa e termina.
        print("\nPrograma encerrado. Não foi possível processar os dados da API.")