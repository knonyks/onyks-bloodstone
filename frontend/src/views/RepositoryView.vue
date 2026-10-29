<script setup lang="js">
    import RepositoryExplorer from '@/components/RepositoryExplorer.vue';
    import { onMounted, reactive } from 'vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import { useLoaderStore } from '@/stores/loader';
    import { useRepositoryExplorer } from '@/composables/useRepositoryExplorer';

    const loaderStore = useLoaderStore()
    const repository = reactive(useRepositoryExplorer())
    
    onMounted(async () =>
    {
        try 
        {
            await repository.init()
            loaderStore.hide()
            loaderStore.globalHide()
        } 
        catch (err) 
        {
            console.error(err)
        }
    })
</script>

<template>
    <ManagerPage :title="$t('common.repository')">
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