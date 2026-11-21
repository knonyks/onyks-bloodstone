<script setup>
    import { RouterView, useRoute } from 'vue-router'
    import { useLoaderStore } from '../stores/loader';
    import { useAuthStore } from '../stores/auth';
    import UserTile from '../components/UserTile.vue';
    import { i18n } from '../utils/localization.js';

    const loaderStore = useLoaderStore()
    const route = useRoute()
    const authStore = useAuthStore()
</script>

<template>
    <onyks-container align="center" class="manager-view">
        <onyks-nav class="manager-nav" size="m" mobile-breakpoint="900" max-view-items="5">
            <img src="../../node_modules/onyks-web-ui/dist/logo.png" class="logo">
            <router-link slot="nav" to="/manager/dashboard" .selected="route.path.endsWith('/dashboard')">{{ $t('common.dashboard') }}</router-link>
            <router-link slot="nav" to="/manager/management" .selected="route.path.endsWith('/management')">{{ $t('common.management') }}</router-link>
            <router-link slot="nav" to="/manager/repository" .selected="route.path.endsWith('/repository')">{{ $t('common.repository') }}</router-link>
            <router-link slot="nav" to="/manager/settings" .selected="route.path.endsWith('/settings')">{{ $t('common.settings') }}</router-link>
            <router-link v-if="authStore.user?.rank === 'admin'" slot="nav" to="/manager/admin" .selected="route.path.endsWith('/admin')">{{ $t('common.admin_panel') }}</router-link>
        </onyks-nav>
        <onyks-container class="content" gap="m">
            
            <router-view v-slot="{ Component, route }" >
                <transition name="fade" mode="out-in">
                    <component :is="Component" :key="route.fullPath"/>
                </transition>
            </router-view>
            <onyks-container class="footer" align="center">

            </onyks-container>
            <onyks-loader scroll-container=".manager-view" :isLoading.prop="loaderStore.isLoading" reset-scroll></onyks-loader>
        </onyks-container>
        <UserTile :username="authStore?.user?.username" :expiration_time="i18n.global.d(authStore?.user?.expiration_time, 'short')"></UserTile>
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
        position: relative;
        z-index: 20;
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