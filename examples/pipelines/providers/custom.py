"""
title: Custom Billing Assistant
author: you
date: 2025-05-13
version: 1.0
license: MIT
description: A custom assistant focused on 5G billing support.
"""

import logging
from typing import List, Union, Generator, Iterator, Dict, Optional, Any
from pydantic import BaseModel
from utils.pipelines.main import pop_system_message


class Pipeline:
    class Valves(BaseModel):
        pass

    def __init__(self):
        self.type = "manifold"
        self.name = "Billing Assistant"
        self.valves = self.Valves()
        self.pipelines = self.get_models()

        # System prompt for this assistant
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

    async def on_startup(self):
        pass

    async def on_shutdown(self):
        pass

    async def on_valves_updated(self):
        pass

    def get_models(self):
        return [
            {
                "id": "custom-billing-assistant-v1",
                "name": "5G Billing Assistant",
            },
        ]

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        try:
            system_message, messages = pop_system_message(messages)

            # Use the fixed system prompt regardless of input
            introduction = (
                "Hello! I'm your 5G mobile billing assistant. How can I assist you with your billing concerns today?"
            )

            # If it's the start of the conversation, respond with the intro
            if not messages or (len(messages) == 1 and messages[0]["role"] == "user"):
                return {
                    "id": "chatcmpl-billing-001",
                    "object": "chat.completion",
                    "choices": [{
                        "message": {
                            "role": "assistant",
                            "content": introduction
                        }
                    }],
                    "usage": {
                        "prompt_tokens": 10,
                        "completion_tokens": 10,
                        "total_tokens": 20
                    }
                }

            # Otherwise, simulate a billing assistant response (mock logic)
            last_user_msg = messages[-1]["content"]
            response = f"I understand. Let me check on the issue regarding: \"{last_user_msg}\". Could you please confirm your billing account number?"

            return {
                "id": "chatcmpl-billing-002",
                "object": "chat.completion",
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": response
                    }
                }],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 10,
                    "total_tokens": 20
                }
            }

        except Exception as e:
            return f"Error: {e}"
