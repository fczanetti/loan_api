from django.db import models


class Bank(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.pk} - {self.name}'


class Loan(models.Model):
    value = models.PositiveIntegerField()
    interest_rate = models.FloatField()
    ip_address = models.CharField(max_length=128)
    request_date = models.DateField(auto_now_add=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    client = models.CharField(max_length=64)


class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    value = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.pk} - ${self.value:.2f}'
