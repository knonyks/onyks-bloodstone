<script setup lang="js">
    import RepositoryExplorer from '@/components/RepositoryExplorer.vue';
    import { onMounted, ref } from 'vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import { MyRepository } from '@/utils/tools';
    import { useLoaderStore } from '@/stores/loader';

    const loaderStore = useLoaderStore()
    const repository = ref(new MyRepository((e) => e.type === 'dir' || e.type === 'schlib' || e.type === 'pcblib' || e.type === 'footprint' || e.type === 'symbol'))

    onMounted(async () =>
    {
        try 
        {
            await repository.value.init()
            loaderStore.hide()
            loaderStore.globalHide()
        } 
        catch (err) 
        {}
    })
</script>

<template>
    <ManagerPage title="Repository">
        <RepositoryExplorer v-model="repository"></RepositoryExplorer>
    </ManagerPage>
</template>

<style lang="css" scoped>
    onyks-container :deep(onyks-file-explorer)
    {
        width: 100%;
        height: 300px;
    }
</style>