import typing

import aiocache
import pydantic
import pydantic_settings

from app.dto import annotations


class WBConSettings(pydantic_settings.BaseSettings):
    WB_URL: annotations.HttpsUrl
    WB_TOKEN: pydantic.SecretStr


class GeneratorSettings(pydantic_settings.BaseSettings):
    GPT_PROMPT: str = """I want you to present yourself as an e-commerce SEO expert who writes compelling
 product descriptions for users who want to make a purchase online. I'm going to provide the
 name of one product. The main goal of these teams is to develop a new, informative and
 fascinating resume/product description, rich in keywords, with a volume of less than the
 specified length. The purpose of the product description is to promote the product among
 users who want to buy it. Use emotional words that are defined by a given tone and creative
 reasons to show why the user should buy the product I'm telling you about.
 Write a convincing and professional-sounding description that will include the
 same wording as the text of the description of the new product. Don't repeat my hint. Don't
 remind me what I asked you to do. Don't apologize. Don't refer to yourself. Never count
 spaces and line breaks as a character.\n"""

    OPENAI_API_KEY: pydantic.SecretStr

    GPT_URL: annotations.HttpsUrl = "https://api.openai.com/v1/chat/completions"

    GPT_PROXY: str | None

    CLUSTERS_SERVICE_URL: annotations.HttpsUrl

    GPT_MODEL: str = "gpt-3.5-turbo"


class AppSettings(pydantic_settings.BaseSettings):
    ENVIRONMENT: typing.Literal["local", "dev", "prod"]
    DEBUG: bool
    AUTH_TOKEN: pydantic.SecretStr

    HOST: str
    PORT: int

    CACHE_TYPE: type[aiocache.BaseCache] = aiocache.Cache.MEMORY

    @property
    def IS_PRODUCTION(self) -> bool:
        return self.ENVIRONMENT == "prod"


@typing.final
class Settings(
    WBConSettings,
    GeneratorSettings,
    AppSettings,
):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings: typing.Final = Settings(_env_file=".env")  # type: ignore[call-arg]
