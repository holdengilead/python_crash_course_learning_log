from django.contrib.auth.models import User
from django.db import models


class Topic(models.Model):
    """A topic the user is learning about."""

    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """Return a string representation of the model."""
        return str(self.text)


class Entry(models.Model):
    """Something specific learned about a topic."""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Necessary for the plural name, without, entrys."""

        verbose_name_plural = "entries"

    def __str__(self) -> str:
        text = str(self.text)
        return f"{text[:50]}{'...' if len(text)>50 else ''}"
