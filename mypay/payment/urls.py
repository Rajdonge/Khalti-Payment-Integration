from django.urls import path

from .views import PaymentView, VerifyKhaltiPaymentView


urlpatterns = [
    path('initiate-payment/', PaymentView.as_view(), name='payment'),
    path("confirm-payment/", VerifyKhaltiPaymentView.as_view(), name="payment-callback"),
]