<template>
  <v-app>
    <MainLayout>
      <router-view></router-view>
    </MainLayout>
  </v-app>
</template>

<script>
import MainLayout from '@/components/MainLayout.vue';

export default {
  components: {
    MainLayout,
  },
};
</script>
