import json
import logging
from typing import Any, List, Optional
from dotenv import load_dotenv
import os

load_dotenv()

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult
from langchain_openai import ChatOpenAI
from pydantic import Field

logger = logging.getLogger(__name__)

class ChatLMStudio(ChatOpenAI):
    """Chat model pointed at your local LM Studio instance."""

    format: Optional[str] = Field(default=None, description="Whether to parse JSON from the response")

    def __init__(
        self,
        model: str = "llama-3.2-3b-instruct",
        temperature: float = 0.7,
        format: Optional[str] = None,
        streaming: bool = False,
        **kwargs: Any,
    ):
        # Load LM Studio host from OPENAI_API_BASE (e.g. http://10.45.14.174:1234)
        api_base = os.getenv("OPENAI_API_BASE", "http://10.45.14.174:1234")
        # LM Studio doesn’t require a real API key
        api_key = os.getenv("OPENAI_API_KEY", "not-needed")

        super().__init__(
            model=model,
            temperature=temperature,
            base_url=f"{api_base}/v1",   # <— this is the critical line
            openai_api_key=api_key,
            streaming=streaming,
            **kwargs,
        )
        self.format = format

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        logger.debug(
            "Calling LMStudio at %s; streaming=%s format=%s",
            getattr(self, "openai_api_base", "unknown"),
            getattr(self, "streaming", False),
            self.format,
        )

        result = super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)

        # Optional JSON-snippet logic
        if self.format == "json" and result.generations:
            raw = result.generations[0][0].text
            start, end = raw.find("{"), raw.rfind("}") + 1
            if start != -1 and end > start:
                snippet = raw[start:end]
                try:
                    json.loads(snippet)
                    result.generations[0][0].text = snippet
                except json.JSONDecodeError:
                    logger.warning("Could not parse JSON snippet; leaving raw text")
        return result

