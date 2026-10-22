<script setup lang="js">
    import RepositoryExplorer from '@/components/RepositoryExplorer.vue';
    import { onMounted, reactive } from 'vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import { useLoaderStore } from '@/stores/loader';
    import { useRepository } from '@/utils/tools';

    const loaderStore = useLoaderStore()
    const repository = reactive(useRepository())
    

    onMounted(async () =>
    {
        try 
        {
            await repository.init()
            loaderStore.hide()
            loaderStore.globalHide()
        } 
        catch (err) 
        {}
    })
</script>

<template>
    <ManagerPage :title="$t('views.RepositoryView.title')">
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