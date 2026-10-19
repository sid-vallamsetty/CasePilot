"""Application configuration loaded from environment variables.

Keeping configuration here prevents API keys and model choices from being scattered
throughout the agent code. The `.env` file is convenient for local development, while
deployment environments can provide the same variables through a secret manager.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """The small set of external settings CasePilot currently needs."""

    model_provider: str
    model_name: str
    embedding_model: str
    api_key: str


def load_settings() -> Settings:
    """Load and validate local configuration without ever printing the API key."""

    # Read `.env` into the process environment. Existing environment variables win,
    # which is useful later in CI and production.
    load_dotenv(override=False)

    settings = Settings(
        model_provider=os.getenv("CASEPILOT_MODEL_PROVIDER", "gemini"),
        model_name=os.getenv("CASEPILOT_MODEL_NAME", "gemini-3.5-flash"),
        embedding_model=os.getenv("CASEPILOT_EMBEDDING_MODEL", "gemini-embedding-001"),
        api_key=os.getenv("CASEPILOT_API_KEY", ""),
    )

    if settings.model_provider.lower() != "gemini":
        raise ValueError("The initial CasePilot agent supports only the Gemini provider")
    if not settings.api_key or settings.api_key == "replace_with_your_key":
        raise ValueError("Set CASEPILOT_API_KEY in the local .env file")

    return settings
