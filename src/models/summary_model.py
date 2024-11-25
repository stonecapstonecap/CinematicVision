from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict
from src.config import GROQ_API_KEY

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
        Extract keywords from the script related to location, lighting, and tone, 
        and provide descriptions inspired by Rajasthan/Mughal palaces.
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
