# MySide

**MySide** é uma API para investigações digitais automatizadas, voltada para auxiliar Personal Shoppers Imobiliários na análise de perfis de interesse, utilizando nome e telefone como ponto de partida. O sistema realiza buscas profundas na web, valida informações e gera relatórios detalhados, respeitando a legislação vigente de privacidade.

## Sumário

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Endpoints Principais](#endpoints-principais)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Licença](#licença)

---

## Visão Geral

A API permite realizar investigações digitais a partir de nome e telefone, utilizando técnicas avançadas de busca (Google Dorks) e extração de dados de páginas web. O objetivo é fornecer ao Personal Shopper Imobiliário informações relevantes, como histórico judicial, presença digital, vínculos empresariais e possíveis riscos, de forma automatizada e rastreável.

---

## Funcionalidades

- Busca profunda na web combinando nome e telefone em múltiplos formatos.
- Utilização de técnicas Google Dorks para refinar resultados.
- Extração de informações de redes sociais, registros públicos, processos judiciais, protestos, dívidas, etc.
- Geração de relatórios objetivos, categorizados e rastreáveis.
- Respeito à LGPD e melhores práticas de privacidade.
- API pronta para deploy com Docker.

---

## Estrutura do Projeto

```
myside/
│
├── main.py                # Ponto de entrada da aplicação
├── Dockerfile             # Build da imagem Docker
├── docker-compose.yml     # Orquestração dos serviços
├── pyproject.toml         # Dependências do projeto
├── src/
│   ├── app.py             # Instância FastAPI e configuração de middlewares/rotas
│   ├── router/
│   │   └── router.py      # Rotas principais da API
│   ├── controller/
│   │   └── chat_controller.py # Endpoint de busca
│   ├── services/
│   │   └── chat_service.py    # Lógica de orquestração dos agentes
│   ├── agents/
│   │   └── deep_search/
│   │       ├── deep_search_agent.py   # Agente de busca profunda
│   │       └── deep_search_prompt.xml # Prompt detalhado do agente
│   └── tools/
│       └── deep_search_tool.py        # Ferramenta de busca e scraping
```

---

## Como Executar

### Requisitos

- Python 3.11+
- Docker e Docker Compose (recomendado)

### Executando com Docker Compose

```bash
docker-compose up --build
```

A API estará disponível em: [http://localhost:8000](http://localhost:8000)

### Executando Localmente

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Exporte as variáveis de ambiente necessárias (veja abaixo).
3. Execute:
   ```bash
   python main.py
   ```

---

## Variáveis de Ambiente

- `OPENAI_MODEL`: Modelo a ser utilizado pelo agente (ex: `gpt-4o`)
- `OPENAI_API_KEY`: Chave de API da OpenAI
- `ENVIRON`, `TIMEZONE`: Outras variáveis para configuração do ambiente

---

## Endpoints Principais

- **GET /**  
  Retorna mensagem de boas-vindas e versão da API.

- **GET /api/v1/myside/buscar/nome/{nome}/telefone/{telefone}**  
  Realiza a busca profunda a partir do nome e telefone informados.  
  **Exemplo:**  
  ```
  GET /api/v1/myside/buscar/nome/Joao%20Silva/telefone/11999999999
  ```

  **Retorno:**  
  Streaming de texto com o relatório gerado.

---

## Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [Google Search Python](https://pypi.org/project/googlesearch-python/)
- [Docker](https://www.docker.com/)
- [OpenAI GPT](https://platform.openai.com/)

---

## Licença

Este projeto está sob a licença MIT.

---

Se desejar, posso adaptar ou expandir este README conforme necessidades específicas do seu projeto!
