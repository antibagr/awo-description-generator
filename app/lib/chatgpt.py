import typing

import aiohttp
import openai

from app.dto import commands


class ChatGPTClient:
    async def generate_description(self, *, command: commands.GenerateDescription) -> str:
        """Generate a description using ChatGPT."""
        raise NotImplementedError

    async def is_alive(self) -> bool:
        """Check if the ChatGPT service is available."""
        raise NotImplementedError


class OpenAIChatGPTClient(ChatGPTClient):
    def __init__(self, *, api_key: str) -> None:
        self._client = openai.AsyncOpenAI(api_key=api_key)

    async def generate_description(
        self,
        *,
        command: commands.GenerateDescription,
    ) -> str:
        """
        Asynchronously fetches a chat completion from OpenAI's ChatGPT API using the OpenAI Python library.

        Parameters:
            messages (list): A list of message objects, where each message is a dict with 'role' and 'content'.
            model (str): The model to use (e.g., 'gpt-4', 'gpt-3.5-turbo'). Default is 'gpt-4'.
            temperature (float): Sampling temperature. Higher values mean more creative responses.
            max_tokens (int): Maximum number of tokens in the response.

        Returns:
            str: The content of the assistant's reply.
        """
        try:
            response = await self._client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": "Say this is a test",
                    }
                ],
                model="gpt-4o",
            )
            return response.choices[0].message["content"].strip()
        except openai.error.OpenAIError as exc:
            # Handle OpenAI API errors
            raise Exception(f"OpenAI API error: {exc}")
        except Exception as exc:
            # Handle other possible errors
            raise Exception(f"An unexpected error occurred: {exc}")

    async def is_alive(self) -> bool:
        """Check if the OpenAI ChatGPT service is available."""
        return True


class AiohttpChatGPTClient(ChatGPTClient):
    def __init__(
        self,
        *,
        token: str,
        url: str,
        prompt: str,
        proxy: str | None,
        model: str = "gpt-3.5-turbo-16k",
    ) -> None:
        self._token = token
        self._url = url
        self._prompt = prompt
        self._proxy = proxy
        self._model = model

    async def generate_description(self, *, command: commands.GenerateDescription) -> str:
        """Generate a description using ChatGPT."""

        gpt_params = (
            f"name: {command.product_name}\n"
            f"description length: {command.length.split('_')[1]}\n"
            f"text tone: {command.tone_of_voice}\n"
            f"keywords: {command.keywords}\n"
            f"negative keywords: {command.minus_words}\n"
            f"product benefits: {command.advantages}\n"
            f"generate a description in Russian language"
        )
        async with (
            aiohttp.ClientSession() as session,
            session.post(
                self._url,
                proxy=self._proxy,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self._token}",
                },
                data={
                    "model": self._model,
                    "messages": [
                        {"role": "user", "content": self._prompt + gpt_params},
                    ],
                },
            ) as resp,
        ):
            resp.raise_for_status()
            data = await resp.json()
            return typing.cast(str, data["choices"][0]["message"]["content"])

    async def is_alive(self) -> bool:
        """Check if the ChatGPT service is available."""
        return True
