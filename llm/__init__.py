import logging
import os, time, requests, openai

logger = logging.getLogger(__name__)


class OpenAIModel:
    def __init__(self, name, base_url, model_name, api_key = "ollama"):
        self.name  = "OpenAI-" + name
        self.model = openai.OpenAI(base_url = base_url, api_key = api_key)
        self.model_name = model_name

    def ask(self, message: str) -> str | None:
        return run_it(self.name, lambda: self.ask_ai(message))

    def ask_ai(self, message: str) -> str:
        response = self.model.chat.completions.create(
            model      = self.model_name,
            messages   = [{"role": "user", "content": message}],
            max_tokens = 1024,
        )
        return response.choices[0].message.content

def open_ai_local() -> OpenAIModel:
    return OpenAIModel("local", "http://localhost:11434/v1/", "qwen2-anzu-iot:7b")


class LocalModel:
    def __init__(self):
        self.name = "local"
        self.url = "http://localhost:11434/api/generate"
        self.headers = {
          "Accept": "application/json",
          "Content-Type": "application/json"
        }

    def ask(self, message: str) -> str | None:
        return run_it(self.name, lambda: self.ask_ai(message))

    def ask_ai(self, message: str) -> str:
        payload = {
                "model": "qwen2:7b",
                "prompt": message,
                "stream": False,
                }
        resp = requests.post(self.url, json=payload, headers=self.headers, timeout=600)
        if resp.status_code != 200:
            raise Exception(resp.text)
        return resp.json()["response"]

took_time = not os.environ.get("no_AI_took_time")

def run_it(name, work_func) -> str | None:
    start_time = time.time()
    try:
        ret = work_func()
    except Exception as e:
        logger.error(f"{name} error:  {e}")
        ret = None
    if took_time:
        seconds = round(time.time() - start_time, 2)
        logger.info(f"{name: <10} took {seconds}s")
    return ret


    