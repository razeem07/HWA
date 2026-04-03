from django.db import models
from django.conf import settings

# Create your models here.


class Appointment(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
    ]

      # 👤 PATIENT INFO
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, db_index=True)  # 🔥 important
    email = models.EmailField(blank=True, null=True)

    specialization = models.ForeignKey(
    "administrator.Specialization",
    on_delete=models.CASCADE,
    related_name="appointments"
    )

    doctor = models.ForeignKey(
    "administrator.Doctor",
    on_delete=models.CASCADE,
    related_name="appointments"
    )

    date = models.DateField()
    time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    is_active = models.BooleanField(
        default=True
    )

    is_deleted = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']
        unique_together = ('doctor', 'date', 'time') 

   
    def __str__(self):
       return f"{self.user.first_name} - {self.doctor} ({self.date} {self.time})"
