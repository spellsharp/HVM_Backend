from django.db import models

# This is assuming, for multiple people only one lead person has to register

class LeadVisitor(models.Model):
    full_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=200)
    accompanying_person = models.ForeignKey('Accompanying', on_delete=models.CASCADE, null=True, blank=True)
    visiting_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    
    def __str__(self):
        return [self.full_name, self.company_name, self.address, self.contact_number, self.visiting_time, self.image]

class Accompanying(models.Model):
    full_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    
    def __str__(self):
        return [self.full_name, self.company_name, self.address, self.contact_number, self.visiting_time, self.image]