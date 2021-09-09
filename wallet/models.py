from re import T
from django.db import models

# Create your models here.
class WalletUser(models.Model):
    customer_xid = models.CharField(max_length=128, primary_key=True, unique=True)

    def __str__(self):
        return self.customer_xid

    def is_authenticated(self):
        pass

class Wallet(models.Model):
    owner = models.ForeignKey(WalletUser, on_delete=models.DO_NOTHING)
    status = models.CharField(default="0", max_length=10)  # 0. Disabled, 1. Enabled
    enabled_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.pk) + " " + self.status

class Koran(models.Model):
    wallet_id = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    amount = models.IntegerField()
    reference_id = models.CharField(max_length=32, blank=False)
    deposit_by = models.CharField(max_length=128, blank=True, null=True)
    deposit_at = models.DateTimeField(blank=True, null=True)
    withdrawal_by = models.CharField(max_length=128,blank=True, null=True)
    withdrawal_at = models.DateTimeField(blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.pk) + " " + str(self.amount)
