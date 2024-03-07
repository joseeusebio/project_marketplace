<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="6" md="4" lg="3" v-for="product in products" :key="product.id" @click="navigateToProductDetail(product.sku)">
        <v-card class="pa-3" outlined elevation="2">
          <v-img :src="product.imageUrl" height="200px"></v-img>
          <v-card-title class="text-h6 mt-3">{{ product.name }}</v-card-title>
          <v-card-subtitle class="pb-4 pt-4">
            SKU: {{ product.sku }} <br>
            Categoria: {{ product.category }} <br>
            Marca: {{ product.supplier }} <br>
            Estoque: {{ product.stockQuantity }}
          </v-card-subtitle>
          <v-card-text class="display-1 pa-2 price-highlight">
            R$ {{ product.price }}
          </v-card-text>
          <v-card-actions>
            <div class="d-flex align-center justify-center quantity-controls">
              <v-btn icon small @click.stop="decrementQuantity(product)" :disabled="product.stockQuantity === 0 || product.selectedQuantity <= 1">
                <v-icon size="18">mdi-minus</v-icon>
              </v-btn>
              <input type="number" class="quantity-input" min="1" :max="product.stockQuantity" v-model.number="product.selectedQuantity" :disabled="product.stockQuantity === 0" @click.stop="handleClick">
              <v-btn icon small @click.stop="incrementQuantity(product)" :disabled="product.stockQuantity === 0 || product.selectedQuantity >= product.stockQuantity">
                <v-icon size="18">mdi-plus</v-icon>
              </v-btn>
            </div>
            <v-btn color="primary" dark :disabled="isAddToCartDisabled(product)" @click.stop="addToCart(product)">
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
import { getProducts, getCategoryById, getSupplierById, getProductsByCategory, getStockBySku } from '../services/api';

export default {
  name: 'ProductList',
  data() {
    return {
      products: [],
    };
  },
  async created() {
    await this.loadProducts();
  },
  methods: {
    async loadProducts() {
      try {
        const categoryName = this.$route.params.categoryName;
        let fetchedProducts = [];

        if (categoryName) {
          fetchedProducts = await getProductsByCategory(categoryName);
        } else {
          fetchedProducts = await getProducts();
        }

        const productsWithDetails = await Promise.all(fetchedProducts.map(async (product) => {
        const category = await getCategoryById(product.category);
        const supplier = await getSupplierById(product.supplier);
        const stockDetail = await getStockBySku(product.sku);

        return {
          ...product,
          category: category.name,
          supplier: supplier.name,
          stockQuantity: stockDetail.quantity,
          selectedQuantity: 1,
          imageUrl: product.image.startsWith('http') ? product.image : `${process.env.VUE_APP_API_BASE_URL}${product.image}`,
        };
      }));
        this.products = productsWithDetails;
        this.products = productsWithDetails;
      } catch (error) {
        console.error("Erro ao buscar produtos:", error);
      }
    },
    navigateToProductDetail(sku) {
      this.$router.push({ name: 'ProductDetail', params: { sku } });
    },
    addToCart(productToAdd) {
      event.stopPropagation();
      this.$store.dispatch('addToCart', {
        ...productToAdd,
        quantity: productToAdd.selectedQuantity,
      });
    },
    isAddToCartDisabled(product) {
      return product.selectedQuantity > product.stockQuantity || this.$store.getters.cartItems.some(cartItem => cartItem.id === product.id && cartItem.quantity >= product.stockQuantity);
    },
    incrementQuantity(product) {
      if (product.selectedQuantity < product.stockQuantity) {
        product.selectedQuantity += 1;
      }
    },
    decrementQuantity(product) {
      if (product.selectedQuantity > 1) {
        product.selectedQuantity -= 1;
      }
    },
    handleClick() {
    }
  },
  watch: {
    '$route.params.categoryName': {
      immediate: true,
      handler(newVal) {
        this.loadProducts(newVal);
      },
    },
  },
};
</script>

<style scoped>

  .price-highlight {
    font-weight: bold;
    font-size: 1.1rem;
    color: #000000;
  }

  .quantity-selector {
    max-width: 100px;
  }

  .quantity-controls {
    display: flex;
    align-items: center;
  }

  .quantity-input {
    width: 60px; /* Ajuste conforme necessário */
    text-align: center;
    border: 1px solid #e0e0e0; /* Estilo da borda do input */
    border-radius: 4px; /* Arredondamento da borda */
    padding: 5px 0; /* Preenchimento vertical para reduzir a altura */
  }

</style>