import typing

import aiohttp
import httpx
import openai
from loguru import logger

from app.dto import commands


class ChatGPTClient:
    _prompt: str

    async def generate_description(self, *, command: commands.GenerateDescription) -> str:
        """Generate a description using ChatGPT."""
        raise NotImplementedError

    async def is_alive(self) -> bool:
        """Check if the ChatGPT service is available."""
        raise NotImplementedError

    def _get_prompt(self, *, command: commands.GenerateDescription) -> str:
        return (
            self._prompt
            + (
                f"name: {command.product_name}\n"
                f"description length: {command.length}\n"
                f"text tone: {command.tone_of_voice}\n"
                f"keywords: {command.keywords}\n"
                f"negative keywords: {command.minus_words}\n"
                f"product benefits: {command.advantages}\n"
                f"generate a description in Russian language"
            )
        ).replace("\n", " ")


class OpenAIChatGPTClient(ChatGPTClient):
    def __init__(
        self,
        *,
        token: str,
        prompt: str,
        proxy: str | None,
        model: str = "gpt-4o-mini",
    ) -> None:
        self._prompt = prompt
        self._proxy = proxy
        self._model = model

        if proxy:
            self._client = openai.AsyncOpenAI(api_key=token, http_client=httpx.AsyncClient(proxies=proxy))
        else:
            self._client = openai.AsyncOpenAI(api_key=token)

    async def generate_description(
        self,
        *,
        command: commands.GenerateDescription,
    ) -> str:
        """
        Asynchronously fetches a chat completion from OpenAI's ChatGPT API using the OpenAI Python library.

        Returns:
            str: The content of the assistant's reply.
        """
        response = await self._client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": self._get_prompt(command=command),
                },
            ],
            model=self._model,
        )
        return typing.cast(str, response.choices[0].message.content)

    async def is_alive(self) -> bool:
        """Check if the OpenAI ChatGPT service is available."""
        try:
            await self._client.models.retrieve(self._model)
        except openai.APIError as exc:
            logger.opt(exception=exc).error("OpenAI service is not available")
            return False
        return True


class AiohttpChatGPTClient(ChatGPTClient):
    def __init__(
        self,
        *,
        token: str,
        prompt: str,
        proxy: str | None,
        model: str = "gpt-4o-mini",
        url: str,
    ) -> None:
        self._token = token
        self._url = str(url)
        self._prompt = prompt
        self._proxy = proxy
        self._model = model

    async def generate_description(self, *, command: commands.GenerateDescription) -> str:
        """Generate a description using ChatGPT."""

        async with (
            aiohttp.ClientSession() as session,
            session.post(
                self._url,
                proxy=self._proxy,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self._token}",
                },
                json={
                    "model": self._model,
                    "messages": [
                        {
                            "role": "user",
                            "content": self._get_prompt(command=command),
                        },
                    ],
                },
            ) as resp,
        ):
            try:
                resp.raise_for_status()
            except aiohttp.ClientResponseError as exc:
                logger.opt(exception=exc).error(await resp.text())
                raise
            data = await resp.json()
            logger.info(data)
            return typing.cast(str, data["choices"][0]["message"]["content"])

    async def is_alive(self) -> bool:
        """Check if the ChatGPT service is available."""
        return True
