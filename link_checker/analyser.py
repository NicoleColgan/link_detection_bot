import logging
from link_checker.constants import VALIDITY_PROMPT
from langchain_community.chat_models import ChatOpenAI
from typing import List, Dict
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)

class LLMAnalyser:  # make it a class cause it needs to hold state. Every call to his class depends on the same llm instance and prompt set up. Also makes it easy to pass in different llms
    def __init__(self, llm=None):
        # Allow injection & default to ChatOpenAI
        self.llm = llm or ChatOpenAI(temperature=0.0)   # low temperate for deterministic output

    def detect_signals(self, response_info: dict) -> List[str]:
        """Check if theres any red flag keywords to indicate an issue with the page (custom error page)"""
        signals = []
        text = (response_info.get("content_snippet") or "").lower()

        if not text:    #if text is any falsy value like "", None, 0
            signals.append("empty response")
        for token in ("coming soon", "not found", "404", "error", "forbidden"): #use tuple since its never changed to avoid error
            if token in text:
                signals.append(token)
        
        return signals
    
    def _build_response_schema(self):   # "_" means its meant for iternal use (called within this class but not by anything that imports it)
        """Use LangChain parser to extract json"""
        usable = ResponseSchema(name="usable", description="True/False/Unknown")
        reason = ResponseSchema(name="reason", description="Why usable or not")
        steps = ResponseSchema(name="resolution_steps", description="How to fix or N/A")
        
        return [usable, reason, steps]
    
    def check_link_validity(self, response_info: dict) -> Dict[str, str]:   #Dict allows you to specify the dict key and value type
        #Use structuredOutputParser + prompt
        schemas = self._build_response_schema()
        parser = StructuredOutputParser(response_schemas=schemas)
        format_instructions = parser.get_format_instructions()
        response_info["format_instructions"] = format_instructions
        signals = self.detect_signals(response_info)

        prompt_template = ChatPromptTemplate.from_template(VALIDITY_PROMPT)
        messages = prompt_template.format_messages(
            original_url = response_info.get("original_url"),
            response_url = response_info.get("response_url"),
            status_code = response_info.get("status_code"),
            ok = response_info.get("ok"),
            is_redirect = response_info.get("is_redirect"),
            redirect_chain = response_info.get("redirect_chain"),
            reason = response_info.get("reason"),
            cookies = response_info.get("cookies"),
            elapsed = response_info.get("elapsed"),
            request_method = response_info.get("request_method"),
            content_snippet = response_info.get("content_snippet"),
            signals = signals,
            format_instructions = format_instructions
        )
        llm_response = self.llm(messages)

        try:
            parsed = parser.parse(llm_response.content)
            return {
                "usable": parsed.get("usable"),
                "reason": parsed.get("reason"),
                "resolution_steps": parsed.get("resolution_steps")
            }
        except Exception as exc:
            logger.exception("LLM parsing error: %s", exc)
            return {
                "usable": "Unknown",
                "reason": "LLM parse error",
                "resolution_steps": "N/A"
            }

