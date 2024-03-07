from rest_framework import serializers
from .models import Product, ProductStock, Category, Supplier, Order, OrderItem, PaymentType

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductStockSerializer(serializers.ModelSerializer):
    product_sku = serializers.SerializerMethodField()

    class Meta:
        model = ProductStock
        fields = ['product_sku', 'quantity']

    def get_product_sku(self, obj):
        return obj.product.sku

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("A quantidade não pode ser negativa.")
        return value

class CategorySerializer(serializers.ModelSerializer):
    is_subcategory = serializers.SerializerMethodField()
    parent_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'is_subcategory', 'parent_category']
    
    def get_is_subcategory(self, obj):
        return obj.parent is not None

    def get_parent_category(self, obj):
        if obj.parent:
            return obj.parent.name
        return None

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(write_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['sku', 'quantity', 'price']

    def validate_sku(self, value):
        try:
            product = Product.objects.get(sku=value)
            return product
        except Product.DoesNotExist:
            raise serializers.ValidationError("Produto com o SKU fornecido não encontrado.")

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['buyer', 'total_price', 'payment_type', 'address', 'delivery_date', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            product = item_data.pop('sku')
            OrderItem.objects.create(order=order, product=product, **item_data)
        return order

class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ['id', 'name']