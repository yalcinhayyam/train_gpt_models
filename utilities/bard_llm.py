from bardapi import Bard
from typing import Any, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
import os

class BardLLM(LLM):
    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None,run_manager: Optional[CallbackManagerForLLMRun] = None) -> str:
        response = Bard(token=os.getenv('BARD_API_TOKEN')).get_answer(prompt)['content']
        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {}
