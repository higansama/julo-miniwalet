import datetime
from django.db import models
from rest_framework import serializers
from .models import *

class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletUser
        fields = "__all__"


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Koran
        fields = ["wallet_id", "amount", "reference_id", "deposit_by", "deposit_at", "balance"]
        read_only_fields = ["withdrawal_by", "withdrawal_at"]
        


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Koran
        fields = ["wallet_id", "amount", "reference_id", "withdrawal_by", "withdrawal_at", "balance"]
        read_only_fields = ["deposit_by", "deposit_at"]
        
