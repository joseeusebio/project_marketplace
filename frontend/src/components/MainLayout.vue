<template>
  <v-app>
    <v-app-bar app color="blue darken-2" dark>
      <v-btn text @click="$router.push('/')">
        <v-toolbar-title>Marketplace</v-toolbar-title>
      </v-btn>
      
      <v-menu open-on-hover offset-y>
        <template v-slot:activator="{ props, on }">
          <v-btn dark v-bind="props" v-on="on">
            Categorias
          </v-btn>
        </template>

        <v-list dense>
          <v-list-item
            v-for="category in categories"
            :key="category.id"
            @click="() => selectCategory(category)">
            <v-list-item-title>{{ capitalizeFirstLetter(category.name) }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <v-btn text @click="$router.push('/')">Home</v-btn>
      <v-btn text>Sobre</v-btn>
      <v-btn text>Contato</v-btn>

      <v-spacer></v-spacer>

      <v-btn icon @click="$router.push('/cart')">
        <v-badge color="red" :content="totalCartItems" overlap>
          <v-icon color="white">mdi-cart</v-icon>
        </v-badge>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <slot></slot>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { getCategories } from '@/services/api';
import { mapState } from 'vuex';

export default {
  name: 'MainLayout',
  data() {
    return {
      categories: [],
    };
  },
  computed: {
    ...mapState(['cart']),
    showCart() {
      return this.$store.state.showCart;
    },
    totalCartItems() {
      return this.cart.reduce((total, item) => total + item.quantity, 0);
    }
  },
  async created() {
    try {
      const data = await getCategories();
      this.categories = data;
    } catch (error) {
      console.error("Erro ao buscar categorias:", error);
    }
  },
  methods: {
    selectCategory(category) {
    this.$router.push(`/category/${category.name}`);
    },
    resetCategory() {
      this.$router.push('/');
    },
    capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
    },
  },
};
</script>
