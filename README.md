# 🤖 Consultor de Carreira IA (Global Solution)

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-blueviolet?logo=google)

Este projeto é uma solução desenvolvida para a Global Solution da disciplina *Dynamic Programming*.

O script utiliza a API do Google Gemini para atuar como um "Consultor de Carreira". Ele coleta o perfil profissional do usuário através de um menu interativo e, em seguida, busca na IA uma lista de 20 áreas relevantes, seus salários e cursos de exemplo.

O núcleo do projeto é a **extração**, **transformação** e **ordenação** desses dados:
1.  **Extração (E):** O texto não estruturado da IA é capturado.
2.  **Transformação (T):** O texto é processado com Regex, limpo e convertido em um "dataframe" (lista de dicionários).
3.  **Ordenação (L):** O dataframe é ordenado usando **Mergesort** para exibir as carreiras com maior salário.

---

## 🎯 Formulação do Problema (Requisito Acadêmico)

Este projeto atende aos requisitos da disciplina ao focar na manipulação e ordenação de dados dinâmicos.

* **Entrada:** Um bloco de texto não estruturado (string) contendo tópicos, retornado pela API do Google Gemini.
    * *Exemplo de linha de entrada:* `* Engenharia de Software: FIAP: 15000`
* **Saída:** Duas tabelas formatadas no console:
    1.  Um "dataframe" original, na ordem em que a API retornou.
    2.  Um "dataframe" ordenado (do maior para o menor) com base no salário.
* **Objetivo:** Processar a entrada não estruturada, transformá-la em um conjunto de dados estruturado (lista de dicionários) e aplicar um algoritmo de ordenação eficiente (Mergesort) para apresentar um relatório de ranking salarial.

---

## ✨ Funcionalidades e Estruturas

* **Menu Interativo:** Um menu amigável em 3 passos para definir o perfil do usuário.
* **Integração com IA:** Gera dados dinâmicos e relevantes em tempo real usando a API Gemini.
* **Parsing de Dados com Regex:** A função `coletar_dados_da_api` usa Expressões Regulares (`re.match`) para extrair e estruturar dados de forma robusta.
* **Algoritmo de Ordenação (Mergesort):** A função `organizar_dados` implementa o Mergesort (requerido na disciplina) para ordenar o dataframe pelo salário.
* **Funções Aninhadas:** A implementação do Mergesort utiliza funções aninhadas (`merge` e `mergesort_interno`) para modularizar o algoritmo.
* **Relatório de Saída Dinâmico:** A função `mostrar_dados` calcula dinamicamente a largura das colunas para criar uma tabela bonita e alinhada, independentemente do tamanho dos dados.

---

## 🚀 Começando

Siga estas instruções para configurar e executar o projeto em sua máquina local.

### 1. Pré-requisitos

* [Python 3.7+](https://www.python.org/downloads/)
* Acesso à Internet para a API do Google.

### 2. Instalação

1.  Clone este repositório (ou baixe os arquivos RAR):
    ```sh
    git clone https://github.com/leoGitFiap/GS_2_Semestre_2025_Dynamic_Programming
    cd Consultor_de_Carreira_IA_Global_Solution
    ```

2.  Instale a biblioteca necessária do Google:
    ```sh
    pip install -q -U google-genai
    ```

---

## 🔑 Configuração da Chave API (PARA EDITAR)

Para executar o script, você precisa de uma chave de API do Google Gemini.

### A. Obtendo sua Chave API

**[ATENÇÃO: EDITE ESTA SEÇÃO]**

> *(Aqui, explique passo a passo como você obteve a chave. Exemplo:)*
>
> 1.  Acesse o site do [Google AI Studio](https://aistudio.google.com/).
> 2.  Faça login com sua conta Google.
> 3.  Clique em "Get API key" (Obter chave de API).
> 4.  Crie uma nova chave de API em um projeto ("Create API key in new project").
> 5.  Copie a chave gerada.

### B. Inserindo a Chave no Projeto

Abra o arquivo `main.py` (ou o nome do seu script) e localize a linha `72`:

```python
# --- Configuração da API ---

try:
    # Cole sua chave de API aqui
    client = genai.Client(api_key="SUA_CHAVE_API_AQUI") # <-- COPIE SUA CHAVE AQUI
except Exception as e:
    # ...