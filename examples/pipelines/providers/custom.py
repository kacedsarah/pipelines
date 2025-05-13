"""
title: Claude 3 - 5G Billing Assistant
author: you
date: 2025-05-13
version: 1.0
license: MIT
description: A Claude-based assistant for 5G billing inquiries using the Anthropic API.
requirements: requests
environment_variables: ANTHROPIC_API_KEY
"""

import os
import requests
import logging
from typing import List, Union, Dict, Optional, Generator, Iterator
from pydantic import BaseModel
from utils.pipelines.main import pop_system_message


class Pipeline:
    class Valves(BaseModel):
        ANTHROPIC_API_KEY: Optional[str] = None

    def __init__(self):
        self.type = "manifold"
        self.name = "Claude 5G Billing Assistant"
        self.valves = self.Valves(
            ANTHROPIC_API_KEY=os.getenv("ANTHROPIC_API_KEY", "")
        )
        self.model_id = "claude-3-sonnet-20240229"  # or claude-3-opus-20240229

        self.pipelines = self.get_models()

        self.system_prompt = (
            "You are a professional customer service assistant for a 5G mobile network provider. "
            "Your role is to assist customers with billing-related inquiries such as data charges, "
            "overage fees, duplicate payments, plan upgrades, and billing cycles.\n\n"
            "Begin the conversation by introducing yourself and politely asking what billing issue the customer needs help with.\n\n"
            "From that point on:\n"
            "- ONLY respond to what the customer says.\n"
            "- NEVER simulate or guess customer inputs.\n"
            "- DO NOT carry both sides of the conversation.\n"
            "- Use a clear, empathetic tone and professional language.\n"
            "- Ask for clarification only when necessary.\n"
            "- Offer solutions, explanations, or escalation steps for billing issues.\n"
            "- Do not end the conversation unless the customer confirms the issue is resolved.\n\n"
            "Stay strictly in the assistant role and stick to 5G billing-related concerns."
        )

    def get_models(self):
        return [{
            "id": "claude-5g-billing-assistant",
            "name": "Claude 5G Billing Assistant",
        }]

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Dict[str, Union[str, list]]]:

        api_key = self.valves.ANTHROPIC_API_KEY
        if not api_key:
            return {"error": "Missing ANTHROPIC_API_KEY"}

        # Remove irrelevant keys
        for key in ['user', 'chat_id', 'title']:
            body.pop(key, None)

        # Inject system message
        system_message, messages = pop_system_message(messages)
        system_message_content = self.system_prompt

        claude_messages = [{"role": "user", "content": system_message_content}]
        claude_messages += messages

        payload = {
            "model": self.model_id,
            "max_tokens": body.get("max_tokens", 1024),
            "temperature": body.get("temperature", 0.7),
            "top_p": body.get("top_p", 0.9),
            "messages": claude_messages,
            "system": system_message_content,
            "stream": False,
        }

        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            reply = result['content'][0]['text']

            return {
                "id": "chatcmpl-claude-5g-001",
                "object": "chat.completion",
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": reply
                    }
                }],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 10,
                    "total_tokens": 20
                }
            }

        except Exception as e:
            logging.exception("Error calling Claude API")
            return {"error": str(e)}
