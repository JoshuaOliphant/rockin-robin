from transformers import GPT2Tokenizer
from crewai_tools import BaseTool


class TruncatePrompt(BaseTool):
    name: str = "TruncatePrompt"
    description: str = (
        "Truncates a prompt to be less than the max_tokens for LLM prompts"
    )

    def _run(self, prompt, max_tokens=8192):
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        tokens = tokenizer.encode(prompt)
        if len(tokens) > max_tokens:
            truncated_tokens = tokens[:max_tokens]
            truncated_prompt = tokenizer.decode(truncated_tokens)
            return truncated_prompt
        return prompt
