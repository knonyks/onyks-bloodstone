<script setup>
    import { useLoaderStore } from '@/stores/loader';
    const loaderStore = useLoaderStore()
</script>

<template>

    <onyks-container padding="m" class="toast-container">
        <onyks-toast-container class="toast-container-content">
        </onyks-toast-container>
    </onyks-container>

    <onyks-container class="container" align="center">
        <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in" appear>
                <component :is="Component"/>
            </transition>
        </router-view>
    </onyks-container>

    <onyks-loader :isLoading.prop="loaderStore.globalIsLoading" reset-scroll full-page></onyks-loader>
</template>

<style lang="css">
    html, body, #app 
    {
        height: 100vh;
        margin: 0;
        padding: 0;
    }

    #app
    {
        overflow-y: hidden;
    }

    .toast-container
    {
        position: fixed;
        right: 0;
        bottom: 0;
        max-width: 400px;
        width: 100%;
        box-sizing: border-box;
        z-index: 101;
    }

    onyks-nav
    {
        position: sticky;
        top: 0;
        z-index: 101;
        width: 100%;
        flex-shrink: 0;
    }

    onyks-dialog
    {
        z-index: 12;
    }

    onyks-button
    {
        min-width: 120px;
    }

    .fade-enter-active, .fade-leave-active
    {
        transition: opacity 0.25s ease;
    }

    .fade-enter-from, .fade-leave-to
    {
        opacity: 0;
    }

    .fade-enter-to, .fade-leave-from
    {
        opacity: 1;
    }
</style>

<style lang="css" scoped>
    .container
    {
        width: 100%;
        height: 100%;
    }
</style>