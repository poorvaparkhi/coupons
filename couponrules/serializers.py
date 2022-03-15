from rest_framework import serializers
from .models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('code_length', 'code', 'discount',
                  'times_used', 'created', 'ruleset')

class CouponTempSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""
    coupon_code = serializers.CharField()
    amount = serializers.IntegerField()
