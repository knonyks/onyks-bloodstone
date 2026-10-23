<script setup>
    import CustomAlert from './CustomAlert.vue';
    const model = defineModel()
</script>

<template>
    <onyks-dialog :open="model.open" @dialog-close="model.open = false; model.error = ''; model.name = ''" corner-close :title="model.title" bottom-buttons modal>
        <onyks-container gap="m" type="stack">
            <onyks-header level="6">{{ $t('components.EditItemDialog.subtitle1') }} {{ model.item?.name || '' }}</onyks-header>
            <onyks-text>{{ $t('components.EditItemDialog.subtitle2') }}</onyks-text>
            <form @submit.prevent="model.handleOK">
                <onyks-textfield :error="model.error != ''" v-model="model.name" @input="model.error = ''" @keydown.enter.prevent="model.handleOK"></onyks-textfield>
            </form>
            <onyks-text>{{ model.error }}</onyks-text>
        </onyks-container>
        <onyks-button background="green" slot="footer" @click="model.handleOK" :disabled="model.isLoading" size="m">OK</onyks-button>
    </onyks-dialog>
</template>

<style lang="css" scoped>
    onyks-text:empty::before 
    {
        content: "\00A0";
    }
</style>