from django.db.utils import IntegrityError
from libs.payments import PaymentService
from rest_framework import permissions, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.validators import ValidationError


class PaymentsViewSet(viewsets.ViewSet):
    """
    client_secret:
        Retrieve client secret key
    """

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated]
        permissions_dict = {
            'client_secret': [],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    @action(methods=['GET'], detail=False)
    def client_secret(self, request):
        payment_service = PaymentService(self.request.user)
        response = {
            'client_secret': payment_service.get_client_secret_key(),
        }
        return Response(response)


class CardViewSet(viewsets.ViewSet):
    """
    save_card:
        Save card for future payments
        Retrieves payment method ID as parameter `pm_id`
    """

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated]
        permissions_dict = {
            'save_card': [],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    @action(methods=['POST'], detail=False)
    def save_card(self, request):
        payment_service = PaymentService(self.request.user)
        pm_id = self.request.POST.get('pm_id', '')
        try:
            payment_service.save_card_into_db(pm_id=pm_id)
        except ValidationError as e:
            raise ValidationError(e.detail)
        return Response({}, status=status.HTTP_201_CREATED)
