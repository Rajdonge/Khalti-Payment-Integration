from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
import uuid
from rest_framework import status
from .serializers import PaymentSerializer
from .models import Payment

class PaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            purchase_order_id = str(uuid.uuid4())  # Generate unique order ID

            # Save payment in the database
            payment = Payment.objects.create(
                purchase_order_id=purchase_order_id,
                purchase_order_name="Payment for Shram",
                amount=validated_data['amount'],
                name=validated_data['name'],
                email=validated_data['email'],
                phone=validated_data['phone'],
                status="Pending",
            )

            # Send request to Khalti
            url = "https://dev.khalti.com/api/v2/epayment/initiate/"
            payload = json.dumps({
                "return_url": "http://localhost:3000/payment",
                "website_url": "http://localhost:3000/",
                "amount": validated_data['amount'],
                "purchase_order_id": purchase_order_id,
                "purchase_order_name": "Payment for Shram",
                "customer_info": {
                    "name": validated_data['name'],
                    "email": validated_data['email'],
                    "phone": validated_data['phone']
                }
            })
            headers = {
                "Authorization": "Key 643469c079464a8788f05615d14be0d2",
                "Content-Type": "application/json"
            }

            try:
                response = requests.post(url, headers=headers, data=payload)
                response_data = response.json()

                if "pidx" in response_data:
                    payment.pidx = response_data["pidx"]
                    payment.save()

                return Response(response_data, status=response.status_code)
            except json.JSONDecodeError:
                return Response({"error": "Invalid response from Khalti"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyKhaltiPaymentView(APIView):
    def get(self, request):
        """ Extract pidx automatically and verify payment status from Khalti API """
        pidx = request.GET.get("pidx")

        if not pidx:
            return Response({"error": "Missing pidx"}, status=status.HTTP_400_BAD_REQUEST)

        # Call Khalti Lookup API
        url = "https://dev.khalti.com/api/v2/epayment/lookup/"
        headers = {
            "Authorization": "Key 643469c079464a8788f05615d14be0d2",
            "Content-Type": "application/json"
        }
        payload = {"pidx": pidx}

        try:
            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json()

            if response.status_code == 200 and response_data.get("status") == "Completed":
                # Update Payment Record in Database
                try:
                    payment = Payment.objects.get(pidx=pidx)
                    payment.transaction_id = response_data.get("transaction_id")
                    payment.status = "Completed"
                    payment.save()

                    return Response({"message": "Payment verified successfully", "data": response_data}, status=status.HTTP_200_OK)
                except Payment.DoesNotExist:
                    return Response({"error": "Invalid pidx in database"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"error": "Payment verification failed", "data": response_data}, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            return Response({"error": "Error verifying payment", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)