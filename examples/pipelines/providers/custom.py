from openai_pipelines.providers.base import BaseProvider

class CustomNetOpsModel(BaseProvider):
    def __init__(self):
        super().__init__(
            model_id="custom-netops-v1",
            provider_id="local_netops",
            api_key="LabLabee"
        )

    def get_prompt_template(self):
        return {
            "system": "You are a VyOS automation expert. Provide concise CLI configuration help.",
            "user": "{input}"
        }

    def generate(self, prompt, **kwargs):
        return {
            "id": "chatcmpl-netops-001",
            "object": "chat.completion",
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": f"Here's a sample CLI configuration for: {prompt}"
                }
            }],
            "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20}
        }
