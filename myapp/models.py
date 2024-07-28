from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expenses(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    Expense_reason=models.CharField(max_length=100)
    Expense_amount=models.IntegerField()
    Expense_timestamp=models.DateTimeField(auto_now_add=True)