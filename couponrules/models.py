import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone
from .helpers import get_random_code
from users.models import Product
import datetime as dt
from multiselectfield import MultiSelectField
# Create your models here.

DSC_COUPON_CODE_LENGTH = 12


class Ruleset(models.Model):
    allowed_users = models.ForeignKey('AllowedUsersRule', on_delete=models.CASCADE, verbose_name="Allowed users rule")
    max_uses = models.ForeignKey('MaxUsesRule', on_delete=models.CASCADE, verbose_name="Max uses rule")
    validity = models.ForeignKey('ValidityRule', on_delete=models.CASCADE, verbose_name="Validity rule")
    free_shipping = models.ForeignKey('FreeShippingRule', on_delete=models.CASCADE, verbose_name="Free shipping rule",
                                      null=True, blank=True)
    free_samples = models.ForeignKey('FreeSamplesRule', on_delete=models.CASCADE, verbose_name="Free Samples rule", null=True, blank=True)
    loyalty_offer = models.ForeignKey('LoyaltyStatusRule', on_delete=models.CASCADE, verbose_name="Loyalty Points rule",
                                      null=True, blank=True)
    bogo_offer = models.ForeignKey('BOGORule', on_delete=models.CASCADE, verbose_name="BOGO rule", null=True, blank=True)
    time_sensitive_coupon = models.ForeignKey('TimeSensitiveCouponRule', on_delete=models.CASCADE,
                                              verbose_name="Time-Sensitive Coupon Rule", null=True, blank=True)

    def __str__(self):
        return "Ruleset Nº{0}".format(self.id)

    class Meta:
        verbose_name = "Ruleset"
        verbose_name_plural = "Rulesets"


class AllowedUsersRule(models.Model):
    user_model = settings.AUTH_USER_MODEL

    users = models.ManyToManyField(user_model, verbose_name="Users", blank=True)
    all_users = models.BooleanField(default=False, verbose_name="All users?")

    def __str__(self):
        return "AllowedUsersRule Nº{0}".format(self.id)

    class Meta:
        verbose_name = "Allowed User Rule"
        verbose_name_plural = "Allowed User Rules"


WEEK_DAYS = (('MONDAY', 'MONDAY'),
             ('TUESDAY', 'TUESDAY'),
             ('WEDNESDAY', 'WEDNESDAY'),
             ('THURSDAY', 'THURSDAY'),
             ('FRIDAY', 'FRIDAY'),
             ('SATURDAY', 'SATURDAY'),
             ('SUNDAY', 'SUNDAY'))

HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]


class TimeSensitiveCouponRule(models.Model):
    is_eligible = models.BooleanField(default=False, verbose_name="Is Time-sensitive coupon Eligible?")
    permissible_weekdays = MultiSelectField(choices=WEEK_DAYS, blank=True, null=True)
    begin_time = models.TimeField(choices=HOUR_CHOICES, default=dt.time(00, 00), blank=True, null=True)

    def __str__(self):
        return "AllowedUsersRule Nº{0}".format(self.id)

    class Meta:
        verbose_name = "Time-Sensitive Coupon Rule"
        verbose_name_plural = "Time-Sensitive Coupon Rules"


class LoyaltyStatusRule(models.Model):
    threshold_loyalty_points = models.IntegerField(default=10000, verbose_name="Threshold loyalty points above which "
                                                                               "benefits can be redeemed")
    is_eligible = models.BooleanField(default=False, verbose_name="Is Loyalty Points Discount Eligible?")

    def __str__(self):
        return "Free LoyaltyStatus Nº{0}".format(self.id)

    class Meta:
        verbose_name = "Loyalty Status Rule"
        verbose_name_plural = "Loyalty Status Rules"


class BOGORule(models.Model):
    main_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="main_product")
    free_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="free_product")
    is_eligible = models.BooleanField(default=False, verbose_name="Is BOGO Rule applicable ?")

    def __str__(self):
        return "BOGORule Nº{0}".format(self.id)

    class Meta:
        verbose_name = "BOGO Rule"
        verbose_name_plural = "BOGO Rules"


class FreeSamplesRule(models.Model):
    threshold_amount = models.IntegerField(default=10000, verbose_name="Threshold amount above which free " +
                                                                       "samples to be given")
    is_eligible = models.BooleanField(default=False, verbose_name="Is Free Samples Gift Eligible?")

    def __str__(self):
        return "Free SampleRule Nº{0}".format(self.id)

    class Meta:
        verbose_name = "Free Sample Rule"
        verbose_name_plural = "Free Sample Rules"


class FreeShippingRule(models.Model):
    is_eligible = models.BooleanField(default=False, verbose_name="Is Free Shipping Eligible?")

    def __str__(self):
        return "Free ShippingRule Nº{0}".format(self.id)

    class Meta:
        verbose_name = "Free Shipping Rule"
        verbose_name_plural = "Free Shipping Rules"


class MaxUsesRule(models.Model):
    max_uses = models.BigIntegerField(default=0, verbose_name="Maximum uses")
    is_infinite = models.BooleanField(default=False, verbose_name="Infinite uses?")
    uses_per_user = models.IntegerField(default=1, verbose_name="Uses per user")

    def __str__(self):
        return "MaxUsesRule Nº{0}".   format(self.id)

    class Meta:
        verbose_name = "Max Uses Rule"
        verbose_name_plural = "Max Uses Rules"


class ValidityRule(models.Model):
    expiration_date = models.DateTimeField(verbose_name="Expiration date")
    is_active = models.BooleanField(default=False, verbose_name="Is active?")

    def __str__(self):
        return "ValidityRule Nº{0}".   format(self.id)

    class Meta:
        verbose_name = "Validity Rule"
        verbose_name_plural = "Validity Rules"

# RECURRENCE_CHOICES = (
#     (0, 'None'),
#     (1, 'Daily'),
#     (7, 'Weekly'),
#     (14, 'Biweekly')
# )

class CouponUser(models.Model):
    user_model = settings.AUTH_USER_MODEL

    user = models.ForeignKey(user_model, on_delete=models.CASCADE, verbose_name="User")
    coupon = models.ForeignKey('Coupon', on_delete=models.CASCADE, verbose_name="Coupon")
    times_used = models.IntegerField(default=0, editable=False, verbose_name="Times used")

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Coupon User"
        verbose_name_plural = "Coupon Users"


class Discount(models.Model):
    value = models.IntegerField(default=0, verbose_name="Value")
    is_percentage = models.BooleanField(default=False, verbose_name="Is percentage?")

    def __str__(self):
        if self.is_percentage:
            return "{0}% - Discount".format(self.value)

        return "Rs{0} - Discount".format(self.value)

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"


class Coupon(models.Model):
    code_length = DSC_COUPON_CODE_LENGTH
    code = models.CharField(max_length=code_length, default=get_random_code, verbose_name="Coupon Code", unique=True)
    discount = models. ForeignKey('Discount', on_delete=models.CASCADE)
    times_used = models.IntegerField(default=0, editable=False, verbose_name="Times used")
    created = models.DateTimeField(editable=False, verbose_name="Created")
    ruleset = models.ForeignKey('Ruleset', on_delete=models.CASCADE, verbose_name="Ruleset")

    def __str__(self):
        return self.code

    def use_coupon(self, user):
        coupon_user, created = CouponUser.objects.get_or_create(user=user, coupon=self)
        coupon_user.times_used += 1
        coupon_user.save()
        self.times_used += 1
        self.save()

    def get_discount(self):
        return {
            "value": self.discount.value,
            "is_percentage": self.discount.is_percentage
        }

    def get_discounted_value(self, initial_value):
        discount = self.get_discount()

        if discount['is_percentage']:
            new_price = initial_value - ((initial_value * discount['value']) / 100)
            new_price = new_price if new_price >= 0.0 else 0.0
        else:
            new_price = initial_value - discount['value']
            new_price = new_price if new_price >= 0.0 else 0.0

        return new_price

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Coupon, self).save(*args, **kwargs)

