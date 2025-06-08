from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Thread(models.Model):
    participants = models.ManyToManyField(User, related_name='threads')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.pk and self.participants.count() > 2:
            raise ValidationError('Thread cannot have more than 2 participants.')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.clean()

    def __str__(self):
        users = ", ".join([user.username for user in self.participants.all()])
        return f"Thread({users})"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField()
    thread = models.ForeignKey(Thread, related_name='messages', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} in Thread {self.thread.id}: {self.text[:30]}"
