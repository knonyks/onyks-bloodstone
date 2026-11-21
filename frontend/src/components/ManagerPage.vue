<script setup>
    import WarningAlert from './WarningAlert.vue';
    const props = defineProps({ title: String, expand: { type: Boolean, default: false } })
</script>

<template>
    <onyks-container gap="m" :class="['manager-page', { expand: props.expand }]" padding="m" type="stack">
        <onyks-container class="header" padding="l">
            <onyks-header underline size="4xl">{{ props.title }}</onyks-header>
        </onyks-container>
        <onyks-container gap="m" type="stack">
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

    .expand
    {
        max-width: 100%;
    }
</style>