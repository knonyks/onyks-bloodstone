<script setup>
    import CustomAlert from './CustomAlert.vue';
    import RepositoryExplorer from './RepositoryExplorer.vue';
    const model = defineModel()
</script>

<template>
    <onyks-dialog :open="model.open" :title="model.title" corner-close bottom-buttons modal @dialog-close="model.open = false">
        <onyks-container type="stack" padding="" gap="m">
            <CustomAlert :text="model.error" type="error" :show="model.error !== ''"></CustomAlert>
            <RepositoryExplorer v-model="model.repository"></RepositoryExplorer>
        </onyks-container>
        <onyks-button background="green" slot="footer" @click="model.handleOk">OK</onyks-button>
    </onyks-dialog>
</template>

<style lang="css" scoped>
    onyks-dialog::part(container)
    {
        max-height: 80vh;
        height: fit-content;
    }

    onyks-dialog::part(content)
    {
        overflow-y: auto;
    }

    onyks-dialog
    {
        position: fixed;
    }
</style>