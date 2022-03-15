from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from .serializers import CouponTempSerializer
from .models import Coupon
from .validations import validate_coupon
from .constants import COUPONS_RESPONSE_TEMPLATE, INVALID_TEMPLATE
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView


class CouponView(GenericAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = CouponTempSerializer

    def get_queryset(self):
        pass

    def post(self, request, *args, **kwargs):
        user = self.request.user
        coupon = get_object_or_404(Coupon, code=request.data["coupon_code"])
        if validate_coupon(coupon, user) != COUPONS_RESPONSE_TEMPLATE:
            return Response(INVALID_TEMPLATE,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'discounted_amount': coupon.get_discounted_value(request.data["amount"])},
                        status=status.HTTP_200_OK)



