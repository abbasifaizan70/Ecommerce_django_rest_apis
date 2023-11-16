from rest_framework.views import APIView
from rest_framework import generics, status
from .serializers import CartSerializer, CartItemSerializer, TransactionHistorySerializer, ShippingInformationSerializer
from .models import Cart, CartItem, TransactionHistory
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
        return Cart.objects.get_or_create(user=self.request.user)[0]


class CartItemView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Cart.objects.none()
        user_cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return user_cart.items.all()

    def perform_create(self, serializer):
        if getattr(self, "swagger_fake_view", False):
            return

        user_cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product_id = serializer.validated_data['product'].id
        quantity = self.request.data.get('quantity')
        cart_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product_id=product_id,
            defaults={'quantity': 1}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            product = cart_item.product
            if quantity > 0:
                # Decrease product stock when quantity is positive
                product.stock -= quantity
                product.save()
            elif quantity < 0:
                # Increase product stock when quantity is negative
                product.stock -= quantity  # Subtracting a negative quantity increases the stock
                product.save()
        else:
            if 'quantity' in serializer.validated_data:
                cart_item.quantity = serializer.validated_data['quantity']
                cart_item.save()
                product = cart_item.product
                product.stock -= quantity
                product.save()

        if cart_item.quantity <= 0:
            cart_item.delete()

        self.cart_data = CartSerializer(instance=user_cart).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(self.cart_data, status=status.HTTP_201_CREATED)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            # This is a DRF-YASG schema generation call, do not execute the actual view logic
            return Cart.objects.none()

        return CartItem.objects.filter(cart=self.get_user_cart())

    def get_user_cart(self):
        return Cart.objects.get_or_create(user=self.request.user)[0]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.user_cart = self.get_user_cart()

    def get_cart_data(self):
        cart_serializer = CartSerializer(self.user_cart)
        return cart_serializer.data

    def get(self, request, *args, **kwargs):
        return Response(self.get_cart_data())

    def put(self, request, *args, **kwargs):
        return Response(self.get_cart_data())

    def delete(self, request, *args, **kwargs):
        cart_item = self.get_object()
         # Retrieve the product associated with the cart item
        product = cart_item.product
        # Add the cart item's quantity back to the product's stock
        product.stock += cart_item.quantity
        product.save()

        cart_item.delete()
        return Response(self.get_cart_data())


class ClearCartView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Cart.objects.get_or_create(user=self.request.user)[0]

    def delete(self, request, *args, **kwargs):
        user_cart = self.get_object()
        for cart_item in user_cart.items.all():
            product = cart_item.product
            product.stock += cart_item.quantity
            product.save()
        user_cart.items.all().delete()  # Delete all cart items
        return Response({'message': 'Cart cleared successfully'})


class UserTransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = TransactionHistory.objects.filter(user=request.user)
        serializer = TransactionHistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ShippingInformationView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        
        shipping_data = request.data
        shipping_data["cart"] = cart.id
        serializer = ShippingInformationSerializer(data=shipping_data)
        if serializer.is_valid():
            serializer.save(cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    amount = int(cart.total_price)

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount * 100,
            currency="usd",
            payment_method=request.data["stripeToken"]["token"],
            confirm=True,
            description=f"Charge for {request.user.email}",
            return_url="http://localhost:3000/shipping/"
        )

        cart.stripe_charge_id = payment_intent["id"]
        for item in cart.items.all():
            product = item.product
            TransactionHistory.objects.create(
                user=request.user,
                product=product,
                quantity=item.quantity,
                total_price=item.total_price,
                stripe_charge_id=payment_intent["id"]
            )
            item.delete()
        cart.delete()
        return Response({"message": "Payment successful!", "url": "http://localhost:3000/shipping/"}, status=status.HTTP_200_OK)
    except stripe.error.CardError as e:
        return Response(
            {"message": "Your card was declined!"}, status=status.HTTP_400_BAD_REQUEST
        )
