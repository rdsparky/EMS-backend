from django.db import models
import uuid


# Create your models here.
class BaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ["-created_at"]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """
        print: {id}/created_date
        :return:
        """
        return "{}-{}".format(self.id, self.created_at)
