import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurações
API_KEY = "<chave_aqui>" # minha chave no weatherapi.com
CIDADES = ['Londrina, PR', 'São Paulo, SP', 'Porto Alegre, RS', 'Florianópolis, SC']
URL_FORMULARIO = "https://forms.gle/pp5zSMEvmHisxjcn8"

def buscar_dados_clima():
    """
    Função responsável por conectar na API e baixar os dados.
    """
    print("--- Iniciando Coleta de Dados (API) ---")
    dados_coletados = []

    for cidade in CIDADES:
        # Montando o endereço da URL (Endpoint)
        # Ex: http://api.weatherapi.com/v1/current.json?key=XYZ&q=Londrina
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={cidade}&aqi=no"
        
        resposta = requests.get(url) # Fazendo a requisição GET
        
        if resposta.status_code == 200: #  200 = OK 
            
            dados_json = resposta.json() # Converte o texto recebido para JSON
            
            # Extraindo apenas os campos pedidos
            registro = {
                'Cidade': cidade,
                'Data e Hora': dados_json['location']['localtime'],
                'Temperatura (C)': dados_json['current']['temp_c'],
                'Umidade (%)': dados_json['current']['humidity'],
                'Pressão (mb)': dados_json['current']['pressure_mb']
            }
            dados_coletados.append(registro)
            print(f"Dados obtidos para: {cidade}")
        else:
            print(f"Erro ao buscar dados de {cidade}: {resposta.text}")

    
    return pd.DataFrame(dados_coletados) # Transforma a lista em uma tabela com os dados

def preencher_formulario(df_dados):
    """
    Função responsável por abrir o Chrome e preencher o Google Form.
    """
    print("\n--- Iniciando Automação Web (Selenium) ---")
    
    # Instala e configura o driver do Chrome automaticamente
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    
    # Para cada linha da nossa tabela de dados (coletada pela API)
    for index, linha in df_dados.iterrows():
        print(f"Preenchendo formulário para: {linha['Cidade']}...")
        
        # Entrar no site do formulário
        navegador.get(URL_FORMULARIO)
        
        time.sleep(2) # Espera 2 segundos para a página carregar (importante!)

        # Encontrar os campos de texto
        # O Google Forms costuma colocar inputs de texto simples como tags <input type='text'>  (importante!)
        # Pegar todos os campos de texto da tela, na ordem que aparecem
        campos_texto = navegador.find_elements(By.CSS_SELECTOR, "input[type='text']")
        
        # A sequencia depende da ordem das perguntas do formulário.
        # Ajustar os índices de acordo com a estrutura do formulario
        
        if len(campos_texto) >= 5:
            campos_texto[0].send_keys(str(linha['Cidade']))
            campos_texto[1].send_keys(str(linha['Data e Hora']))
            campos_texto[2].send_keys(str(linha['Temperatura (C)']))
            campos_texto[3].send_keys(str(linha['Umidade (%)']))
            campos_texto[4].send_keys(str(linha['Pressão (mb)']))
            
        else:
            print("Erro: Não foi encontrado campos suficientes no formulário.")
            break

        # Clicar no botão Enviar
        # O botão enviar geralmente tem classes específicas, mas podemos procurar pelo texto do botão (importante!)
        # O XPath procura: Um elemento span que contém o texto Enviar
        botao_enviar = navegador.find_elements(By.XPATH, "//span[contains(text(), 'Enviar')]")
        
        if botao_enviar:
            botao_enviar[0].click()
        else:
            # Caso o botão seja Submit ou outra tag
            botoes = navegador.find_elements(By.CSS_SELECTOR, "div[role='button']")
            for botao in botoes:
                if "Enviar" in botao.text or "Submit" in botao.text:
                    botao.click()
                    break
        
        # Espera um pouco antes de ir para o próximo para garantir que foi realizado o envio
        time.sleep(2)

    print("Automação finalizada com sucesso!")
    navegador.quit()  # Fecha o navegador no final

# principal
if __name__ == "__main__":
    #Pegar dados
    tabela_clima = buscar_dados_clima()
    
    #Verifica se conseguiu dados
    if not tabela_clima.empty:
        print("\nDados processados:")
        print(tabela_clima)
        
        #Preencher formulário
        preencher_formulario(tabela_clima)
    else:

        print("Nenhum dado foi coletado. Verifique sua API Key.")
