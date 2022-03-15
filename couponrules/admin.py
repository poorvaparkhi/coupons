from django.contrib import admin

# Register your models here.
from .models import (Coupon,
                                          Discount,
                                          Ruleset,
                                          CouponUser,
                                          AllowedUsersRule,
                                          MaxUsesRule,
                                          ValidityRule,
                                          FreeShippingRule,
                                          FreeSamplesRule,
                                          LoyaltyStatusRule, BOGORule, TimeSensitiveCouponRule)

from .actions import (reset_coupon_usage, delete_expired_coupons)


# Register your models here.
# ==========================
class DiscountAdminInline(admin.TabularInline):
    model = Discount
    extra = 0


class RulesetAdminInline(admin.TabularInline):
    model = Ruleset
    extra = 0

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass

@admin.register(Ruleset)
class RulesetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'allowed_users', 'max_uses', 'validity', )

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code','times_used', 'created', 'discount', 'ruleset')
    #inline_display = [DiscountAdminInline, RulesetAdminInline]
    actions = [delete_expired_coupons]


@admin.register(CouponUser)
class CouponUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'times_used', )
    actions = [reset_coupon_usage]


@admin.register(AllowedUsersRule)
class AllowedUsersRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(MaxUsesRule)
class MaxUsesRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(ValidityRule)
class ValidityRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

@admin.register(FreeShippingRule)
class FreeShippingRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

@admin.register(FreeSamplesRule)
class FreeSamplesRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

@admin.register(BOGORule)
class BOGORuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}

@admin.register(LoyaltyStatusRule)
class LoyaltyStatusRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(TimeSensitiveCouponRule)
class TimeSensitiveCouponRuleAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}