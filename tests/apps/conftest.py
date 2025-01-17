from unittest.mock import Mock

import pytest
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from pytest_mock import MockerFixture

from apps.videos.models import VideoFile, Video

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def pdf_file() -> ContentFile:
    return ContentFile(bytes([1]), name="summary.pdf")


@pytest.fixture()
def video_file() -> SimpleUploadedFile:
    filename = "file"
    ext = "mp4"
    return SimpleUploadedFile(
        f"{filename}.{ext}",
        bytes(3),
        content_type="video/mp4",
    )


@pytest.fixture()
def mocked_pdf_creator(mocker: MockerFixture) -> Mock:
    method = mocker.patch("apps.summarization.services.summary.creator.pdf_creator.SummaryPDFCreator.act")
    method.return_value = b"string"
    return method


@pytest.fixture()
def mocked_quiz_generator(mocker: MockerFixture) -> Mock:
    method = mocker.patch("apps.summarization.services.quiz_generator.base_creator.BaseQuizCreator.generate_quiz")
    method.return_value = [
        {
            "quiz": [
                {
                    "question": "Что будет происходить?",
                    "wrong_answers": ["Игра.", "Обед.", "Лекция."],
                    "correct_answer": "Неизвестно.",
                }
            ],
            "chapter": {"text": "Посмотреть, что у нас здесь будет.", "start": 232.179, "title": ""},
        },
        {
            "quiz": [
                {
                    "question": "Что произойдёт после перезапуска приложения?",
                    "wrong_answers": [
                        "Приложение перестанет работать.",
                        "Появится сообщение об ошибке.",
                        "Ничего не изменится.",
                    ],
                    "correct_answer": "Приложение будет работать.",
                }
            ],
            "chapter": {
                "text": "Восклицательный знак перезапустим наше приложение с вами, перезапускаем его. Вот у нас опять"
                " работает и опять же вернемся на ту страницу, на которой мы были. 127 0 0 1 8000 Но зайдем на"
                " свэш оф лайф, посмотрите, что произойдет!",
                "start": 284.009,
                "title": "",
            },
        },
    ]

    return method


@pytest.fixture()
def mocked_quiz_expenses(mocker: MockerFixture) -> Mock:
    method = mocker.patch("apps.summarization.services.quiz_generator.quiz_creator.YGPTQuizCreator.filter_expenses")
    method.return_value = {'yandex': 150}
    return method


@pytest.fixture()
def mocked_filtering_quiz_generator(mocker: MockerFixture) -> Mock:
    method = mocker.patch("apps.summarization.services.quiz_generator.base_creator.BaseQuizCreator.handle_quiz_again")
    method.return_value = [
        {
            "quiz": [
                {
                    "question": "Что будет происходить в комате?",
                    "wrong_answers": ["Игра.", "Обед.", "Лекция."],
                    "correct_answer": "Неизвестно.",
                }
            ],
            "chapter": {"text": "Посмотреть, что у нас здесь будет.", "start": 232.179, "title": ""},
        },
        {
            "quiz": [
                {
                    "question": "Что произойдёт после перезапуска веб приложения?",
                    "wrong_answers": [
                        "Приложение перестанет работать.",
                        "Появится сообщение об ошибке.",
                        "Ничего не произойдёт.",
                    ],
                    "correct_answer": "Приложение будет работать.",
                }
            ],
            "chapter": {
                "text": "Восклицательный знак перезапустим наше приложение с вами, перезапускаем его. Вот у нас опять"
                " работает и опять же вернемся на ту страницу, на которой мы были. 127 0 0 1 8000 Но зайдем на"
                " свэш оф лайф, посмотрите, что произойдет!",
                "start": 284.009,
                "title": "",
            },
        },
    ]

    return method


@pytest.fixture()
def video_file_instance(video_file: VideoFile, video: Video) -> VideoFile:
    return VideoFile.objects.create(file=video_file, video=video)
