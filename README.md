# 🤖 Consultor de Carreira IA (Global Solution)

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-API-blueviolet?logo=google)

Este projeto é uma solução desenvolvida para a Global Solution da disciplina *Dynamic Programming*.

**Realizado pelo grupo:**
* Leonardo Fernandes Mesquita, RM:559623
* Marco Antonio Caires Freire, RM:559256
* Guilherme Augusto Caseiro, RM:559765

---

## 💡 Sobre o Projeto

O script utiliza a API do Google **Gemini 2.5 Flash** para atuar como um "**Consultor de Carreira**". Ele coleta o perfil profissional do usuário através de um menu interativo e, em seguida, busca na IA uma lista de 20 áreas relevantes, seus salários e cursos de exemplo.

O núcleo do projeto é a **extração**, **transformação** e **ordenação** desses dados:
1.  **Extração (E):** O texto não estruturado da IA é capturado.
2.  **Transformação (T):** O texto é processado com **Regex** (Expressões Regulares), limpo e convertido em um "dataframe" (lista de dicionários).
3.  **Ordenação (L):** O dataframe é ordenado usando o algoritmo **Mergesort** para exibir as carreiras com maior salário.

---

## 🎯 Formulação do Problema (Requisito Acadêmico)

Este projeto atende aos requisitos da disciplina ao focar na manipulação e ordenação de **dados dinâmicos**.

* **Entrada:** Um bloco de texto não estruturado (string) contendo tópicos, retornado pela API do Google Gemini.
    * *Exemplo de linha de entrada:* `* Engenharia de Software: FIAP: 15000`
* **Saída:** Duas tabelas formatadas no console:
    1.  Um "dataframe" original, na ordem em que a API retornou.
    2.  Um "dataframe" **ordenado** (do maior para o menor) com base no salário, usando o Mergesort.
* **Objetivo:** Processar a entrada não estruturada, transformá-la em um conjunto de dados estruturado (lista de dicionários) e aplicar um algoritmo de ordenação eficiente (Mergesort) para apresentar um relatório de ranking salarial.

---

## ✨ Funcionalidades e Estruturas

* **Menu Interativo:** Um menu amigável em 3 passos para definir o perfil do usuário, com navegação de **retorno** (`VOLTAR`).
* **Integração com IA:** Gera dados dinâmicos e relevantes em tempo real usando a API Gemini.
* **Parsing de Dados com Regex:** A função `coletar_dados_da_api` usa Expressões Regulares (`re.match`) para extrair e estruturar dados de forma robusta a partir de um formato pré-definido pela IA.
* **Algoritmo de Ordenação (Mergesort):** A função `organizar_dados` implementa o **Mergesort** (requerido na disciplina) com complexidade $O(n \log n)$ para ordenar o dataframe pelo salário.
* **Funções Aninhadas:** A implementação do Mergesort utiliza funções aninhadas (`merge` e `mergesort_interno`) para modularizar o algoritmo e garantir o fluxo recursivo.
* **Relatório de Saída Dinâmico:** A função `mostrar_dados` calcula dinamicamente a largura das colunas para criar uma tabela bonita e alinhada no console, independentemente do tamanho dos dados.

---

## 🚀 Começando

Siga estas instruções para configurar e executar o projeto em sua máquina local.

### 1. Pré-requisitos

* [Python 3.7+](https://www.python.org/downloads/)
* Acesso à Internet para a API do Google.

### 2. Instalação

1.  Clone este repositório (ou baixe os arquivos):
    ```sh
    git clone https://github.com/leoGitFiap/GS_2_Semestre_2025_Dynamic_Programming
    cd Consultor_de_Carreira_IA_Global_Solution
    ```

2.  Instale a biblioteca necessária do Google:
    ```sh
    pip install -q -U google-genai
    ```

---

## 🔑 Configuração da Chave API

O script tentará primeiro ler a chave da variável de ambiente `GOOGLE_API_KEY`. Se não encontrar, ele solicitará a chave no console.

### A. Obtendo sua Chave API

1.  Acesse o site do [Google AI Studio](https://aistudio.google.com/).
2.  Faça login com sua conta Google.
3.  Clique em "Get API key" (Obter chave de API).
4.  Crie uma nova chave de API em um projeto ("Create API key in new project").
5.  **Copie a chave gerada.**

### B. Executando e Inserindo a Chave

1.  Execute o script:
    ```sh
    python seu_script.py 
    # (ou python main.py, dependendo do nome do seu arquivo)
    ```
2.  O script exibirá:
    ```
    ⚠️ Nenhuma chave de ambiente encontrada.
    Você precisa de uma chave Gemini válida (aistudio.google.com).
    
    Digite o Chave de API (ou digite 'sair'): 
    ```
3.  Cole a chave copiada no terminal e pressione Enter. A conexão será validada antes de iniciar o menu interativo.