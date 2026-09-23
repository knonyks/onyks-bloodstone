<script setup>
    import WarningAlert from './WarningAlert.vue';
    const props = defineProps(['title'])
</script>

<template>
    <onyks-container gap="m" class="manager-page" padding="m">
        <onyks-container class="header" padding="l">
            <onyks-header>{{ props.title }}</onyks-header>
        </onyks-container>
        <onyks-container gap="l">
            <WarningAlert></WarningAlert>
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
</style>