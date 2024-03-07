<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8">
        <v-card class="mb-4" v-for="item in cartItemsWithTotal" :key="item.id">
          <v-card-title>
            <v-row align="center" class="mx-0">
              <v-col cols="2" class="pa-1">
                <v-img :src="item.imageUrl" contain height="100"></v-img>
              </v-col>
              <v-col cols="4" class="product-name pa-1">{{ item.name }}</v-col>
              <v-col cols="2" class="pa-1">
                <div class="d-flex align-center justify-center quantity-controls">
                  <input type="number" class="quantity-input" min="1" :max="item.stockQuantity" v-model="item.quantity" @input="updateQuantity(item, $event.target.value)">
                </div>
              </v-col>
              <v-col cols="2">{{ 'R$ ' + item.price }}</v-col>
              <v-col cols="2" class="pa-1 d-flex justify-end">
                <v-btn icon color="red" @click="removeFromCart(item)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-card-title>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Resumo do Pedido</v-card-title>
          <v-card-text>
            <div class="subtotal-highlight">
              Subtotal ({{ totalItems }} Produtos) <span class="font-weight-bold">R$ {{ totalPrice }}</span>
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" block @click="openCheckoutModal">Finalizar Compra</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  <v-dialog v-model="showCheckoutModal" persistent max-width="600px">
    <v-card>
      <v-card-title class="text-h5">Finalizar Compra</v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field label="Nome do Comprador" v-model="order.buyer" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field label="Endereço" v-model="order.address" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field label="Data de Entrega" v-model="order.delivery_date" type="date" required></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-select :items="paymentTypes" item-title="name" item-value="id" label="Tipo de Pagamento" v-model="order.payment_type" required></v-select>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="green darken-1" text @click="submitOrder">Confirmar</v-btn>
        <v-btn color="grey darken-1" text @click="showCheckoutModal = false">Cancelar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapState } from 'vuex';
import { fetchPaymentTypes } from '@/services/api';

export default {
  name: 'ShoppingCart',
  computed: {
    ...mapState({
      cartItems: state => state.cart,
    }),
    cartItemsWithTotal() {
      return this.cartItems.map(item => ({
        ...item,
        totalPrice: (item.price * item.quantity).toFixed(2),
      }));
    },
    totalItems() {
      return this.cartItems.reduce((acc, item) => acc + item.quantity, 0);
    },
    totalPrice() {
      return this.cartItems.reduce((acc, item) => acc + (item.price * item.quantity), 0).toFixed(2);
    }
  },
  data() {
    return {
      showCheckoutModal: false,
      order: {
        buyer: '',
        address: '',
        delivery_date: null,
        payment_type: null,
      },
      paymentTypes: [],
    };
  },
  async created() {
    try {
      this.paymentTypes = await fetchPaymentTypes();
    } catch (error) {
      console.error("Erro ao carregar tipos de pagamento:", error);
    }
  },
  methods: {
    openCheckoutModal() {
      this.showCheckoutModal = true;
    },
    removeFromCart(itemToRemove) {
      this.$store.dispatch('removeFromCart', itemToRemove.id);
    },
    updateQuantity(item, newQuantity) {
      const quantity = parseInt(newQuantity, 10);
      if (!isNaN(quantity) && quantity > 0 && quantity <= item.stockQuantity) {
        this.$store.dispatch('updateItemQuantity', {
          id: item.id,
          quantity: quantity,
        });
      } else {
        item.quantity = item.quantity > 0 ? item.quantity : 1;
      }
    },
    quantityOptions(stockQuantity) {
      return Array.from({ length: stockQuantity }, (_, i) => i + 1);
    },
    checkout() {
      console.log('Finalizar compra', this.order);
      this.showCheckoutModal = false;
    }
  }
};
</script>

<style scoped>
  .product-name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 250px; 
  }

  .v-card-title {
    padding-top: 4px !important; 
  }

  .v-col {
    padding: 4px !important;
  }

  .subtotal-highlight {
    font-size: 1rem;
  }

  .quantity-controls {
    width: auto;
  }

  .quantity-input {
    width: 60px; /* Ajuste conforme necessário */
    text-align: center;
    border: 1px solid #e0e0e0; /* Estilo da borda do input */
    border-radius: 4px; /* Arredondamento da borda */
    padding: 5px 0; /* Preenchimento vertical para reduzir a altura */
  }

</style>