import os
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from src.tools.deep_search_tool import DeepSearchTool
import xml.etree.ElementTree as ET

class DeepSearchAgent:

    def get_deep_search_agent(self):
        behavior = ""

        tree = ET.parse("./src/agents/deep_search/deep_search_prompt.xml")
        root = tree.getroot()
        behavior = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')

        deep_search_agent = Agent(
            name="DeepSearchAgent",
            model=LiteLlm(model=os.environ.get("OPENAI_MODEL")),
            description="Agent specialized in digital investigations, capable of building and executing advanced searches using Google Dorks techniques to locate relevant information about individuals and companies, including data from social networks, public records, lawsuits, debts, business associations, and digital presence, documenting all queries and results for detailed reports.",
            instruction=behavior,
            tools=[DeepSearchTool.api_deep_search],
            sub_agents=[],
            generate_content_config={
                "temperature": 0.7,
                "top_p": 0.7,
                "top_k": 50,
            }
        )

        return deep_search_agent
