import os
from google.adk.tools import load_memory
from fastapi.responses import StreamingResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types
from src.agents.deep_search.deep_search_agent import DeepSearchAgent
from dotenv import load_dotenv


load_dotenv()

class ChatService:

    @classmethod
    def executar(cls, nome: str, telefone: str):
        async def stream_response():
            try:
                app_name = "MySideApp"
                user_id = "72eadd5b-676c-413e-b48e-cc0c00310c99"
                session_id = "8c13921e-a5f4-4178-93bb-411e85a41c80"
                agent_description = ("Como Investigador Digital, sua principal responsabilidade é auxiliar o Personal Shopper Imobiliário na realização de investigações aprofundadas sobre perfis de interesse, utilizando informações como nome e telefone. "
                                     "Seu papel é buscar, analisar e validar dados relevantes em fontes digitais, sempre respeitando a legislação vigente e as melhores práticas de privacidade. " 
                                     "Você deve identificar possíveis riscos, oportunidades e informações complementares que possam impactar a negociação ou a tomada de decisão do cliente. " 
                                     "Seu trabalho é fornecer relatórios claros, objetivos e imparciais, garantindo que o Personal Shopper Imobiliário tenha uma visão completa e segura sobre o perfil investigado, "
                                     "contribuindo para uma experiência de compra ou locação de imóveis mais transparente, assertiva e protegida para o cliente")
                agent_instruction = agent_instruction = ("<prompt>"
                                                            "<priority_instructions>"
                                                            "<instructions>"
                                                            "<instructions>"
                                                            "<instruction>"
                                                            "Ao receber um nome e telefone para investigação, acione o DeepSearchAgent para realizar buscas aprofundadas na web."
                                                            "</instruction>"
                                                            "<instruction>"
                                                            "Forneça ao DeepSearchAgent instruções claras sobre os formatos de busca a serem utilizados, combinando nome e telefone em diferentes variações."
                                                            "</instruction>"
                                                            "<instruction>"
                                                            "Analise criticamente os resultados retornados pelo DeepSearchAgent, verificando a credibilidade das fontes e a relevância das informações para o contexto imobiliário."
                                                            "</instruction>"
                                                            "<instruction>"
                                                            "Identifique e destaque no relatório quaisquer sinais de alerta como: histórico de inadimplência, processos judiciais, protestos, dívidas ativas ou fraudes anteriores."
                                                            "</instruction>"
                                                            "<instruction>"
                                                            "Verifique a consistência das informações encontradas, buscando validar dados importantes em múltiplas fontes independentes."
                                                            "</instruction>"
                                                            "<instruction>"
                                                            "Organize as informações coletadas em categorias relevantes: perfil financeiro, histórico judicial, presença digital, vínculos empresariais e patrimônio declarado."
                                                            "</instruction>"
                                                            "<instruction>"
                                                            "Elabore um relatório objetivo e imparcial, destacando claramente os fatos encontrados e separando-os de suposições ou informações não confirmadas."
                                                            "</instruction>"
                                                            "<instruction>"
                                                            "Inclua no relatório uma seção de \"Considerações para Negociação\" com pontos específicos que o Personal Shopper Imobiliário deve atentar durante as tratativas."
                                                            "</instruction>"
                                                            "<instruction>"
                                                            "Mantenha registro detalhado de todas as fontes consultadas, queries utilizadas e métodos de validação empregados para garantir a rastreabilidade das informações."
                                                            "</instruction>"
                                                            "<instruction>"
                                                            "Respeite rigorosamente a legislação de proteção de dados, evitando coletar ou reportar informações sensíveis não pertinentes ao contexto da negociação imobiliária."
                                                            "</instruction>"
                                                            "</instructions>"
                                                            "</instructions>"
                                                            "</priority_instructions>"
                                                            "<tools>"
                                                            "<tool name='load_memory'><description></description></tool>"
                                                            "</tools>"
                                                            "<sub_agents>"
                                                            "<sub_agent name='DeepSearchAgent'><description>Agente de busca profunda na web</description></sub_agent>"
                                                            "</sub_agents>"
                                                            "</prompt>")

                session_service = InMemorySessionService()
                memory_service = InMemoryMemoryService()
                artifact_service = InMemoryArtifactService()

                session = session_service.create_session(
                    app_name=app_name,
                    user_id=user_id,
                    session_id=session_id,
                )

                deep_search_agent = DeepSearchAgent().get_deep_search_agent()

                root_agent = Agent(
                    name="RootAgent",
                    model=LiteLlm(model=os.environ.get("OPENAI_MODEL")),
                    description=agent_description,
                    instruction=agent_instruction,
                    tools=[load_memory],
                    sub_agents=[deep_search_agent],
                    generate_content_config={
                        "temperature": 0.7,
                        "top_p": 0.7,
                        "top_k": 50,
                    }
                )

                runner = Runner(
                    agent=root_agent,
                    app_name="MySideApp",
                    session_service=session_service,
                    memory_service=memory_service,
                    artifact_service=artifact_service
                )

                full_response_text = ""

                async for event in runner.run_async(user_id=user_id,
                                                    session_id=session_id,
                                                    new_message=types.Content(role='user', parts=[types.Part(text=f"Nome: {nome} - Telefone: {telefone}")])):

                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            text = getattr(part, "text", None)
                            if text:
                                if event.is_final_response():
                                    final_response_text = full_response_text + text
                                    yield final_response_text.strip()
                                    break

            except Exception as e:
                print(str(e))
                yield {"Erro": str(e)}

        return StreamingResponse(stream_response(), media_type="text/event-stream")
