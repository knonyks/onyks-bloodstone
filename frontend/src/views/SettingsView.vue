<script setup>
    import ManagerPage from '@/components/ManagerPage.vue';
    import { MyLoaderState, MyTime } from '@/utils/tools';
    import DataLoader from '@/components/DataLoader.vue';
    import { ref } from 'vue';
    import { onMounted } from 'vue';
    import { useLoaderStore } from '@/stores/loader';

    const loaderStore = useLoaderStore()

    onMounted(async () =>
    {
        loaderStore.hide()
        loaderStore.globalHide()
    })

</script>

<template>

        <ManagerPage title="Settings">
            <onyks-header level="4">Account Details</onyks-header>
            <onyks-container type="grid" cols="2" gap="m">
                <onyks-header level="6">Username:</onyks-header>
                <onyks-text>JanKowal</onyks-text>
                <onyks-header level="6">E-mail:</onyks-header>
                <onyks-text>jan.kowalski.2025@gmail.com</onyks-text>
                <onyks-header level="6">Expiration Date:</onyks-header>
                <onyks-text>2023-12-31, 23:59:59</onyks-text>
            </onyks-container>

        </ManagerPage>

</template>

<style lang="css">
</style>