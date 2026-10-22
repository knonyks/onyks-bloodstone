<script setup>
    import CustomAlert from './CustomAlert.vue';
    const model = defineModel()
</script>

<template>
    <onyks-dialog :open="model.open" @dialog-close="model.open = false; model.error = ''; model.name = ''" corner-close :title="model.title" bottom-buttons modal>
        <onyks-container gap="m" type="stack">
            <onyks-text>{{ $t('components.AddItemDialog.subtitle') }}</onyks-text>
            <form @submit.prevent="model.handleOK">
                <onyks-textfield :error="model.error != ''" v-model="model.name" @input="model.error = ''" @keydown.enter.prevent="model.handleOK()"></onyks-textfield>
            </form>
            <onyks-text type="error">{{ model.error }}</onyks-text>
            <!-- <CustomAlert :text="model.error" type="error" :show="model.error != ''" size="s"></CustomAlert> -->
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