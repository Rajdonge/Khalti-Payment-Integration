from django.db import models

class Payment(models.Model):
    pidx = models.CharField(max_length=255, unique=True, null=True, blank=True)  # Khalti Payment ID
    transaction_id = models.CharField(max_length=255, null=True, blank=True)  # Khalti Transaction ID
    purchase_order_id = models.CharField(max_length=255, unique=True)  # Unique Order ID
    purchase_order_name = models.CharField(max_length=255)
    amount = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="Pending")  # Payment status
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of payment initiation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of last update

    def __str__(self):
        return f"Payment {self.purchase_order_id} - {self.status}"
