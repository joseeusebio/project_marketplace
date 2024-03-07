<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card>
          <v-img :src="product.imageUrl" height="300" contain></v-img>
          <v-card-title>{{ product.name }}</v-card-title>
          <v-card-subtitle>
            Categoria: {{ product.category }} <br>
            Marca: {{ product.supplier }}</v-card-subtitle>
          <v-card-text>
            {{ product.description }}
            <br>
            <strong>Estoque:</strong> {{ product.stockQuantity }}
            <br>
            <strong>Preço:</strong> R$ {{ product.price }}
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" :disabled="isOutOfStock" @click="addToCart">
              Adicionar ao Carrinho
              <v-icon right>mdi-cart-plus</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import { getProductDetail, getCategoryById, getSupplierById, getStockBySku } from '../services/api';

export default {
  name: 'ProductDetail',
  props: {
    sku: String,
  },
  setup(props) {
    const product = ref({});
    const store = useStore();

    const fetchProductDetail = async () => {
      try {
        const productDetail = await getProductDetail(props.sku);
        const category = await getCategoryById(productDetail.category);
        const supplier = await getSupplierById(productDetail.supplier);
        const stock = await getStockBySku(props.sku);

        product.value = {
          ...productDetail,
          imageUrl: productDetail.image.startsWith('http') ? productDetail.image : `${process.env.VUE_APP_API_BASE_URL}${productDetail.image}`,
          category: category.name,
          supplier: supplier.name,
          stockQuantity: stock.quantity,
          selectedQuantity: 1
        };
      } catch (error) {
        console.error("Erro ao buscar detalhes do produto:", error);
      }
    };

    const addToCart = () => {
      if (product.value.stockQuantity > 0 && product.value.selectedQuantity <= product.value.stockQuantity) {
        store.dispatch('addToCart', {
          ...product.value,
          quantity: product.value.selectedQuantity,
        });
      } else {
        console.error("Quantidade solicitada não disponível no estoque.");
      }
    };

    onMounted(fetchProductDetail);

    return {
      product,
      addToCart,
    };
  },
  computed: {
    isOutOfStock() {
      const cartItem = this.$store.getters.cartItems.find(item => item.id === this.product.id);
      if (!cartItem) {
        return false; // Se o produto não está no carrinho, não está fora de estoque
      }
      return cartItem.quantity >= this.product.stockQuantity;
    }
  }
};
</script>
