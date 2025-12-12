# 🤖 RPA: Coleta de Clima e Preenchimento Automático

Este projeto é uma solução de **RPA (Robotic Process Automation)** que integra o consumo de uma API externa com automação web. O script coleta dados climáticos em tempo real de várias cidades e preenche automaticamente um formulário no Google Forms.

## 🚀 Funcionalidades

1.  **Consumo de API:** Conecta-se à *WeatherAPI* para obter dados meteorológicos (Temperatura, Umidade, Pressão) de uma lista definida de cidades.
2.  **Processamento de Dados:** Utiliza `Pandas` para estruturar os dados JSON recebidos em uma tabela organizada.
3.  **Automação Web:** Utiliza `Selenium` para abrir o navegador, acessar um formulário web e preencher os campos com os dados coletados, simulando a digitação humana.

## 🛠️ Tecnologias Utilizadas

* [Python 3](https://www.python.org/)
* [Requests](https://pypi.org/project/requests/) (Requisições HTTP)
* [Pandas](https://pandas.pydata.org/) (Manipulação de dados)
* [Selenium](https://www.selenium.dev/) (Automação de navegador)
* [WebDriver Manager](https://pypi.org/project/webdriver-manager/) (Gerenciamento automático de drivers)

## 📋 Pré-requisitos

Antes de começar, você precisa ter o **Google Chrome** instalado na sua máquina, pois o script utiliza o driver deste navegador.

### Instalação das dependências

Execute o comando abaixo no terminal para instalar as bibliotecas Python necessárias:

```bash
pip install requests pandas selenium webdriver-manager

⚙️ Configuração
Antes de executar, é necessário ajustar algumas variáveis no início do arquivo main.py:

1. Chave da API
Você precisará de uma chave de API gratuita do WeatherAPI. Substitua o valor da variável API_KEY:

Python

API_KEY = "SUA_CHAVE_AQUI" 
⚠️ Importante: Nunca suba sua chave de API real para um repositório público no GitHub.

2. Cidades e Formulário
Você pode alterar a lista de cidades e o link do formulário alvo:

Python

CIDADES = ['Londrina, PR', 'São Paulo, SP', 'Porto Alegre, RS']
URL_FORMULARIO = "[https://seu-formulario-google.com](https://seu-formulario-google.com)"
3. Estrutura do Formulário (Atenção)
O script utiliza a ordem dos campos (input[type='text']) para preencher os dados. Certifique-se de que seu Google Form tenha 5 perguntas de resposta curta na seguinte ordem:

Nome da Cidade

Data e Hora

Temperatura

Umidade

Pressão

▶️ Como Executar
Com as dependências instaladas e a configuração feita, execute o script:

Bash

python main.py
O que vai acontecer?
O script buscará os dados na API e mostrará o progresso no terminal.

Uma janela do Chrome será aberta automaticamente.

Para cada cidade, o script preencherá os campos e clicará em "Enviar".

Ao final, o navegador será fechado.

📷 Exemplo de Console
Plaintext

--- Iniciando Coleta de Dados (API) ---
Dados obtidos para: Londrina, PR
Dados obtidos para: São Paulo, SP

--- Iniciando Automação Web (Selenium) ---
Preenchendo formulário para: Londrina, PR...
Preenchendo formulário para: São Paulo, SP...
Automação finalizada com sucesso!

Nota: Este projeto foi desenvolvido para fins educacionais demonstrando a integração entre APIs REST e automação de interface (GUI).


---

### Observações sobre o código:

1.  **WebDriver Manager:**`ChromeDriverManager().install()`, evita que o código quebre quando o Google Chrome atualiza no computador.
2.  **Fragilidade do Google Forms:** O Google Forms muda as classes dos botões e inputs com frequência. O código usa uma lógica inteligente (`find_elements` por ordem e `xpath` buscando texto "Enviar"). Se o Google mudar o layout, pode ser necessário ajustar os seletores no futuro.
