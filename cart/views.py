from rest_framework import generics, status
from .serializers import CartSerializer, CartItemSerializer
from .models import Cart, CartItem
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import stripe
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import NotAuthenticated


class CartView(generics.RetrieveUpdateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get or create a cart for the authenticated user
        return Cart.objects.get_or_create(user=self.request.user)[0]


class CartItemView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            # this is a DRF-YASG schema generation call, do not execute the actual view logic
            return Cart.objects.none()

        # Return only cart items associated with the authenticated user's cart
        user_cart = Cart.objects.get_or_create(user=self.request.user)[0]
        return CartItem.objects.filter(cart=user_cart)

    def perform_create(self, serializer):
        if getattr(self, "swagger_fake_view", False):
            # this is a DRF-YASG schema generation call, do not execute the actual view logic
            return Cart.objects.none()

        user_cart = Cart.objects.get_or_create(user=self.request.user)[0]
        serializer.save(cart=user_cart)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            # this is a DRF-YASG schema generation call, do not execute the actual view logic
            return Cart.objects.none()

        user_cart = Cart.objects.get_or_create(user=self.request.user)[0]
        return CartItem.objects.filter(cart=user_cart)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "stripeToken": openapi.Schema(
                type=openapi.TYPE_STRING, description="Stripe token"
            ),
        },
        required=["stripeToken"],
    ),
    responses={200: "Payment successful", 400: "Payment failed"},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def charge(request):
    cart = Cart.objects.get(user=request.user)
    amount = int(cart.total_price * 100)  # Convert to cents for Stripe

    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=request.data["stripeToken"],
            description=f"Charge for {request.user.email}",
        )
        cart.stripe_charge_id = charge["id"]
        for item in cart.items.all():
            product = item.product
            product.stock -= item.quantity
            if product.stock < 0:
                return Response(
                    {"message": f"Not enough stock for product {product.name}!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            product.save()
            item.delete()

        cart.save()
        # At this point, you might want to mark the cart as paid or convert it into an order.
        return Response({"message": "Payment successful!"}, status=status.HTTP_200_OK)
    except stripe.error.CardError as e:
        return Response(
            {"message": "Your card was declined!"}, status=status.HTTP_400_BAD_REQUEST
        )
