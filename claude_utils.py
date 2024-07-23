from anthropic import AI_PROMPT, HUMAN_PROMPT, AsyncAnthropic

from config import claude_api


class Claude:
    system_prompts = {
        "default": "You are Claude, an AI assistant.",
        "coder": "You are Claude, an AI assistant specialized in coding. Provide code examples and explanations.",
        "writer": "You are Claude, an AI assistant specialized in creative writing. Help with story ideas, plot development, and prose."    }

    def __init__(self):
        self.model = "claude-3-5-sonnet-20240620"
        self.temperature = 0.8
        self.cutoff = 2000
        self.client = AsyncAnthropic(api_key=claude_api)
        self.prompt = ""
        self.system_prompt = self.system_prompts["default"]

    def reset(self):
        self.prompt = ""

    def revert(self):
        self.prompt = self.prompt[: self.prompt.rfind(HUMAN_PROMPT)]

    def change_model(self, model):
        valid_models = {"claude-2", "claude-instant-1", "claude-3-5-sonnet-20240620"}
        if model in valid_models:
            self.model = model
            return True
        return False

    def change_temperature(self, temperature):
        try:
            temperature = float(temperature)
        except ValueError:
            return False
        if 0 <= temperature <= 1:
            self.temperature = temperature
            return True
        return False

    def change_cutoff(self, cutoff):
        try:
            cutoff = int(cutoff)
        except ValueError:
            return False
        if cutoff > 0:
            self.cutoff = cutoff
            return True
        return False
      
    def change_system_prompt(self, task):
        if task in self.system_prompts:
            self.system_prompt = self.system_prompts[task]
            return True
        return False
    
    def get_available_tasks(self):
        return list(self.system_prompts.keys())

    async def send_message(self, message):
        messages = [
            {"role": "user", "content": message},
        ]

        response = await self.client.messages.create(
            model=self.model,
            messages=messages,
            system=self.system_prompt,
            temperature=self.temperature,
            max_tokens=2000,
        )

        content = response.content
        if isinstance(content, list) and content:
            return content[0].text
        else:
            return ""
