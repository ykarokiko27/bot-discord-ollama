import discord
import requests

TOKEN = "token_real"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith("!ia"):
        pergunta = message.content[3:].strip()

        if not pergunta:
            await message.channel.send("Digite uma pergunta depois de `!ia`.")
            return

        async with message.channel.typing():
            try:
                resposta = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL,
                        "prompt": pergunta,
                        "stream": False
                    }
                )

                dados = resposta.json()
                texto = dados["response"]

                await message.channel.send(texto[:2000])

            except Exception as erro:
                print(erro)
                await message.channel.send("❌ Não consegui falar com a IA.")


client.run(TOKEN)
