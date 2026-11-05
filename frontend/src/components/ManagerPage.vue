<script setup>
    import { i18n } from '../utils/localization.js';
    import UserAlert from './UserAlert.vue';
    import WarningAlert from './WarningAlert.vue';
    import { useAuthStore } from '../stores/auth.js';
    const props = defineProps({ title: String, expand: { type: Boolean, default: false } })
    const authStore = useAuthStore();
</script>

<template>
    <onyks-container gap="m" :class="['manager-page', { expand: props.expand }]" padding="m" type="stack">
        <onyks-container class="header" padding="l">
            <onyks-header>{{ props.title }}</onyks-header>
        </onyks-container>
        <onyks-container gap="l" type="stack">
            <WarningAlert></WarningAlert>
            <UserAlert :username="authStore?.user?.username" :expiration_time="i18n.global.d(authStore?.user?.expiration_time, 'short')"></UserAlert>
            <slot></slot>
        </onyks-container>
    </onyks-container>
</template>

<style scoped>
    .header
    {
        padding-left: 0 !important;
    }

    .manager-page
    {
        max-width: 1024px;
        width: 100%;
        margin-left: auto;
        margin-right: auto;
        box-sizing: border-box;
        min-height: 100vh;
    }

    .expand
    {
        max-width: 100%;
    }
</style>