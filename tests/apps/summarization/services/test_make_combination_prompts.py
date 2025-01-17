import pytest

from apps.summarization.models import SummarizationSettingsDetailed
from apps.summarization.services.summary.summarizer.segment import make_combination_prompts_yandexgpt

pytestmark = pytest.mark.django_db


def test_make_combination_prompts_yandexgpt() -> None:
    prompt = make_combination_prompts_yandexgpt()

    attributes = ['markdown', 'title', 'text']

    for attr in attributes:
        assert hasattr(prompt, attr), f"{attr} attribute not found in prompt"

        value = getattr(prompt, attr)
        assert isinstance(value, SummarizationSettingsDetailed), f"{attr} is not of type SummarizationSettingsDetailed"

        assert isinstance(value.system, str), f"{attr}.system is not a string"
        assert isinstance(value.template, str), f"{attr}.template is not a string"
        assert isinstance(value.prompt, (str, type(None))), f"{attr}.prompt is neither a string nor None"
        assert isinstance(value.model, str), f"{attr}.model is not a string"
        assert isinstance(value.token_capacity, int), f"{attr}.token_capacity is not an integer"
