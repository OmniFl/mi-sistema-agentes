from fastapi import FastAPI
from pydantic import BaseModel
import anthropic
import os

app = FastAPI()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

class AgentRequest(BaseModel):
    tipo: str
    input_data: dict

@app.post("/run-agent")
async def run_agent(req: AgentRequest):
    roles = {
        "redactor": "Eres un experto en contenido viral para TikTok e Instagram sobre dinero online. Crea hooks y scripts virales.",
        "analista": "Eres un analista de tendencias en redes sociales. Detecta oportunidades virales en el nicho de dinero online.",
    }
    sistema = roles.get(req.tipo, "Eres un asistente útil.")
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=sistema,
        messages=[
            {"role": "user", "content": str(req.input_data)}
        ]
    )
    return {"status": "ok", "resultado": message.content[0].text}
