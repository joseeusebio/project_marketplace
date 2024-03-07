import { createStore } from 'vuex';

export default createStore({
  state() {
    return {
      cart: [],
    };
  },
  mutations: {
    ADD_TO_CART(state, product) {
      const exists = state.cart.find(item => item.id === product.id);
      if (exists) {
        exists.quantity += product.quantity;
      } else {
        state.cart.push({ ...product, quantity: product.quantity });
      }
    },
    REMOVE_FROM_CART(state, itemId) {
      state.cart = state.cart.filter(item => item.id !== itemId);
    },
    UPDATE_ITEM_QUANTITY(state, { id, quantity }) {
      const item = state.cart.find(item => item.id === id);
      if (item) {
        item.quantity = quantity;
      }
    },
  },
  actions: {
    addToCart({ commit }, product) {
      commit('ADD_TO_CART', product);
    },
    removeFromCart({ commit }, itemId) {
      commit('REMOVE_FROM_CART', itemId);
    },
    updateItemQuantity({ commit }, { id, quantity }) {
      commit('UPDATE_ITEM_QUANTITY', { id, quantity });
    },
  },
  getters: {
    cartItems: (state) => state.cart, 
  }
});
