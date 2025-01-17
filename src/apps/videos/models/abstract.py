from core.models import models
from core.models.choices import MaterialsCookStatuses, MaterialsStatuses


class MaterialStatus(models.Model):
    transcript_status = models.CharField(
        choices=MaterialsCookStatuses.choices,
        default=MaterialsCookStatuses.NOT_STARTED,
    )
    summary_status = models.CharField(choices=MaterialsCookStatuses.choices, default=MaterialsCookStatuses.NOT_STARTED)
    short_summary_status = models.CharField(
        choices=MaterialsCookStatuses.choices,
        default=MaterialsCookStatuses.NOT_STARTED,
    )
    quizz_status = models.CharField(choices=MaterialsCookStatuses.choices, default=MaterialsCookStatuses.NOT_STARTED)

    def update_material_statuses(self, set_of_statuses: MaterialsStatuses) -> None:
        self.transcript_status = set_of_statuses.get("transcript_status")
        self.summary_status = set_of_statuses.get("summary_status")
        self.short_summary_status = set_of_statuses.get("short_summary_status")
        self.quizz_status = set_of_statuses.get("quizz_status")
        self.save()

    def return_actual_statuses(self) -> dict:
        return {
            "transcript_status": self.transcript_status,
            "summary_status": self.summary_status,
            "short_summary_status": self.short_summary_status,
            "quizz_status": self.quizz_status,
        }

    class Meta:
        abstract = True
