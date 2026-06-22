import sys
from types import ModuleType
from unittest.mock import MagicMock


def _patch_vertexai():
    community = (
        sys.modules.get("langchain_community")
        or ModuleType("langchain_community")
    )

    chat_models = (
        sys.modules.get("langchain_community.chat_models")
        or ModuleType("langchain_community.chat_models")
    )

    vertexai_mod = ModuleType(
        "langchain_community.chat_models.vertexai"
    )

    vertexai_mod.ChatVertexAI = MagicMock()

    sys.modules.setdefault(
        "langchain_community",
        community
    )

    sys.modules.setdefault(
        "langchain_community.chat_models",
        chat_models
    )

    sys.modules[
        "langchain_community.chat_models.vertexai"
    ] = vertexai_mod


_patch_vertexai()