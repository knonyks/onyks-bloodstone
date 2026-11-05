<script setup>
    import ManagerPage from '../components/ManagerPage.vue';
    import { onMounted } from 'vue';
    import { useLoaderStore } from '../stores/loader';

    const loaderStore = useLoaderStore()

    onMounted(async () =>
    {
        loaderStore.hide()
        loaderStore.globalHide()
    })

</script>

<template>
    <ManagerPage title="Settings">

    </ManagerPage>
</template>

<style lang="css">
    onyks-dialog::part(content)
    {
        overflow-y: unset;
    }

    onyks-dialog::part(container)
    {
        max-height: unset;
    }
</style>