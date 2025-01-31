from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException,ElementNotInteractableException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time
import pandas as pd
import requests

from verificar_chrome import *

def login(nav):

    try:
        # logando
        WebDriverWait(nav, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="username"]'))).send_keys("ti.prod")
        WebDriverWait(nav, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="password"]'))).send_keys("Cemag@15")
        WebDriverWait(nav, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="password"]'))).send_keys(Keys.ENTER)

        print("Acessou a página de login")

    except Exception as e:
        print(f"Ocorreu um erro durante o login: {e}")

def menu_innovaro_1(nav):
    
    """
    Função para abrir ou fechar menu no innovaro do tipo 1
    :nav: webdriver
    """
    
    #abrindo menu

    try:
        nav.switch_to.default_content()
    except:
        pass

    menu=WebDriverWait(nav, 10).until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'menuBar-button-label')))
    time.sleep(2.5)
    menu.click()
    time.sleep(2.5)

def menu_innovaro_2(nav):
    
    """
    Função para abrir ou fechar menu no innovaro do tipo 2
    :nav: webdriver
    """
    
    #abrindo menu

    try:
        nav.switch_to.default_content()
    except:
        pass

    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="bt_1898143037"]/table/tbody/tr/td[2]'))).click()

    time.sleep(2)

def menu_cadastro(nav):
    
    nav.switch_to.default_content()
    
    #menu
    try:
        menu_innovaro_1(nav)
        print('Menu aberto')
    except TimeoutException:
        print('Erro ao clicar no menu')
        return
    time.sleep(2)
    
    #Clicando em Projeto
    lista_menu, test_list = listar(nav, 'webguiTreeNodeLabel')
    time.sleep(2)
    click_producao = test_list.loc[test_list[0] == 'Projeto'].reset_index(drop=True)['index'][0]
    lista_menu[click_producao].click()
    time.sleep(2)

    #Clicando em Materiais e Produtos
    lista_menu, test_list = listar(nav, 'webguiTreeNodeLabel')
    time.sleep(2)
    click_producao = test_list.loc[test_list[0] == 'Materiais e Produtos'].reset_index(drop=True)['index'][0]
    lista_menu[click_producao].click()
    time.sleep(2)

    #menu
    try:
        menu_innovaro_1(nav)
        print('Menu aberto')
    except TimeoutException:
        print('Erro ao clicar no menu')
        return
    time.sleep(2)

    #Clicando em Projeto
    lista_menu, test_list = listar(nav, 'webguiTreeNodeLabel')
    time.sleep(2)
    click_producao = test_list.loc[test_list[0] == 'Projeto'].reset_index(drop=True)['index'][0]
    lista_menu[click_producao].click()
    time.sleep(2)

    #menu
    try:
        menu_innovaro_1(nav)
        print('Menu aberto')
    except TimeoutException:
        print('Erro ao clicar no menu')
        return
    time.sleep(2)
    
    #menu
    try:
        print('Menu fechado')
    except TimeoutException:
        print('Erro ao clicar no menu')
        return
    time.sleep(2)

def iframes(nav):
    
    iframe_list = nav.find_elements(By.CLASS_NAME, 'tab-frame')

    for iframe in range(len(iframe_list)):
        time.sleep(1)
        try:
            nav.switch_to.default_content()
            nav.switch_to.frame(iframe_list[iframe])
            print(iframe)
        except:
            pass

def listar(nav, classe):

    try:

        lista_menu = nav.find_elements(By.CLASS_NAME, classe)

        elementos_menu = []

        for x in range(len(lista_menu)):
            a = lista_menu[x].text
            elementos_menu.append(a)

        test_lista = pd.DataFrame(elementos_menu)
        test_lista = test_lista.loc[test_lista[0] != ""].reset_index()

        print("listou as opções do menu")

    except Exception as e:
        print(f"Ocorreu um erro durante a listagem de opções: {e}")

    return (lista_menu, test_lista)

def add_novo_item(nav):

    nav.switch_to.default_content()
    iframes(nav)

    # Clicar em adicionar novo item
    try:
        WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer"]//div[@id="insertButton"]'))).click()
        time.sleep(1.5)
    except:
        status = 'Erro ao clicar na lupa'
        return status
    
def mudar_visualizacao(nav, xpath, xpath_classe, classe_esperada, max_tentativas=5, intervalo=2):
    """
    Tenta clicar em um botão para mudar a visualização e verifica se uma classe específica aparece.
    """

    tentativas = 0
    actions = ActionChains(nav)

    while tentativas < max_tentativas:
        try:
            
            classe_atual = WebDriverWait(nav, 1).until(EC.presence_of_element_located((By.XPATH, xpath_classe))).get_attribute('class')

            if classe_atual == classe_esperada:
                print(f"Classe esperada '{classe_esperada}' detectada!")
                return True
            else:
                # Localizar o botão
                btn = WebDriverWait(nav, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))

                # Clicar no botão
                actions.move_to_element(btn).click().perform()
                print(f"Tentativa {tentativas + 1}: Botão clicado.")
            
        except TimeoutException:
            print(f"Tentativa {tentativas + 1}: Timeout - Elemento não encontrado ou classe não atualizada.")
        except (StaleElementReferenceException, ElementNotInteractableException) as e:
            print(f"Tentativa {tentativas + 1}: Erro ao interagir com o elemento: {e}")
        
        # Incrementa tentativas e espera antes de tentar novamente
        tentativas += 1
        time.sleep(intervalo)

    print("Falha ao encontrar a classe esperada após o número máximo de tentativas.")
    return False

def digitar_como_humano(elemento, texto, intervalo=0.1):
    for letra in texto:
        elemento.send_keys(letra)  # Envia uma letra de cada vez
        time.sleep(intervalo)  # Aguarda um intervalo entre cada letra

def verificar_se_erro(nav):

    nav.switch_to.default_content()

    time.sleep(3)

    try:
        error = WebDriverWait(nav, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="errorMessageBox"]'))).text
        confirm_button = WebDriverWait(nav, 4).until(EC.presence_of_element_located((By.XPATH, "//button[@id='confirm']")))
        time.sleep(2)
        confirm_button.click()
        time.sleep(2)
    except:
        iframes(nav)
        return None
    
    iframes(nav)
    return error

def carregamento(nav):

    nav.switch_to.default_content()

    print('procurando carregamento 1')
    try:
        # Espera inicial para verificar se a mensagem de carregamento existe
        carregamento = WebDriverWait(nav, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="statusMessageBox"]')))
        
        # Enquanto o elemento existir, continue verificando
        while True:
            print("Carregando...")
            try:
                # Aguarde novamente pela presença do elemento
                carregamento = WebDriverWait(nav, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="statusMessageBox"]')))
            except TimeoutException:
                # Se o elemento não for encontrado, interrompa o loop
                iframes(nav)
                return
    except TimeoutException:
        # Não há mensagem de carregamento inicial
        pass    

    print('procurando carregamento 2')
    try:
        # Espera inicial para verificar se a mensagem de carregamento existe
        carregamento =  WebDriverWait(nav, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="waitMessageBox"]')))
        
        # Enquanto o elemento existir, continue verificando
        while True:
            print("Carregando...")
            try:
                # Aguarde novamente pela presença do elemento
                carregamento =  WebDriverWait(nav, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="waitMessageBox"]')))
            except TimeoutException:
                # Se o elemento não for encontrado, interrompa o loop
                iframes(nav)
                return
    except TimeoutException:
        # Não há mensagem de carregamento inicial
        pass  

    print('procurando carregamento 3')
    try:
        # Espera inicial para verificar se a mensagem de carregamento existe
        carregamento =  WebDriverWait(nav, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="progressMessageBox"]')))
        
        # Enquanto o elemento existir, continue verificando
        while True:
            print("Carregando...")
            try:
                # Aguarde novamente pela presença do elemento
                carregamento =  WebDriverWait(nav, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="progressMessageBox"]')))
            except TimeoutException:
                # Se o elemento não for encontrado, interrompa o loop
                iframes(nav)
                return
    except TimeoutException:
        # Não há mensagem de carregamento inicial
        pass    

    print('procurando carregamento 4')
    try:
        # Espera inicial para verificar se a mensagem de carregamento existe
        carregamento = WebDriverWait(nav, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content_waitMessageBox"]')))
        
        # Enquanto o elemento existir, continue verificando
        while True:
            print("Carregando...")
            try:
                # Aguarde novamente pela presença do elemento
                carregamento = WebDriverWait(nav, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content_waitMessageBox"]')))
            except TimeoutException:
                # Se o elemento não for encontrado, interrompa o loop
                iframes(nav)
                return
    except TimeoutException:
        # Não há mensagem de carregamento inicial
        iframes(nav)
        pass 

    iframes(nav)

# def guardar_erro(nav, erro):
def preencher_cadastro_peca(nav, dados):

    status = 'ok'
    actions = ActionChains(nav)

    # for item in dados['peca']:
    # item
    # info genericas
    # iframes(nav)

    try:
        time.sleep(2)
        codigo_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer"]//input[@name="CODIGO"]')))
        codigo_input.send_keys(Keys.CONTROL + 'A')
        time.sleep(1.5)
        codigo_input.send_keys(dados['peca']['codigo'])
        time.sleep(1.5)
        codigo_input.send_keys(Keys.TAB)
        print('Codigo ok')

        carregamento(nav)

        #verifica se mostrou erro
        erro=verificar_se_erro(nav)
        if erro:
            print(f"{erro}, informar na base e pular para outro item")

            # return erro

        ref_principal_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer"]//input[@name="REFERENCIAPRINCIPAL"]')))
        ref_principal_input.click()
        ref_principal_input.send_keys(Keys.CONTROL + 'A')
        time.sleep(1.5)
        ref_principal_input.send_keys(dados['peca']['ref_principal'])
        # digitar_como_humano(ref_principal_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
        time.sleep(1.5)
        ref_principal_input.send_keys(Keys.TAB)
        print('ref principal ok')

        carregamento(nav)

        #verifica se mostrou erro
        erro=verificar_se_erro(nav)
        if erro:
            print(f"{erro}, informar na base e pular para outro item")

            # return erro
        
        classe_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer"]//input[@name="CLASSE"]')))
        classe_input.send_keys(Keys.CONTROL + 'A')
        time.sleep(1.5)
        classe_input.send_keys(dados['peca']['classe'])
        # digitar_como_humano(classe_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
        time.sleep(1.5)
        classe_input.send_keys(Keys.TAB)
        print('classe ok')

        carregamento(nav)

        #verifica se mostrou erro
        erro=verificar_se_erro(nav)
        if erro:
            print(f"{erro}, informar na base e pular para outro item")

            # return erro

        nome_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer"]//input[@name="NOME"]')))
        nome_input.send_keys(Keys.CONTROL + 'A')
        time.sleep(1.5)
        nome_input.send_keys(dados['peca']['nome'])
        # digitar_como_humano(nome_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
        time.sleep(1.5)
        nome_input.send_keys(Keys.TAB)
        time.sleep(0.5)
        print('nome ok')

        desc_generica_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer"]//input[@name="DESCRICAOGENERICA"]')))
        desc_generica_input.send_keys(Keys.CONTROL + 'A')
        time.sleep(1.5)
        desc_generica_input.send_keys(dados['peca']['desc_generica'])
        # digitar_como_humano(desc_generica_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
        time.sleep(1.5)
        desc_generica_input.send_keys(Keys.TAB)
        time.sleep(0.5)
        print('desc generica ok')

        un_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer"]//input[@name="UNIDMEDIDA"]')))
        un_input.send_keys(Keys.CONTROL + 'A')
        time.sleep(1.5)
        un_input.send_keys(dados['peca']['un'])
        # digitar_como_humano(un_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
        time.sleep(1.5)
        un_input.send_keys(Keys.TAB)
        time.sleep(0.5)
        print('unidade ok')

    except:
        status = 'Erro no input de info genericas'
        registrar_status(dados['peca']['codigo'], status)
        # return status

    # info fiscais
    try:
        class_fiscal_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer"]//input[@name="CLFISCAL"]')))
        class_fiscal_input.send_keys(Keys.CONTROL + 'A')
        time.sleep(1.5)
        class_fiscal_input.send_keys(dados['peca']['class_fiscal'])
        # digitar_como_humano(class_fiscal_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
        time.sleep(1.5)
        class_fiscal_input.send_keys(Keys.TAB)
        print('class fiscal ok')

        carregamento(nav)

        #verifica se mostrou erro
        erro=verificar_se_erro(nav)
        if erro:
            print(f"{erro}, informar na base e pular para outro item")

            # return erro

        procedencia_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer"]//input[@name="PROCEDENCI"]')))
        procedencia_input.send_keys(Keys.CONTROL + 'A')
        time.sleep(1.5)
        procedencia_input.send_keys(dados['peca']['procedencia'])
        # digitar_como_humano(procedencia_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
        time.sleep(1.5)
        procedencia_input.send_keys(Keys.TAB)
        print('procedencia ok')

        carregamento(nav)

        #verifica se mostrou erro
        erro=verificar_se_erro(nav)
        if erro:
            print(f"{erro}, informar na base e pular para outro item")

            # return erro

    except:
        status = 'Erro no input de info fiscais'
        registrar_status(dados['peca']['codigo'], status)
        # return status

    #Clicar na tabela de etapas e composição de recursos
    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA"]'))).click()
    time.sleep(4)
    print('click na tabela de etapas e composição de recursos')

    # Clica em adicionar etapa
    clicar_ate_classe(nav,'//*[@id="explorer_RECURSOETAPA"]//div[@id="insertButton"]','grid-titleBar-button grid-titleBar-newRecordButton-inactive')
    time.sleep(2)
    print('click em adicionar etapa')

    # Clicar no campo de ordem
    WebDriverWait(nav, 4).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//input[@name="ORDEM"]'))).click()
    time.sleep(2)
    print('click em campo de ordem')

    #Mudar visualização de etapas
    mudar_visualizacao(nav, '//*[@id="explorer_RECURSOETAPA"]//div[@id="changeViewButton"]', '//*[@id="explorer_RECURSOETAPA"]//input[@name="ORDEM"]','field formView editingRecord focus control-input')
    print('mudar visualização de etapas')

    cont_etapa=1

    for etapa in dados['etapas']:
        # etapa = dados['etapas'][0]

        actions = ActionChains(nav)

        try:
            checkboxAponta = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="checkbox" and @name="APONTA"]')))
            actions.move_to_element(checkboxAponta).click().perform()
            time.sleep(2)

            checkboxAponta = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="checkbox" and @name="APONTA"]')))
            if not checkboxAponta.is_selected():
                actions.move_to_element(checkboxAponta).click().perform()
            
            # Preenche o campo "Ordem"
            ordem_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//input[@name="ORDEM"]')))
            ordem_input.send_keys(Keys.CONTROL + 'A')
            time.sleep(1.5)
            ordem_input.send_keys(str(etapa['ordem']))
            # digitar_como_humano(ordem_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
            time.sleep(1.5)
            ordem_input.send_keys(Keys.TAB)
            print('ordem ok')

            carregamento(nav)

            #verifica se mostrou erro
            erro=verificar_se_erro(nav)
            if erro:
                print(f"{erro}, informar na base e pular para outro item")

                # return erro

            # Preenche o campo "Processo"
            processo_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//input[@name="PROCESSO"]')))
            processo_input.send_keys(Keys.CONTROL + 'A')
            time.sleep(1.5)
            processo_input.send_keys(etapa['processo'])
            time.sleep(1.5)
            processo_input.send_keys(Keys.TAB)
            # digitar_como_humano(processo_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
            time.sleep(1.5)
            processo_input.send_keys(Keys.TAB)
            print('processo ok')

            carregamento(nav)

            #verifica se mostrou erro
            erro=verificar_se_erro(nav)
            if erro:
                print(f"{erro}, informar na base e pular para outro item")

                # return erro

            # Preenche o campo "Descrição"
            descricao_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//textarea[@name="DESCRICAO"]')))
            descricao_input.send_keys(Keys.CONTROL + 'A')
            time.sleep(1.5)
            descricao_input.send_keys(etapa['descricao'])
            # digitar_como_humano(descricao_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
            time.sleep(1.5)
            descricao_input.send_keys(Keys.TAB)
            print('descricao ok')

            carregamento(nav)

            #verifica se mostrou erro
            erro=verificar_se_erro(nav)
            if erro:
                print(f"{erro}, informar na base e pular para outro item")

                # return erro

            # Preenche o campo "Destino"
            destino_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//input[@name="DEPOSITO"]')))
            destino_input.send_keys(Keys.CONTROL + 'A')
            time.sleep(1.5)
            destino_input.send_keys(etapa['destino'])
            # digitar_como_humano(destino_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
            time.sleep(1.5)
            destino_input.send_keys(Keys.TAB)
            print('destino ok')

            carregamento(nav)

            #verifica se mostrou erro
            erro=verificar_se_erro(nav)
            if erro:
                print(f"{erro}, informar na base e pular para outro item")

                # return erro

            # Preenche o campo "Desvio"
            desvio_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//input[@name="DEPOSITODE"]')))
            desvio_input.send_keys(Keys.CONTROL + 'A')
            time.sleep(1.5)
            desvio_input.send_keys(etapa['desvio'])
            # digitar_como_humano(desvio_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
            time.sleep(1.5)
            desvio_input.send_keys(Keys.TAB)
            print('desvio ok')

            carregamento(nav)

            #verifica se mostrou erro
            erro=verificar_se_erro(nav)
            if erro:
                print(f"{erro}, informar na base e pular para outro item")

                # return erro

        except Exception as e:
            print(f"Erro ao preencher a etapa {etapa['ordem']}: {e}")
            status = 'Erro no preenchimento de etapas'
            # registrar_status(dados['peca']['codigo'], status)
            # return status  

        time.sleep(2)

        if cont_etapa == 1:
            # Recursos
            # Clique na tabela de recursos
            WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]'))).click()
            time.sleep(2)
            print('click tabela de recursos')

            #Clica em adicionar etapa
            clicar_ate_classe(nav,'//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//div[@id="insertButton"]','grid-titleBar-button grid-titleBar-newRecordButton-inactive')
            time.sleep(2)
            print('click add etapa')

            # Clicar no campo de ordem
            WebDriverWait(nav, 4).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//tr[@id=0]//td[@fieldname="ORDEM"]'))).click()
            time.sleep(2)
            print('click campo de ordem')

            #Mudar visualização de recursos
            mudar_visualizacao(nav, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//div[@id="changeViewButton"]', '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//input[@name="ORDEM"]','field formView editingRecord focus control-input')
            print('click mudar visualização')

            for recurso in dados['recursos']:

                # recurso = dados['recursos'][1]

                try:

                    # Preenche o campo "Ordem"
                    ordem_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                        By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//input[@name="ORDEM"]')))    
                    ordem_input.send_keys(Keys.CONTROL + 'A')
                    time.sleep(1.5)
                    ordem_input.send_keys(str(recurso['ordem']))
                    # digitar_como_humano(ordem_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
                    time.sleep(1.5)
                    ordem_input.send_keys(Keys.TAB)
                    print('ordem ok')

                    carregamento(nav)

                    #verifica se mostrou erro
                    erro=verificar_se_erro(nav)
                    if erro:
                        print(f"{erro}, informar na base e pular para outro item")
                        registrar_status(dados['peca']['codigo'], erro)
                        # return erro

                    # Preenche o campo "Recurso"
                    recurso_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                        By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//input[@name="RECURSO"]')))    
                    recurso_input.send_keys(Keys.CONTROL + 'A')
                    time.sleep(1.5)
                    recurso_input.send_keys(recurso['recurso']['codigo'])
                    # digitar_como_humano(recurso_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
                    time.sleep(3)
                    recurso_input.send_keys(Keys.TAB)
                    print('recurso ok')

                    carregamento(nav)

                    #verifica se mostrou erro
                    erro=verificar_se_erro(nav)
                    if erro:
                        print(f"{erro}, informar na base e pular para outro item")
                        registrar_status(dados['peca']['codigo'], erro)
                        # return erro

                    # Preenche o campo "Quantidade"
                    quantidade_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                        By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//input[@name="QUANTIDADE"]')))    
                    quantidade_input.send_keys(Keys.CONTROL + 'A')
                    time.sleep(1.5)
                    quantidade_input.send_keys(recurso['quantidade'])
                    # digitar_como_humano(quantidade_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
                    time.sleep(1.5)
                    quantidade_input.send_keys(Keys.TAB)
                    print('quantidade ok')

                    carregamento(nav)

                    #verifica se mostrou erro
                    erro=verificar_se_erro(nav)
                    if erro:
                        print(f"{erro}, informar na base e pular para outro item")
                        registrar_status(dados['peca']['codigo'], erro)
                        # return erro

                    # Preenche o campo "Depósito origem"
                    destino_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                        By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//input[@name="DEPOSITO"]')))    
                    destino_input.send_keys(Keys.CONTROL + 'A')
                    time.sleep(1.5)
                    destino_input.send_keys(recurso['dep_origem'])
                    # digitar_como_humano(destino_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
                    time.sleep(1.5)
                    destino_input.send_keys(Keys.TAB)
                    print('destino ok')

                    carregamento(nav)

                    #verifica se mostrou erro
                    erro=verificar_se_erro(nav)
                    if erro:
                        print(f"{erro}, informar na base e pular para outro item")

                        # return erro

                    # Clica no botão "Inserir" ou "Finalizar"
                    if recurso != dados['recursos'][-1]:  # Se não for a última etapa
                        # WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//*[@id="postButton"]'))).click()
                        clicar_ate_classe(nav,'//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//div[@id="postButton"]','grid-titleBar-button grid-titleBar-saveRecordButton-inactive')
                        time.sleep(1.5)
                        clicar_ate_classe(nav,'//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//div[@id="insertButton"]','grid-titleBar-button grid-titleBar-newRecordButton-inactive')
                        time.sleep(1.5)

                    else:  # Última etapa, finaliza
                        clicar_ate_classe(nav,'//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//div[@id="postButton"]','grid-titleBar-button grid-titleBar-saveRecordButton-inactive')
                        carregamento(nav)
                        time.sleep(1.5)

                except Exception as e:
                    print(f"Erro ao preencher recurso: {e}")
                    status = 'Erro no preenchimento de recursos'
                    registrar_status(dados['peca']['codigo'], status)
                    # return status   

            #Propriedades
            if dados['propriedades']:

                # Clique na tabela de propriedades
                WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]'))).click()
                time.sleep(2)
                print('click na tabela de propriedades')

                #Clica em adicionar propriedade
                clicar_ate_classe(nav,'//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//div[@id="insertButton"]','grid-titleBar-button grid-titleBar-newRecordButton-inactive')
                time.sleep(2)
                print('click add propriedades')

                # Clicar no campo de ordem
                WebDriverWait(nav, 4).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//tr[@id=0]//td[@fieldname="CAMPOINTEIRO"]'))).click()
                time.sleep(2)
                print('click ordem')

                #Mudar visualização de propriedades
                mudar_visualizacao(nav, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//div[@id="changeViewButton"]', '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//tr[@id=0]//td[@fieldname="CAMPOINTEIRO"]','grid-cell tableView browsingRecord editingRecord focus')
                print('mudar visualização')

                for propriedade in dados['propriedades']:
                    try:
                        propriedade_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//input[@name="CAMPOINTEIRO"]')))
                        propriedade_input.send_keys(propriedade['propriedade'])
                        time.sleep(2)
                        propriedade_input.send_keys(Keys.TAB)
                        time.sleep(1)

                        valor_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//input[@name="VALOR"]')))
                        time.sleep(2)
                        valor_input.click()
                        time.sleep(2)
                        valor_input.send_keys(propriedade['valor'])
                        time.sleep(2)
                        valor_input.send_keys(Keys.TAB)
                        time.sleep(2)
                        print('valor input')

                        carregamento(nav)

                        #verifica se mostrou erro
                        erro=verificar_se_erro(nav)
                        if erro:
                            print(f"{erro}, informar na base e pular para outro item")

                            # return erro

                        # verificando se o campo de propriedade está preenchido
                        propriedade_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//input[@name="CAMPOINTEIRO"]')))
                        
                        if propriedade_input.get_attribute('value') == '':
                            propriedade_input.send_keys(propriedade['propriedade'])
                            time.sleep(2)
                            propriedade_input.send_keys(Keys.TAB)
                            time.sleep(1)




                        # Clica no botão "Inserir" ou "Finalizar"
                        if propriedade != dados['propriedades'][-1]:  # Se não for a última etapa
                            # WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//*[@id="postButton"]'))).click()
                            clicar_ate_classe(nav,'//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//div[@id="postButton"]','grid-titleBar-button grid-titleBar-saveRecordButton-inactive')
                            carregamento(nav)

                            clicar_ate_classe(nav,'//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//div[@id="insertButton"]','grid-titleBar-button grid-titleBar-newRecordButton-inactive')
                            carregamento(nav)

                            #verifica se mostrou erro
                            erro=verificar_se_erro(nav)
                            if erro:
                                print(f"{erro}, informar na base e pular para outro item")
                                # return erro
                        
                        else:  # Última etapa, finaliza
                            clicar_ate_classe(nav,'//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//div[@id="postButton"]','grid-titleBar-button grid-titleBar-saveRecordButton-inactive')
                            carregamento(nav)

                            #verifica se mostrou erro
                            erro=verificar_se_erro(nav)
                            if erro:
                                print(f"{erro}, informar na base e pular para outro item")
                                # return erro

                    except Exception as e:
                        print(f"Erro ao preencher a propriedade: {e}")
                        status = 'Erro no preenchimento de propriedades'
                        registrar_status(dados['peca']['codigo'], status)
                        # return status

            else:
                time.sleep(2)
                #Mudar visualização de propriedades
                changeViewButton = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//div[@id="changeViewButton"]')))
                time.sleep(2)
                actions.move_to_element(changeViewButton).click().perform()
                time.sleep(2)
        
        # cont_etapa+=1

        # if etapa != dados['etapas'][-1]:  # Se não for a última etapa
        #     # WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//*[@id="postButton"]'))).click()
        #     clicar_ate_classe(nav,'//*[@id="explorer_RECURSOETAPA"]//div[@id="postButton"]','grid-titleBar-button grid-titleBar-saveRecordButton-inactive')
        #     clicar_ate_classe(nav,'//*[@id="explorer_RECURSOETAPA"]//div[@id="insertButton"]','grid-titleBar-button grid-titleBar-newRecordButton-inactive')
        #     time.sleep(1.5)
        # else:  # Última etapa, finaliza
        #     clicar_ate_classe(nav,'//*[@id="explorer_RECURSOETAPA"]//div[@id="postButton"]','grid-titleBar-button grid-titleBar-saveRecordButton-inactive')
        #     time.sleep(1.5)

        time.sleep(5)

    # registrar_status(dados['peca']['codigo'], status)

    # nav.switch_to.default_content()

    time.sleep(0.5)
    # Fechar aba ativa
    # WebDriverWait(nav, 4).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tabs"]//div[@class="process-tab-right-active"]'))).click()

    # recomecar(nav)

    return status

def preencher_cadastro_conjunto(nav, dados):

    status = 'ok'
    
    for item in dados['pecas']:
        
        # info genericas
        try:
            time.sleep(2)
            codigo_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[2]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/table/tbody/tr/td[1]/input')))
            codigo_input.send_keys(Keys.CONTROL + 'A')
            time.sleep(1.5)
            codigo_input.send_keys(item['peca']['codigo'])
            # digitar_como_humano(codigo_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
            time.sleep(1.5)

            ref_principal_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[2]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[5]/td[2]/table/tbody/tr/td[1]/input')))
            ref_principal_input.click()
            #verifica se mostrou erro
            try:
                nav.switch_to.default_content()
                status=WebDriverWait(nav, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="errorMessageBox"]/div[2]/table/tbody/tr[1]/td[2]/div/div/span[1]'))).text
                
                time.sleep(2)

                #fecha aba
                WebDriverWait(nav, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tabs"]/td[1]/table/tbody/tr/td[4]/span/div'))).click()

                registrar_status(item['peca']['codigo'], status)
                return status
            except:
                iframes(nav)
                pass    

            ref_principal_input.send_keys(Keys.CONTROL + 'A')
            time.sleep(1.5)
            ref_principal_input.send_keys(item['peca']['ref_principal'])
            # digitar_como_humano(ref_principal_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
            time.sleep(1.5)

            classe_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[2]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[7]/td[2]/table/tbody/tr/td[1]/input')))
            classe_input.send_keys(Keys.CONTROL + 'A')
            time.sleep(1.5)
            classe_input.send_keys(item['peca']['classe'])
            # digitar_como_humano(classe_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
            time.sleep(1.5)

            nome_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[2]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[4]/table/tbody/tr/td[1]/input')))
            nome_input.send_keys(Keys.CONTROL + 'A')
            time.sleep(1.5)
            nome_input.send_keys(item['peca']['nome'])
            # digitar_como_humano(nome_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
            time.sleep(1.5)

            desc_generica_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[2]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[5]/td[4]/table/tbody/tr/td[1]/input')))
            desc_generica_input.send_keys(Keys.CONTROL + 'A')
            time.sleep(1.5)
            desc_generica_input.send_keys(item['peca']['desc_generica'])
            # digitar_como_humano(desc_generica_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
            time.sleep(1.5)

            un_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[2]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[7]/td[4]/table/tbody/tr/td[1]/input')))
            un_input.send_keys(Keys.CONTROL + 'A')
            time.sleep(1.5)
            un_input.send_keys(item['peca']['un'])
            # digitar_como_humano(un_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
            time.sleep(1.5)

        except:
            status = 'Erro no input de info genericas'
            registrar_status(item['peca']['codigo'], status)
            return status

        # info fiscais
        try:
            class_fiscal_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[2]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[2]/table/tbody/tr/td[1]/input')))
            class_fiscal_input.send_keys(Keys.CONTROL + 'A')
            time.sleep(1.5)
            class_fiscal_input.send_keys(item['peca']['class_fiscal'])
            # digitar_como_humano(class_fiscal_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
            time.sleep(1.5)

            procedencia_input=WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[2]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[4]/td/table/tbody/tr[3]/td[4]/table/tbody/tr/td[1]/input')))
            procedencia_input.send_keys(Keys.CONTROL + 'A')
            time.sleep(1.5)
            procedencia_input.send_keys(item['peca']['procedencia'])
            # digitar_como_humano(procedencia_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
            time.sleep(1.5)

        except:
            status = 'Erro no input de info fiscais'
            registrar_status(item['peca']['codigo'], status)
            return status

        #Clicar na tabela de etapas e composição de recursos
        WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA"]'))).click()
        time.sleep(4)

        #Mudar visualização de etapas
        actions = ActionChains(nav)
        changeViewButton = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//div[@id="changeViewButton"]')))
        time.sleep(2)
        actions.move_to_element(changeViewButton).click().perform()
        time.sleep(2)

        #Clica em adicionar etapa
        btnAdd = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//div[@id="insertButton"]')))
        actions.move_to_element(btnAdd).click().perform()
        time.sleep(2)

        for etapa in item['etapas']:

            try:
                checkboxAponta = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="checkbox" and @name="APONTA"]')))
                actions.move_to_element(checkboxAponta).click().perform()
                time.sleep(2)

                checkboxAponta = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="checkbox" and @name="APONTA"]')))
                if not checkboxAponta.is_selected():
                    actions.move_to_element(checkboxAponta).click().perform()
                
                # Preenche o campo "Ordem"
                ordem_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//input[@name="ORDEM"]')))
                ordem_input.send_keys(Keys.CONTROL + 'A')
                time.sleep(1.5)
                ordem_input.send_keys(str(etapa['ordem']))
                # digitar_como_humano(ordem_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
                time.sleep(1.5)

                # Preenche o campo "Processo"
                processo_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//input[@name="PROCESSO"]')))
                processo_input.send_keys(Keys.CONTROL + 'A')
                time.sleep(1.5)
                processo_input.send_keys(etapa['processo'])
                time.sleep(1.5)
                processo_input.send_keys(Keys.TAB)
                # digitar_como_humano(processo_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
                time.sleep(1.5)

                # Preenche o campo "Descrição"
                descricao_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//textarea[@name="DESCRICAO"]')))
                descricao_input.send_keys(Keys.CONTROL + 'A')
                time.sleep(1.5)
                descricao_input.send_keys(etapa['descricao'])
                # digitar_como_humano(descricao_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
                time.sleep(1.5)

                # Preenche o campo "Destino"
                destino_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//input[@name="DEPOSITO"]')))
                destino_input.send_keys(Keys.CONTROL + 'A')
                time.sleep(1.5)
                destino_input.send_keys(etapa['destino'])
                # digitar_como_humano(destino_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
                time.sleep(1.5)

                # Preenche o campo "Desvio"
                desvio_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//input[@name="DEPOSITODE"]')))
                desvio_input.send_keys(Keys.CONTROL + 'A')
                time.sleep(1.5)
                desvio_input.send_keys(etapa['desvio'])
                # digitar_como_humano(desvio_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
                time.sleep(1.5)

                # Clica no botão "Inserir" ou "Finalizar"
                if etapa != item['etapas'][-1]:  # Se não for a última etapa
                    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//*[@id="postButton"]'))).click()
                    carregamento(nav)
                    time.sleep(1.5)
                    btnConfirmar = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//*[@id="postButton"]')))
                    time.sleep(2)
                    actions.move_to_element(btnConfirmar).click().perform()
                    carregamento(nav)
                    # actions.key_down(Keys.CONTROL).send_keys('m').key_up(Keys.CONTROL).perform()
                    time.sleep(2)
                    actions.move_to_element(btnAdd).click().perform()
                    carregamento(nav)
                    time.sleep(8)
                else:  # Última etapa, finaliza
                    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//*[@id="postButton"]'))).click()
                    carregamento(nav)
                    time.sleep(1.5)
                    btnConfirmar = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//*[@id="postButton"]')))
                    time.sleep(2)
                    actions.move_to_element(btnConfirmar).click().perform()
                    carregamento(nav)
                    # actions.key_down(Keys.CONTROL).send_keys('m').key_up(Keys.CONTROL).perform()
                    time.sleep(3)

            except Exception as e:
                print(f"Erro ao preencher a etapa {etapa['ordem']}: {e}")
                status = 'Erro no preenchimento de etapas'
                registrar_status(item['peca']['codigo'], status)
                return status  

        time.sleep(2)

        # Recursos
        # Clique na tabela de recursos
        WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]'))).click()
        time.sleep(2)

        #Mudar visualização de recursos
        actions = ActionChains(nav)
        changeViewButton = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//div[@id="changeViewButton"]')))
        time.sleep(2)
        actions.move_to_element(changeViewButton).click().perform()
        time.sleep(2)

        #Clica em adicionar recursos
        btnAdd = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//div[@id="insertButton"]')))
        actions.move_to_element(btnAdd).click().perform()
        time.sleep(2)
        actions.move_to_element(btnAdd).click().perform()
        
        for recurso in item['recursos']:

            try:

                # Preenche o campo "Ordem"
                ordem_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//input[@name="ORDEM"]')))    
                ordem_input.send_keys(Keys.CONTROL + 'A')
                time.sleep(1.5)
                ordem_input.send_keys(str(recurso['ordem']))
                # digitar_como_humano(ordem_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
                time.sleep(1.5)

                # Preenche o campo "Recurso"
                recurso_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//input[@name="RECURSO"]')))    
                recurso_input.send_keys(Keys.CONTROL + 'A')
                time.sleep(1.5)
                recurso_input.send_keys(recurso['recurso'])
                # digitar_como_humano(recurso_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
                time.sleep(10)

                # Preenche o campo "Quantidade"
                quantidade_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//input[@name="QUANTIDADE"]')))    
                quantidade_input.send_keys(Keys.CONTROL + 'A')
                time.sleep(1.5)
                quantidade_input.send_keys(recurso['quantidade'])
                # digitar_como_humano(quantidade_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
                time.sleep(1.5)

                # Preenche o campo "Depósito origem"
                destino_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((
                    By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//input[@name="DEPOSITO"]')))    
                destino_input.send_keys(Keys.CONTROL + 'A')
                time.sleep(1.5)
                destino_input.send_keys(recurso['dep_origem'])
                # digitar_como_humano(destino_input, descricao_texto, intervalo=0.2)  # Intervalo de 200ms entre as letras
                time.sleep(1.5)

                # Clica no botão "Inserir" ou "Finalizar"
                if recurso != item['recursos'][-1]:  # Se não for a última etapa
                    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//*[@id="postButton"]'))).click()
                    carregamento(nav)
                    time.sleep(1.5)
                    btnConfirmar = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//*[@id="postButton"]')))
                    time.sleep(2)
                    actions.move_to_element(btnConfirmar).click().perform()
                    carregamento(nav)
                    # actions.key_down(Keys.CONTROL).send_keys('m').key_up(Keys.CONTROL).perform()
                    time.sleep(2)
                    actions.move_to_element(btnAdd).click().perform()
                    carregamento(nav)
                    time.sleep(8)
                else:  # Última etapa, finaliza
                    WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//*[@id="postButton"]'))).click()
                    carregamento(nav)
                    time.sleep(1.5)
                    btnConfirmar = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//*[@id="postButton"]')))
                    time.sleep(2)
                    actions.move_to_element(btnConfirmar).click().perform()
                    carregamento(nav)
                    # actions.key_down(Keys.CONTROL).send_keys('m').key_up(Keys.CONTROL).perform()
                    time.sleep(3)

            except Exception as e:
                print(f"Erro ao preencher recurso: {e}")
                status = 'Erro no preenchimento de recursos'
                registrar_status(item['peca']['codigo'], status)
                return status   

        # Clique na tabela de propriedades
        WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]'))).click()
        time.sleep(2)

        #Mudar visualização de propriedades
        changeViewButton = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//div[@id="changeViewButton"]')))
        time.sleep(2)
        actions.move_to_element(changeViewButton).click().perform()
        time.sleep(2)

        #Clica em adicionar etapa
        btnAdd = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//div[@id="insertButton"]')))
        time.sleep(2)
        actions.move_to_element(btnAdd).click().perform()
        time.sleep(2)

        #Propriedades

        if item['propriedades']:
            for propriedade in item['propriedades']:
                try:
                    propriedade_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//input[@name="CAMPOINTEIRO"]')))
                    propriedade_input.send_keys(propriedade['propriedade'])
                    time.sleep(2)

                    valor_input = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//input[@name="VALOR"]')))
                    time.sleep(2)
                    valor_input.click()
                    time.sleep(2)
                    valor_input.send_keys(propriedade['valor'])
                    time.sleep(2)
                    valor_input.send_keys(Keys.TAB)
                    time.sleep(2)

                    # Clica no botão "Inserir" ou "Finalizar"
                    if propriedade != item['propriedades'][-1]:  # Se não for a última etapa
                        WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//*[@id="postButton"]'))).click()
                        carregamento(nav)
                        time.sleep(1.5)
                        btnConfirmar = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//*[@id="postButton"]')))
                        time.sleep(2)
                        actions.move_to_element(btnConfirmar).click().perform()
                        carregamento(nav)
                        # actions.key_down(Keys.CONTROL).send_keys('m').key_up(Keys.CONTROL).perform()
                        time.sleep(2)
                        actions.move_to_element(btnAdd).click().perform()
                        carregamento(nav)
                        time.sleep(8)
                    else:  # Última etapa, finaliza
                        WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//*[@id="postButton"]'))).click()
                        carregamento(nav)
                        time.sleep(1.5)
                        btnConfirmar = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//*[@id="postButton"]')))
                        time.sleep(2)
                        actions.move_to_element(btnConfirmar).click().perform()
                        carregamento(nav)
                        # actions.key_down(Keys.CONTROL).send_keys('m').key_up(Keys.CONTROL).perform()
                        time.sleep(3)
                except Exception as e:
                    print(f"Erro ao preencher a propriedade: {e}")
                    status = 'Erro no preenchimento de propriedades'
                    registrar_status(item['peca']['codigo'], status)
                    return status

        else:
            time.sleep(2)
            #Mudar visualização de propriedades
            changeViewButton = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//div[@id="changeViewButton"]')))
            time.sleep(2)
            actions.move_to_element(changeViewButton).click().perform()
            time.sleep(2)

        time.sleep(5)

        registrar_status(item['peca']['codigo'], status)

        #Mudar visualização de propriedades
        changeViewButton = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS_PROPRIEDADES"]//div[@id="changeViewButton"]')))
        time.sleep(2)
        actions.move_to_element(changeViewButton).click().perform()
        time.sleep(2)

        #Mudar visualização de recursos
        changeViewButton = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA_ETAPARECURSOS"]//div[@id="changeViewButton"]')))
        time.sleep(2)
        actions.move_to_element(changeViewButton).click().perform()
        time.sleep(4)

        #Mudar visualização de etapas
        changeViewButton = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer_RECURSOETAPA"]//div[@id="changeViewButton"]')))
        time.sleep(2)
        actions.move_to_element(changeViewButton).click().perform()
        time.sleep(2)

        recomecar(nav)

    return status

def recomecar(nav):

    nav.switch_to.default_content()
    iframes(nav)

    # Clicar em adicionar novo item
    try:
        WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="explorer"]//div[@id="insertButton"]'))).click()
        time.sleep(1.5)
    except:
        status = 'Erro ao clicar na lupa'

def buscando_dados_peca():

    # Faz a requisição GET
    response = requests.get("http://192.168.3.140:8081/gerar-json/pecas")

    # Verifica o status da resposta
    if response.status_code == 200:
        # Converte os dados para JSON
        dados = response.json()
    else:
        print(f"Erro na requisição. Código de status: {response.status_code}")

    return dados

def buscando_dados_conjuntos():

    # Faz a requisição GET
    response = requests.get("http://192.168.3.140:8081/gerar-json/conjuntos")

    # Verifica o status da resposta
    if response.status_code == 200:
        # Converte os dados para JSON
        dados = response.json()
    else:
        print(f"Erro na requisição. Código de status: {response.status_code}")

    return dados

def registrar_status(codigo,status):

    url = "http://192.168.3.140:8081/registrar-status/"
    
    # Dados a serem enviados
    payload = {
        "codigo": codigo,
        "status": status
    }

    # Envia a requisição POST
    response = requests.post(url, json=payload)

    # Verifica a resposta
    if response.status_code == 200:
        print("Resposta:", response.json())  # Resposta JSON
    else:
        print(f"Erro {response.status_code}: {response.text}")

def clicar_ate_classe(nav, xpath, classe_esperada, max_tentativas=5, intervalo=2):
    tentativas = 0
    actions = ActionChains(nav)
    while tentativas < max_tentativas:
        try:
            # Localizar o botão
            btn = WebDriverWait(nav, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
            
            # Capturar a classe do botão
            classe_atual = btn.get_attribute('class')
            print(f"Tentativa {tentativas + 1}: Classe atual - {classe_atual}")
            
            # Verificar se a classe esperada apareceu
            if classe_esperada in classe_atual:
                print("Classe esperada detectada!")
                return True  # Sai do loop
            
            # Tentar clicar no botão
            actions.move_to_element(btn).click().perform()
            print("Botão clicado.")

            carregamento(nav)
            
            # Aguarda antes de tentar novamente
            time.sleep(intervalo)
            tentativas += 1
        except TimeoutException:
            print("Elemento não encontrado. Tentando novamente...")
            time.sleep(intervalo)
            tentativas += 1
    
    print("Falha ao encontrar a classe esperada.")
    return False

while True:

    dados_peca = buscando_dados_peca()
    # dados_conjuntos = buscando_dados_conjuntos()

    if len(dados_peca)>0:

        chrome_driver_path = verificar_chrome_driver()
        nav = webdriver.Chrome(chrome_driver_path)
        nav.maximize_window()
        nav.get("https://hcemag.innovaro.com.br/sistema/")

        login(nav)

        for dados in dados_peca['pecas']:
            
            # dados = dados_peca['pecas'][0]

            menu_cadastro(nav)

            iframes(nav)

            add_novo_item(nav)

            mudar_visualizacao(nav, '//*[@id="explorer"]//div[@id="changeViewButton"]', '//*[@id="explorer"]//input[@name="CODIGO"]','field formView editingRecord focus control-input')

            status = preencher_cadastro_peca(nav, dados)

        print("acabou")

    # if len(dados_conjuntos)>0:

    #     chrome_driver_path = verificar_chrome_driver()
    #     nav = webdriver.Chrome(chrome_driver_path)
    #     nav.maximize_window()
    #     nav.get("https://hcemag.innovaro.com.br/sistema/")

    #     login(nav)

    #     menu_cadastro(nav)

    #     iframes(nav)

    #     localizar(nav)

    #     status = preencher_cadastro_peca(nav, dados_peca)
