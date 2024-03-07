from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.response import Response
from .models import Product, ProductStock, Supplier, Category, PaymentType
from .serializers import ProductSerializer, ProductStockSerializer, CategorySerializer, SupplierSerializer, OrderSerializer, PaymentTypeSerializer
from django.core.exceptions import ObjectDoesNotExist

#Views Product
class ProductCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        category_name = data.get('category_name', "sem categoria").lower()

        try:
            if category_name:
                category = Category.objects.get(name=category_name)
            else:
                category, _ = Category.objects.get_or_create(name="sem categoria")
            data['category'] = category.pk
        except ObjectDoesNotExist:
            return Response({"error": f"Categoria '{category_name}' não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductListView(APIView):
    def get(self, request, format=None):
        category_name = request.query_params.get('category', None)
        if category_name:
            products = Product.objects.filter(category__name=category_name)
        else:
            products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailView(APIView):
    def get(self, request, sku, format=None):
        try:
            product = Product.objects.get(sku=sku)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)

class ProductUpdateView(APIView):
    def patch(self, request, sku, format=None):
        try:
            product = Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            return Response({"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        category_name = request.data.get('category_name')
        if category_name is not None:
            try:
                category = Category.objects.get(name=category_name.lower())
                product.category = category
            except Category.DoesNotExist:
                return Response({"error": f"Categoria '{category_name}' não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data.pop('category_name', None)
        serializer = ProductSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteView(APIView):
    def delete(self, request, sku, format=None):
        try:
            product = Product.objects.get(sku=sku)
            if ProductStock.objects.filter(product=product, quantity__gt=0).exists():
                return Response({"error": "Não é possível deletar produtos com saldo."}, status=status.HTTP_400_BAD_REQUEST)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)

#Views Category
class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class CategoryCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        name = data.get('name', '').lower()
        
        if Category.objects.filter(name=name).exists():
            return Response({"error": f"A categoria '{name}' já existe."}, status=status.HTTP_400_BAD_REQUEST)
        
        parent_name = data.get('parent_name', '').lower()
        if parent_name:
            try:
                parent = Category.objects.get(name=parent_name)
                data['parent'] = parent.id
            except Category.DoesNotExist:
                return Response({"error": f"Categoria pai '{parent_name}' não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        else:
            data.pop('parent_name', None)

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"error": "Categoria não encontrada."}, status=status.HTTP_404_NOT_FOUND)

class CategoryUpdateView(APIView):
    def patch(self, request, name, format=None):
        try:
            category = Category.objects.get(name=name.lower())
            serializer = CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"error": "Categoria não encontrada."}, status=status.HTTP_404_NOT_FOUND)

class CategoryDeleteView(APIView):
    def delete(self, request, name, format=None):
        try:
            category = Category.objects.get(name=name)
            if Product.objects.filter(category=category).exists():
                return Response({"error": "Não é possível deletar categorias associadas a produtos."}, status=status.HTTP_400_BAD_REQUEST)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"error": "Categoria não encontrada."}, status=status.HTTP_404_NOT_FOUND)

#Views Supplier
class SupplierListView(APIView):
    def get(self, request, *args, **kwargs):
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

class SupplierCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SupplierDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            supplier = Supplier.objects.get(pk=pk)
            serializer = SupplierSerializer(supplier)
            return Response(serializer.data)
        except Supplier.DoesNotExist:
            return Response({"error": "Fornecedor não encontrado."}, status=status.HTTP_404_NOT_FOUND)

class SupplierUpdateView(APIView):
    def patch(self, request, pk, *args, **kwargs):
        try:
            supplier = Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            return Response({"error": "Fornecedor não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SupplierSerializer(supplier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SupplierDeleteView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            supplier = Supplier.objects.get(pk=pk)
            if supplier.product_set.exists():
                return Response({"error": "Não é possível deletar fornecedores vinculados a produtos."}, status=status.HTTP_400_BAD_REQUEST)
            
            supplier.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Supplier.DoesNotExist:
            return Response({"error": "Fornecedor não encontrado."}, status=status.HTTP_404_NOT_FOUND)

#Views Stock
class StockListView(APIView):
    def get(self, request, format=None):
        product_stocks = ProductStock.objects.all()
        serializer = ProductStockSerializer(product_stocks, many=True)
        return Response(serializer.data)

class StockDetailView(APIView):
    def get(self, request, sku, format=None):
        try:
            product = Product.objects.get(sku=sku)
            product_stock = ProductStock.objects.get(product=product)
            serializer = ProductStockSerializer(product_stock)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({"error": f"Produto com SKU {sku} não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except ProductStock.DoesNotExist:
            return Response({"error": f"Estoque não encontrado para o produto com SKU {sku}."}, status=status.HTTP_404_NOT_FOUND)
    
class StockUpdateView(APIView):
    def patch(self, request, sku, format=None):
        product = Product.objects.filter(sku=sku).first()
        if not product:
            return Response({"error": f"Produto com SKU {sku} não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        product_stock, created = ProductStock.objects.get_or_create(product=product)
        data = {'quantity': request.data.get('quantity')}
        serializer = ProductStockSerializer(product_stock, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        payment_type_name = request.data.get('payment_type', None)
        
        if payment_type_name:
            try:
                payment_type = PaymentType.objects.get(name=payment_type_name)
                request.data['payment_type'] = payment_type.id 
            except PaymentType.DoesNotExist:
                return Response({"error": "Payment type not found."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            items = request.data.get('items', [])
            calculated_total_price = sum(item.get('price', 0) * item.get('quantity', 0) for item in items)

            if calculated_total_price != float(request.data.get('total_price', 0)):
                return Response({"error": "Total price does not match with the sum of products' prices times quantities."}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                order = serializer.save()

                for item in items:
                    sku = item.get('sku')
                    quantity_requested = item.get('quantity')
                    product_stock = ProductStock.objects.select_for_update().get(product__sku=sku)

                    if product_stock.quantity >= quantity_requested:
                        product_stock.quantity -= quantity_requested
                        product_stock.save()
                    else:
                        transaction.rollback()
                        return Response({"error": f"Not enough stock for product with SKU {sku}."}, status=status.HTTP_400_BAD_REQUEST)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PaymentTypeListView(APIView):
    def get(self, request, format=None):
        payment_types = PaymentType.objects.all()
        serializer = PaymentTypeSerializer(payment_types, many=True)
        return Response(serializer.data)