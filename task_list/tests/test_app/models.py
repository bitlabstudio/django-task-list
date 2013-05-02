"""Models for testing purposes."""
from django.db import models


class DummyModel(models.Model):
    """Dummy model for testing purposes."""
    user = models.ForeignKey('auth.User')
    dummy_field = models.CharField(max_length=64)

    def task_list_has_permission(self, request):
        return self.user == request.user
