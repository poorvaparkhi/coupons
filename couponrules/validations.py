from .models import Coupon, CouponUser
from django.utils import timezone
from .constants import COUPONS_RESPONSE_TEMPLATE, INVALID_TEMPLATE
import calendar
from datetime import date, datetime

def assemble_invalid_message(message=""):
    response = INVALID_TEMPLATE
    response['message'] = message
    return response


def validate_allowed_users_rule(coupon_object, user):
    allowed_users_rule = coupon_object.ruleset.allowed_users
    if not user in allowed_users_rule.users.all():
        return False if not allowed_users_rule.all_users else True

    return True


def validate_max_uses_rule(coupon_object, user):
    max_uses_rule = coupon_object.ruleset.max_uses
    if coupon_object.times_used >= max_uses_rule.max_uses and not max_uses_rule.is_infinite:
        return False

    try:
        coupon_user = CouponUser.objects.get(user=user)
        if coupon_user.times_used >= max_uses_rule.uses_per_user:
            return False
    except CouponUser.DoesNotExist:
        pass

    return True


def validate_free_shipping_rule(coupon_object):
    validity_rule = coupon_object.ruleset.free_shipping
    return validity_rule.is_eligible

def validate_bogo_rule(coupon_object):
    validity_rule = coupon_object.ruleset.bogo_offer
    return validity_rule.is_eligible

def validate_loyalty_points_rule(coupon_object):
    validity_rule = coupon_object.ruleset.loyalty_offer
    return validity_rule.is_eligible

def validate_time_sensitive_coupons_rule(coupon_object):
    validity_rule = coupon_object.ruleset.time_sensitive_coupon
    day_of_week = calendar.day_name[date.today().weekday()]
    now = datetime.now()
    current_hour = now.strftime("%H")
    if day_of_week in validity_rule.permissible_weekdays and (validity_rule.begin_time <= current_hour
        <= (validity_rule.begin_time +1)) and validity_rule.is_eligible:
        return True
    return False

def validate_free_samples_rule(coupon_object):
    validity_rule = coupon_object.ruleset.free_samples
    return validity_rule.is_eligible


def validate_validity_rule(coupon_object):
    validity_rule = coupon_object.ruleset.validity
    if timezone.now() > validity_rule.expiration_date:
        return False

    return validity_rule.is_active


def validate_coupon(coupon_code, user):
    if not coupon_code:
        return assemble_invalid_message(message="No coupon code provided!")

    if not user:
        return assemble_invalid_message(message="No user provided!")

    try:
        coupon_object = Coupon.objects.get(code=coupon_code)
    except Coupon.DoesNotExist:
        return assemble_invalid_message(message="Coupon does not exist!")

    valid_allowed_users_rule = validate_allowed_users_rule(coupon_object=coupon_object, user=user)
    if not valid_allowed_users_rule:
        return assemble_invalid_message(message="Invalid coupon for this user!")

    valid_max_uses_rule = validate_max_uses_rule(coupon_object=coupon_object, user=user)
    if not valid_max_uses_rule:
        return assemble_invalid_message(message="Coupon uses exceeded for this user!")

    valid_validity_rule = validate_validity_rule(coupon_object=coupon_object)
    if not valid_validity_rule:
        return assemble_invalid_message(message="Invalid coupon!")

    free_shipping_rule = validate_free_shipping_rule(coupon_code)
    if free_shipping_rule:
        COUPONS_RESPONSE_TEMPLATE[free_shipping_rule] = True

    free_samples_rule = validate_free_samples_rule(coupon_code)
    if free_samples_rule:
        COUPONS_RESPONSE_TEMPLATE[free_samples_rule] = True

    bogo_rule = validate_bogo_rule(coupon_code)
    if bogo_rule:
        COUPONS_RESPONSE_TEMPLATE[bogo_rule] = True

    loyalty_points_rule = validate_loyalty_points_rule(coupon_code)
    if loyalty_points_rule:
        COUPONS_RESPONSE_TEMPLATE[loyalty_points_rule] = True

    time_sensitive_coupons = validate_time_sensitive_coupons_rule(coupon_code)

    if time_sensitive_coupons:
        COUPONS_RESPONSE_TEMPLATE[time_sensitive_coupons] = True

    return COUPONS_RESPONSE_TEMPLATE
