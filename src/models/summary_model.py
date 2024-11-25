from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict
from src.config import GROQ_API_KEY
import json

exmaple_json=json.load('assets\example.json')

class SummaryJSON(BaseModel):
    keywords: Dict[str, List[str]] = Field({}, description="Keywords for location, lighting, and tone")
    elaborative_descriptions: Dict[str, str] = Field({}, description="Detailed descriptions for each location")
    scene_improvement_tips: Dict[str, str] = Field({}, description="Improvement tips for lighting, tone, composition, and color palette")

llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    verbose=True,
)

def get_summary_json(prompt):
    try:
        structured_llm = llm.with_structured_output(SummaryJSON, method="json_mode")
        system_prompt = """
                            Extract keywords from the script related to the following aspects: location, lighting, and tone of the scene.
                            Organize the output in JSON format with:

                            Keywords for each aspect, such as location, lighting, and tone.
                            Note that you have to provide all the different location mentioned in the script and they should be in the lines of room or courtyard or garden or hallway.
                            Elaborative descriptions of each location mentioned, drawing inspiration from Rajasthan/Mughal palaces only, while providing rich historical and cultural context in under 50 words.
                            Improvement tips for enhancing the lighting and tone. The tips should emphasize capturing the grandeur, warmth, and authenticity of Rajasthan/Mughal historical settings only.
                            Ensure that each section—keywords, location descriptions, and improvement tips—appears as a separate key-value pair in the JSON structure.

                            json_structure: {example_json}
        """
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_prompt), ("human", "{input}")]
        )
        few_shot_structured_llm = prompt_template | structured_llm
        data = few_shot_structured_llm.invoke({"input": prompt})
        return data.dict()
    except Exception as e:
        print(f"Error in get_summary_json: {e}")
        return None
