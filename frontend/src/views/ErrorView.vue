<template>
  <onyks-container gap="m" align="center" justify="center" class="container">
    <Logos class="logos"></Logos>
    <onyks-container gap="m">
      
      <onyks-header underline size="3xl">ERROR</onyks-header>
      <onyks-text>Something went wrong</onyks-text>
      <onyks-button class="btn" @click="router.push({name: 'management'})">Return</onyks-button>
    </onyks-container>
  </onyks-container>
</template>

<style scoped>
  .container
  {
    width: 100%;
    height: 100%;
  }

  .logos
  {
    position: fixed;
    left: 0;
    top: 0;
  }

  .btn
  {
    width: 100%;
  }
</style>

<script setup>
  import Logos from '../components/Logos.vue';
  import { useLoaderStore } from '../stores/loader';
  import router from '../router';

  const loaderStore = useLoaderStore();
  loaderStore.hide()
  loaderStore.globalHide()
</script>