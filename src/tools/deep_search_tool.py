import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from bs4 import BeautifulSoup
from requests import get
from urllib.parse import unquote
from googlesearch.user_agents import get_useragent
from googlesearch import search



class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"

class GenericTextScraper:
    def __init__(self, url):
        self.url = url
        self.setup_driver()

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(10)
        self.wait = WebDriverWait(self.driver, 20)

    def acessar_pagina(self):
        try:
            self.driver.get(self.url)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2)
            return True
        except TimeoutException:
            return False

    def capturar_texto(self):
        try:
            body = self.driver.find_element(By.TAG_NAME, "body")
            return body.text
        except Exception as e:
            print(e)
            return ""

    def extrair_texto(self):
        try:
            if not self.acessar_pagina():
                raise Exception("Falha ao acessar página")
            texto = self.capturar_texto()
            if not texto:
                raise Exception("Nenhum texto encontrado")
            return texto
        except Exception as e:
            print(e)
            return ""
        finally:
            self.driver.quit()


class DeepSearchTool:


    def _req(term, results, lang, start, proxies, timeout, safe, ssl_verify, region):
        resp = get(
            url="https://www.google.com/search",
            headers={
                "User-Agent": get_useragent(),
                "Accept": "*/*"
            },
            params={
                "q": term,
                "num": results + 2,  # Prevents multiple requests
                "hl": lang,
                "start": start,
                "safe": safe,
                "gl": region,
            },
            proxies=proxies,
            timeout=timeout,
            verify=ssl_verify,
            cookies = {
                'CONSENT': 'PENDING+987',
                'SOCS': 'CAESHAgBEhIaAB',
            }
        )
        resp.raise_for_status()
        return resp


    @staticmethod
    def api_deep_search(questions: list[str]) -> str:
        """
        Realiza uma busca profunda na web com base em uma pergunta fornecida.

        Esta função utiliza a ferramenta DeepSearchTool para buscar URLs relevantes
        e extrair texto a partir dessas URLs. O resultado é uma string que contémß
        o texto combinado de todas as URLs encontradas.

        Parâmetros:
        ----------
        questions : list[str]
            lista de perguntas ou termos de busca que serão utilizados para encontrar informações.

        Retorna:
        -------
        str
            Uma string contendo o texto extraído das URLs encontradas.
        """
        urls = []
        for question in questions:
            urls.extend(list(search(question, num_results=1, lang="pt-br")))

        urls = list(filter(lambda x: x.strip(), urls))

        texts = []
        for url in urls:
            scraper = GenericTextScraper(url)
            texts.append(scraper.extrair_texto())
        unique_text = "\n".join(texts)

        return unique_text