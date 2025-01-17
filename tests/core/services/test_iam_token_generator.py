import re

import pytest
from core.services.iam_token import IAMTokenCreator


@pytest.mark.skip("Skip for CI")
def test_transcript_generator() -> None:
    result = IAMTokenCreator()()

    assert re.match(pattern=r"t1\.[A-Z0-9a-z_-]+[=]{0,2}\.[A-Z0-9a-z_-]{86}[=]{0,2}", string=result)
