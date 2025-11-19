# --- Importações de Bibliotecas ---
import re  # Importa a biblioteca 're' para usar Expressões Regulares (Regex).
import sys  # Importa a biblioteca 'sys' para interações com o interpretador e sistema.
import time  # Importa a biblioteca 'time' para funções relacionadas ao tempo (como pausas).
import os  # Importa a biblioteca 'os' para interagir com o sistema operacional (variáveis de ambiente).
from google import genai  # Importa a classe principal 'genai' para comunicação com o Gemini API.
from google.genai.errors import APIError # Importa a classe de exceção específica de erro da API para tratamento de chave inválida

# --- Configurações Globais ---
# Aumenta o limite padrão de recursão para 2000. Necessário para garantir que o Mergesort não falhe
sys.setrecursionlimit(2000)  # em listas grandes, excedendo o limite padrão de 1000.
client = None  # Inicializa a variável 'client' da API como None; será preenchida posteriormente.

# --- Dicionário de Dados (Base de Referência) ---
# Esta estrutura de dados aninhada define os menus de seleção (Área > Campo > Nicho).
dados_profissoes = {
    "Exatas": {  # Nível 1: Grande Área
        # Nível 2: "Campo de Atuação": ["Nível 3: Nichos"]
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


# --- Funções Utilitárias (Interface) ---

def exibir_titulo(texto):
    """ Define e exibe uma função para formatar títulos. """
    print(f"\n{'=' * 40}")  # Imprime uma linha superior de separação.
    print(f"   {texto.upper()}")  # Imprime o texto em maiúsculas, levemente indentado.
    print(f"{'=' * 40}\n")  # Imprime uma linha inferior de separação.


def configurar_chave_api():
    """ Define uma função para gerir a obtenção da chave de API. """
    exibir_titulo("Configuração de Acesso")  # Exibe o título da seção.

    chave_env = os.getenv("GOOGLE_API_KEY")  # Tenta ler a chave da variável de ambiente.
    if chave_env:  # Verifica se a chave foi encontrada.
        print("✅ Chave de API encontrada nas variáveis de ambiente.")  # Informa sucesso.
        return chave_env  # Retorna a chave.

    # Caso a chave não seja encontrada no ambiente:
    print("⚠️  Nenhuma chave de ambiente encontrada.")  # Alerta o usuário.
    print("Você precisa de uma chave Gemini válida (aistudio.google.com).\n")  # Instruções.

    while True:
        chave_input = input("\nDigite o Chave de API (ou digite 'sair'): ").strip()

        if chave_input.lower() == "sair":
            print("\n❌ Operação cancelada pelo usuário. Encerrando o programa.")
            sys.exit()

        if chave_input:
            print("\n✅ Chave recebida. Testando conexão...")
            time.sleep(0.5)

            if validar_chave_input(chave_input):
                return chave_input
            else:
                print("\n❌ Chave inválida ou erro de conexão. Tente novamente.")
        else:
            print("\n❌ A chave não pode estar vazia. Tente novamente.")


def validar_chave_input(chave):
    """
    Tenta inicializar o cliente da API e fazer uma chamada simples para validar a chave.
    Reintroduz o try/except APENAS para tratamento de erro de conexão/autenticação.
    """
    try:
        # Tenta inicializar o cliente com a chave fornecida
        temp_client = genai.Client(api_key=chave)

        # Faz uma chamada trivial (ex: listar modelos) para forçar a autenticação
        # Se a chave for inválida, esta linha levantará uma APIError
        temp_client.models.list()

        # Se chegou aqui, a chave é válida e a conexão foi estabelecida
        print("✅ Conexão estabelecida com sucesso.")
        return True

    except APIError as e:
        # Captura erros específicos da API (inclui chaves inválidas, permissões negadas, etc.)
        if "API_KEY_INVALID" in str(e):
            print(f"❌ Erro de Autenticação: A chave fornecida é inválida.")
        else:
            print(f"❌ Erro de Conexão ou Servidor: {e}")
        return False

    except Exception as e:
        # Captura outros erros inesperados (ex: falha de rede/DNS)
        print(f"❌ Erro Inesperado durante a validação: {e}")
        return False


def obter_escolha_usuario(opcoes, nome_nivel, permitir_voltar=False):
    """
    Define uma função para exibir opções de menu, incluindo a opção 'Voltar' se permitido.
    """
    print(f"Selecione uma opção de {nome_nivel}:")  # Exibe o título do menu (nível).

    i = 1  # Inicializa o contador de índice para exibição (começa em 1).
    for opcao in opcoes:  # Loop que itera sobre a lista de opções de dados.
        print(f"   [{i}] ➤ {opcao}")  # Imprime a opção com o índice atual.
        i = i + 1  # Incrementa o contador para a próxima linha.

    # Lógica para adicionar a opção 'Voltar'
    if permitir_voltar:  # Verifica se a opção de retorno está ativa.
        print(f"   [{i}] ⬅️ Voltar")  # Imprime a opção 'Voltar' com o próximo índice.
        limite_superior = i  # Define o limite superior como o índice de 'Voltar'.
    else:
        limite_superior = len(opcoes)  # Se não puder voltar, o limite é o tamanho da lista.

    print("-" * 40)  # Imprime uma linha separadora.

    # Loop de validação de entrada
    while True:
        prompt_range = f"(1-{limite_superior})"  # Define o intervalo de números válidos para o prompt.
        entrada = input(f"Digite o número da sua escolha {prompt_range}: ")  # Solicita a entrada.

        escolha = int(entrada)  # Converte a entrada para inteiro (ponto frágil, sem try/except).

        # 1. TRATAMENTO DE VOLTAR: Verifica se a escolha corresponde ao índice de 'Voltar'
        if permitir_voltar and escolha == limite_superior:
            return "VOLTAR"  # Retorna a string de comando 'VOLTAR'.

        # 2. TRATAMENTO DE OPÇÃO VÁLIDA: Verifica se o número está dentro do range das opções de dados
        elif 1 <= escolha <= len(opcoes):
            return opcoes[escolha - 1]  # Retorna a string da opção escolhida (índice 0-based).

        # 3. TRATAMENTO DE ERRO DE RANGE: Se o número for inválido
        else:
            print(
                f"❌ Opa! O número {escolha} não está na lista. Tente entre 1 e {limite_superior}.")  # Mensagem de erro.


# --- Função Principal da Interface (Menu) ---

def menu_selecao_amigavel():
    """
    Define a função que gerencia os 3 menus interativos com navegação de retorno.
    """
    global dados_profissoes  # Declara uso da variável global de dados.

    # Descrições usadas no primeiro menu
    descricoes_areas = {
        "Exatas": "Foco em lógica, cálculos, números e sistemas.",
        "Humanas": "Foco em sociedade, cultura, comportamento e leis.",
        "Artes": "Foco em criatividade, estética, expressão e design.",
        "Biológicas": "Foco em vida, saúde, natureza e meio ambiente.",
        "Negócios": "Foco em gestão, mercado, finanças e estratégia."
    }

    # Variáveis de estado para armazenar as escolhas em cada nível
    escolha_1 = None  # Inicializa a escolha do Nível 1.
    escolha_2 = None  # Inicializa a escolha do Nível 2.
    escolha_3 = None  # Inicializa a escolha do Nível 3.
    passo_atual = 1  # Inicializa a variável de controle de estado do menu no Passo 1.

    exibir_titulo("Consultor de Carreira IA")  # Exibe o título principal do programa.
    print("Olá! Vou ajudar você a definir seu perfil profissional em 3 passos.")  # Mensagem de boas-vindas.
    time.sleep(1.5)  # Pausa dramática para leitura.

    # --- LOOP PRINCIPAL DE NAVEGAÇÃO ---
    # O loop executa enquanto o passo atual for menor ou igual a 3 (Passos 1, 2 e 3).
    while passo_atual <= 3:

        # --- PASSO 1: Grande Área (Nível 1) ---
        if passo_atual == 1:  # Verifica se o estado atual é o Passo 1.
            print("\n📊 PASSO 1: A GRANDE ÁREA")  # Título da etapa.
            for area, descricao in descricoes_areas.items():  # Itera e exibe as descrições.
                print(f"🔹 {area}: {descricao}")
            print("")

            opcoes_nivel_1 = list(dados_profissoes.keys())  # Obtém as chaves do dicionário principal.
            # Chama a função de escolha. Não permite voltar (False).
            resultado = obter_escolha_usuario(opcoes_nivel_1, "Grande Área", permitir_voltar=False)

            # Atualiza o estado: armazena a escolha e avança para o Passo 2.
            escolha_1 = resultado
            passo_atual = 2
            print(f"\n✅ Entendido! Vamos focar em **{escolha_1}**.")
            time.sleep(1)

        # --- PASSO 2: Subcategoria (Nível 2) ---
        elif passo_atual == 2:  # Verifica se o estado atual é o Passo 2.
            print(f"\n📂 PASSO 2: ESPECIALIDADE EM {escolha_1.upper()}")  # Título dinâmico baseado na escolha_1.
            print("Qual destes campos mais te atrai?\n")

            subcategorias = dados_profissoes[escolha_1]  # Acessa o dicionário de subcategorias com base na escolha_1.
            opcoes_nivel_2 = list(subcategorias.keys())  # Obtém a lista de campos de atuação.
            # Permite voltar para o Passo 1 (True).
            resultado = obter_escolha_usuario(opcoes_nivel_2, "Campo de Atuação", permitir_voltar=True)

            if resultado == "VOLTAR":  # Verifica se o usuário escolheu voltar.
                # Reinicia o estado para o Passo 1, limpando a escolha anterior.
                passo_atual = 1
                escolha_1 = None
                time.sleep(0.5)
                continue  # Volta ao início do loop 'while' para reexibir o Passo 1.

            # Atualiza o estado: armazena a escolha e avança para o Passo 3.
            escolha_2 = resultado
            passo_atual = 3
            print(f"\n✅ Ótima escolha: **{escolha_2}**.")
            time.sleep(1)

        # --- PASSO 3: Nicho Específico (Nível 3) ---
        elif passo_atual == 3:  # Verifica se o estado atual é o Passo 3.
            print(f"\n🎯 PASSO 3: NICHO EM {escolha_2.upper()}")  # Título dinâmico baseado na escolha_2.
            print("Para finalizar, qual é o seu foco específico?\n")

            areas_finais = dados_profissoes[escolha_1][escolha_2]  # Acessa a lista final de nichos.
            # Permite voltar para o Passo 2 (True).
            resultado = obter_escolha_usuario(areas_finais, "Nicho Específico", permitir_voltar=True)

            if resultado == "VOLTAR":  # Verifica se o usuário escolheu voltar.
                # Reinicia o estado para o Passo 2, limpando a escolha anterior.
                passo_atual = 2
                escolha_2 = None
                time.sleep(0.5)
                continue  # Volta ao início do loop 'while' para reexibir o Passo 2.

            # Sai do loop: armazena a escolha e define o passo como 4.
            escolha_3 = resultado
            passo_atual = 4

    # --- FINALIZAÇÃO (Executada após passo_atual se tornar 4) ---
    time.sleep(0.5)
    exibir_titulo("Resultado Gerado")  # Exibe o título final.

    # Constrói o prompt final concatenando as 3 escolhas.
    lista_prompt = [escolha_1, escolha_2, escolha_3]
    prompt_final = (
        f"Atuo na área de {lista_prompt[0]}, "
        f"especificamente no campo de {lista_prompt[1]}, "
        f"com foco profissional em {lista_prompt[2]}."
    )

    print("Aqui está o resumo do seu perfil:\n")  # Mensagem de conclusão.
    print(f"📝 \"{prompt_final}\"")  # Imprime o prompt gerado.
    print("\nObrigado por usar o sistema!")

    return prompt_final  # Retorna o prompt final que será enviado à API.


# --- Funções de Processamento de Dados (API e Mergesort) ---

def prompt_para_ia(prompt_texto):
    """ Envia um prompt para a API Gemini e retorna o texto de resposta. """
    global client  # Acessa a variável global do cliente da API.
    print(f"\n-> Enviando prompt para a API...")

    # Chamada da API: especifica o modelo e o conteúdo. Retorna apenas o texto.
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_texto
    ).text

    print("-> Resposta recebida.")
    return response  # Retorna o bloco de texto da IA.


def coletar_dados_da_api(response_text):
    """ Converte o texto da API (tópicos formatados) em uma lista de dicionários. """
    print("-> Formatando dados da API (Tópicos)...")
    if not response_text:  # Verifica se a resposta está vazia.
        return []

    dataframe_lista = []  # Inicializa a lista que atuará como nosso "dataframe".
    linhas = response_text.strip().split('\n')  # Divide o texto em linhas.

    for linha in linhas:  # Processa cada linha individualmente.
        linha_limpa = linha.strip()  # Remove espaços iniciais/finais.
        # Regex: Busca o padrão "* [Área]: [Curso]: [Salário]"
        match = re.match(r'^\*\s*(.*?)\s*:\s*(.*?)\s*:\s*([\d,.]+)', linha_limpa)

        if match:  # Se a linha corresponder ao padrão Regex:
            area = match.group(1).strip()  # Captura o Grupo 1 (Área).
            curso = match.group(2).strip()  # Captura o Grupo 2 (Curso).
            salario_str = match.group(3).strip()  # Captura o Grupo 3 (Salário, como string).

            # Limpeza do Salário:
            parte_inteira_str = salario_str.split(',')[0]  # Pega a parte antes da vírgula.
            salario_limpo_str = parte_inteira_str.replace(".", "")  # Remove pontos de milhar.
            salario_int = int(salario_limpo_str)  # Converte para inteiro (ponto de falha potencial).

            item_dicionario = {  # Cria o dicionário com os dados extraídos.
                'area': area,
                'curso': curso,
                'salario_estimado_mensal': salario_int  # Armazena o valor numérico (int).
            }
            dataframe_lista.append(item_dicionario)  # Adiciona o dicionário à lista.
        else:
            if linha_limpa:  # Ignora linhas totalmente vazias.
                print(f"-> Linha ignorada (formato de tópico não reconhecido): {linha}")

    print(f"-> {len(dataframe_lista)} tópicos convertidos para o dataframe.")
    return dataframe_lista  # Retorna a lista de dicionários.


def mostrar_dados(dados_lista, titulo="Dados da API"):
    """ Imprime a lista de dicionários formatada como tabela. """
    print(f"\n--- {titulo} ---")
    if not dados_lista:  # Verifica se há dados a serem exibidos.
        print("Nenhum dado para mostrar.")
        return

    # 1. Definição de Cabeçalhos
    header_area = "Área de Atuação"
    header_curso = "Curso Exemplo"
    header_salario = "Salário Mensal (R$)"

    # 2. Cálculo da largura máxima para garantir o alinhamento da tabela
    max_w_area = max(len(item['area']) for item in dados_lista)  # Largura máxima do campo 'area'.
    max_w_curso = max(len(item['curso']) for item in dados_lista)  # Largura máxima do campo 'curso'.
    max_w_salario_num = max(
        len(f"{item['salario_estimado_mensal']:,}") for item in dados_lista)  # Largura máxima do salário formatado.

    w_area = max(len(header_area), max_w_area)  # Largura final da coluna Área.
    w_curso = max(len(header_curso), max_w_curso)  # Largura final da coluna Curso.
    w_salario = max(len(header_salario), max_w_salario_num)  # Largura final da coluna Salário.
    sep = " | "  # Separador entre colunas.

    # 3. Impressão do Cabeçalho
    print(
        f"{header_area:<{w_area}}" + sep +  # Alinha a Área à esquerda.
        f"{header_curso:<{w_curso}}" + sep +  # Alinha o Curso à esquerda.
        f"{header_salario:>{w_salario}}"  # Alinha o Salário à direita.
    )
    total_width = w_area + w_curso + w_salario + len(sep) * 2  # Calcula o tamanho total da linha.
    print("-" * total_width)  # Imprime o separador horizontal.

    # 4. Impressão dos Dados
    for item in dados_lista:  # Itera sobre cada dicionário na lista.
        area = item['area']
        curso = item['curso']
        salario_f = f"{item['salario_estimado_mensal']:,}"  # Formata o número com separadores de milhar.

        print(
            f"{area:<{w_area}}" + sep +
            f"{curso:<{w_curso}}" + sep +
            f"{salario_f:>{w_salario}}"
        )


def organizar_dados(lista_de_dados, chave_para_ordenar):
    """
    Função principal do algoritmo Mergesort.
    """

    print(f"\nIniciando organização (Maior -> Menor) por '{chave_para_ordenar}'...")

    def merge(esquerda, direita):
        """ Função ANINHADA: Mescla duas sublistas ordenadas. """
        resultado_mesclado = []
        idx_esq, idx_dir = 0, 0

        while idx_esq < len(esquerda) and idx_dir < len(direita):  # Enquanto houver elementos nas duas listas
            # Comparação para ordenação DESCENDENTE (Maior >= Menor)
            if esquerda[idx_esq][chave_para_ordenar] >= direita[idx_dir][chave_para_ordenar]:
                resultado_mesclado.append(esquerda[idx_esq])  # Adiciona o item da esquerda (maior)
                idx_esq += 1  # Avança o índice da esquerda
            else:
                resultado_mesclado.append(direita[idx_dir])  # Adiciona o item da direita (maior)
                idx_dir += 1  # Avança o índice da direita

        # Adiciona o que sobrou de cada lista (após o loop principal)
        resultado_mesclado.extend(esquerda[idx_esq:])
        resultado_mesclado.extend(direita[idx_dir:])
        return resultado_mesclado

    def mergesort_interno(lista):
        """ Função ANINHADA: Recursiva que divide a lista. """
        if len(lista) <= 1:  # Caso Base: se 0 ou 1 elemento, retorna a lista (já ordenada)
            return lista

        # Divisão:
        meio = len(lista) // 2
        lado_esquerdo = lista[:meio]  # Primeira metade (do início até o meio)
        lado_direito = lista[meio:]  # Segunda metade (do meio até o fim)

        # Chamadas Recursivas:
        esquerdo_ordenado = mergesort_interno(lado_esquerdo)  # Ordena a metade esquerda
        direito_ordenado = mergesort_interno(lado_direito)  # Ordena a metade direita

        # Conquista (Mesclagem):
        return merge(esquerdo_ordenado, direito_ordenado)  # Mescla as duas metades ordenadas

    # Ponto de Partida: inicia o processo recursivo
    dados_ordenados = mergesort_interno(lista_de_dados)

    print("Organização concluída.")
    return dados_ordenados


# --- Execução Principal do Programa ---

if __name__ == "__main__":  # Bloco que garante que o código só é executado se o script for o principal.

    # 1. CONFIGURAÇÃO DA API
    minha_chave = configurar_chave_api()  # Chama a função para obter a chave do usuário/ambiente.
    client = genai.Client(api_key=minha_chave)  # Inicializa o cliente da API com a chave.

    # 2. CONSTRUÇÃO DO PROMPT
    prompt_contexto = menu_selecao_amigavel()  # Chama a função principal do menu, que retorna o texto do perfil.

    # Monta o prompt final detalhado, instruindo a IA sobre o formato de saída desejado.
    prompt_detalhado = f"""
    {prompt_contexto}.
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

    # 3. CHAMA A API
    resposta_em_texto = prompt_para_ia(prompt_detalhado)  # Envia o prompt para a IA e recebe o texto de volta.

    # 4. CONVERTE OS DADOS (ETL)
    minha_lista_api = coletar_dados_da_api(resposta_em_texto)  # Processa o texto da IA em uma lista de dicionários.

    # 5. PROCESSA E EXIBE
    if minha_lista_api:  # Verifica se a lista não está vazia.
        # Exibe a tabela na ordem original da API.
        mostrar_dados(minha_lista_api, "DataFrame Original (Ordem da API)")

        # Ordena a lista usando o Mergesort.
        lista_ordenada_salario = organizar_dados(minha_lista_api, 'salario_estimado_mensal')

        # Exibe a tabela ordenada pelo maior salário.
        mostrar_dados(lista_ordenada_salario, "DataFrame Ordenado (Maior Salário)")
    else:
        print("\nPrograma encerrado. Não foi possível processar os dados da API.")  # Mensagem de falha final.