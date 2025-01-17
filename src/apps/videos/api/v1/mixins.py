from django.db.models import QuerySet


class AccessForStaffMixin:
    def get_queryset(self) -> QuerySet:
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.for_user(user=self.request.user)
