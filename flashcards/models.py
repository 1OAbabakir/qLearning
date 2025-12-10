from django.db import models # pyright: ignore[reportMissingModuleSource]
from django.contrib.auth.models import User
from datetime import date

class Card(models.Model):
    # Generic front/back so it works for vocab or Q&A
    question = models.CharField(max_length=120)
    answer = models.CharField(max_length=120)
    category = models.CharField(max_length=80, default="uncategorized")
    box = models.PositiveSmallIntegerField(default=1)
    next_due = models.DateField(default=date.today)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='cards_images/', null=True, blank=True)

    # next thing should be image support 
    # and scheduling algorithm (Leitner system)
    

    def save(self, *args, **kwargs):
        if not self.id: # pyright: ignore[reportAttributeAccessIssue]
            self.next_due = date.today()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.answer} ↔ {self.question}"
