from django.db import models

# Create your models here.


class Entry(models.Model):
    """Entry models"""
    title = models.CharField(null=False, max_length=20)
    event = models.TextField(null=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    # Text represenation of models

    def __str__(self):
        return self.title

    # Correct the mispelling of class Entry in Django admin
    class Meta:
        """
        Change Entrys to Entries in Django models
        """
        verbose_name_plural = 'entries'
