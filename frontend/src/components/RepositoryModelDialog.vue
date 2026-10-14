<script setup>
    import RepositoryExplorer from './RepositoryExplorer.vue';

    const model = defineModel()
</script>


<template>
    <onyks-dialog :open="model.open" :title="model.title" corner-close bottom-buttons modal @dialog-close="model.open = false">
        <onyks-container type="stack" padding="" gap="l">
            <RepositoryExplorer v-model="model.repository"></RepositoryExplorer>
        </onyks-container>
        <onyks-button background="green" slot="footer" @click="console.log">OK</onyks-button>
    </onyks-dialog>
</template>

<style lang="css" scoped>
    onyks-dialog::part(container)
    {
        max-height: 80vh;
        height: fit-content;
    }

    onyks-dialog
    {
        position: fixed;
    }
</style>