<script setup>
    import { RouterView, useRoute } from 'vue-router'
    import { useLoaderStore } from '@/stores/loader';

    const loaderStore = useLoaderStore()
    const route = useRoute()
</script>

<template>
    <onyks-container align="center" class="manager-view">
        <onyks-nav class="manager-nav" size="m" mobile-breakpoint="900" max-view-items="5">
            <img src="../../node_modules/onyks-web-ui-system/dist/logo.png" class="logo">
            <router-link slot="nav" to="/manager/dashboard" .selected="route.path.endsWith('/dashboard')">{{ $t('views.ManagerView.nav.dashboard') }}</router-link>
            <router-link slot="nav" to="/manager/management" .selected="route.path.endsWith('/management')">{{ $t('views.ManagerView.nav.management') }}</router-link>
            <router-link slot="nav" to="/manager/repository" .selected="route.path.endsWith('/repository')">{{ $t('views.ManagerView.nav.repository') }}</router-link>
            <router-link slot="nav" to="/manager/settings" .selected="route.path.endsWith('/settings')">{{ $t('views.ManagerView.nav.settings') }}</router-link>
            <router-link slot="nav" to="/manager/admin" .selected="route.path.endsWith('/admin')">{{ $t('views.ManagerView.nav.admin') }}</router-link>
        </onyks-nav>
        <onyks-container class="content" gap="m">
            
            <router-view v-slot="{ Component }">
                <transition name="fade" mode="out-in">
                    <component :is="Component"/>
                </transition>
            </router-view>
            <onyks-container class="footer"></onyks-container>
            <onyks-loader scroll-container=".manager-view" :isLoading.prop="loaderStore.isLoading" reset-scroll></onyks-loader>
        </onyks-container>
    </onyks-container>
</template>

<style lang="css" scoped>
    .manager-view
    {
        width: 100%;
        height: 100%;
        flex-shrink: 0;
        overflow-y: scroll;
        overflow-x: hidden;
    }

    onyks-loader
    {
        z-index: 20000;
        position: relative;
    }

    .logo
    {
        height: 100%;
        padding: var(--onyks-spacing-md);
        box-sizing: border-box;
        position: absolute;
    }

    .content
    {
        width: 100%;
        flex: 1;
        box-sizing: border-box;
    }

    .footer
    {
        height: 300px;
        width: 100%;
        background-color: var(--onyks-surface-1);
        border: 1px solid var(--onyks-surface-1-border);
        border-width: 1px 0 0 0;
        flex-shrink: 0;
        z-index: 0;
    }
</style>