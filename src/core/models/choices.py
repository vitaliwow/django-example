from typing import TypedDict

from django.utils.translation import gettext_lazy as _

from core.models import models


class PurposeChoices(models.TextChoices):
    PERSONAL = "PERSONAL", (_("Personal"))
    EDUCATIONAL = "EDUCATIONAL", (_("Educational"))
    COMMERCIAL = "COMMERCIAL", (_("Commercial"))


class MaterialsCookStatuses(models.TextChoices):
    NOT_STARTED = "NOT_STARTED", _("Not Started")
    IN_PROGRESS = "IN_PROGRESS", _("In progress")
    DONE = "DONE", _("Done")
    FAILED = "FAILED", _("Failed")
    QUEUED = "QUEUED", _("QUEUED")


class MaterialsStatuses(TypedDict):
    transcript_status: MaterialsCookStatuses
    summary_status: MaterialsCookStatuses
    short_summary_status: MaterialsCookStatuses
    quizz_status: MaterialsCookStatuses
