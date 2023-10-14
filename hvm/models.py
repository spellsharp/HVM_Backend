import uuid
from django.db import models

class LeadVisitor(models.Model):
    full_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    visiting_time = models.DateTimeField("Visiting Time", null=True, blank=True)
    unique_id = models.CharField(max_length=36, default=uuid.uuid4)

    def __str__(self):
        return self.full_name + " | " + self.unique_id

class Accompanying(models.Model):
    lead_visitor = models.ForeignKey(LeadVisitor, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=200)
    unique_id = models.CharField(max_length=36, default=uuid.uuid4)

    def __str__(self):
        return self.full_name + " | " + self.unique_id
