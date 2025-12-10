from django.db import models # pyright: ignore[reportMissingModuleSource]
from django.contrib.auth.models import User
from datetime import date, timedelta

INTERVALS = {1:1, 2:2, 3:4, 4:7, 5:16}

class Card(models.Model):
    # Generic front/back so it works for vocab or Q&A
    question = models.CharField(max_length=120)
    answer = models.CharField(max_length=120)
    category = models.CharField(max_length=80, default="uncategorized")
    box = models.PositiveSmallIntegerField(default=1)
    next_due = models.DateField(default=date.today)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    # next thing should be image support 
    # and scheduling algorithm (Leitner system)
    

    def schedule(self, correct: bool):
        if correct:
            self.box = min(5, self.box + 1)
        else:
            self.box = 1
        self.next_due = date.today() + timedelta(days=INTERVALS[self.box])

    def save(self, *args, **kwargs):
        if not self.id: # pyright: ignore[reportAttributeAccessIssue]
            self.next_due = date.today()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.answer} ↔ {self.question}"
