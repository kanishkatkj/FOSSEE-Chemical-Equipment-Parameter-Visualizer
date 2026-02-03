from django.db import models

class Dataset(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dataset {self.id} - {self.uploaded_at}"

class EquipmentData(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='data')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=255)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()

    def __str__(self):
        return self.equipment_name
