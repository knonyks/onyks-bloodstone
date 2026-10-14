<script setup>
    import CustomAlert from './CustomAlert.vue';
    const model = defineModel()
</script>

<template>
    <onyks-dialog :open="model.open" @dialog-close="model.open = false; model.error = ''; model.name = ''" corner-close :title="model.title" bottom-buttons modal>
        <onyks-container gap="m" type="stack">
            <onyks-text>Enter name below:</onyks-text>
            <onyks-textfield v-model="model.name" @input="model.error = ''"></onyks-textfield>
            <CustomAlert :text="model.error" type="error" :show="model.error != ''"></CustomAlert>
        </onyks-container>
        <onyks-button background="green" slot="footer" @click="model.handleOK" :disabled="model.isLoading" size="m">OK</onyks-button>
    </onyks-dialog>
</template>

<style lang="css" scoped>

</style>