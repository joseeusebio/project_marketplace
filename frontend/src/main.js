import { createApp } from 'vue';
import App from './App.vue';
import { loadFonts } from './plugins/webfontloader';
import vuetify from './plugins/vuetify';
import store from './store';
import router from './router';

loadFonts();

const app = createApp(App);

app.use(vuetify);
app.use(store);
app.use(router);
app.mount('#app');
