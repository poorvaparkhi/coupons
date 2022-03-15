from django.urls import path
from .views import CouponView

app_name = 'password_reset'

urlpatterns = [
    path(
        'calculate/',
        CouponView.as_view(),
        name='Calculate Coupon',
        )
            # path(
    #     'get/',
    #     CouponViewSet.as_view({'get': 'list'}),
    #     name='Get Coupons',
    # )
]
