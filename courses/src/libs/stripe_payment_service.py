import stripe
from libs.exceptions import CustomerNotCreatedException

from django.conf import settings


class StripePaymentService:
    def __init__(self, user):
        stripe.api_key = settings.STRIPE_API_SECRET_KEY
        self._user = user

    def get_customer(self):
        if not hasattr(self._user, 'customer'):
            raise CustomerNotCreatedException
        customer = self._retrieve_customer_by_stripe_id(self._user.customer.stripe_id)
        return customer

    def create_customer(self):
        customer = stripe.Customer.create(name=f'{self._user.id}_{self._user.username}')
        return customer

    def _retrieve_customer_by_stripe_id(self, stripe_id):
        customer = stripe.Customer.retrieve(stripe_id)
        return customer

    def create_intent(self, customer_id, payment_method_types=None):
        methods = payment_method_types or ['card']
        intent = stripe.SetupIntent.create(
            customer=customer_id,
            payment_method_types=methods,
        )
        return intent

