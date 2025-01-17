import pytest
from apps.interactions.models import Quiz
from apps.interactions.services.quiz.deleter import QuizDeleter
from apps.users.models import User
from rest_framework.exceptions import ValidationError

pytestmark = [pytest.mark.django_db]


def test_deletes_ok(staff: User, quiz: Quiz) -> None:
    result = QuizDeleter(
        quiz=quiz,
        user=staff,
    )()

    assert result is None
