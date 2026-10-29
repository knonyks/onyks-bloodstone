<script setup>
    const model = defineModel()
</script>

<template>
    <onyks-dialog :open="model.open" @dialog-close="model.open = false; model.error = ''; model.name = ''" corner-close :title="model.title" bottom-buttons modal>
        <onyks-container gap="m" type="stack">
            <onyks-header level="6">{{ $t('common.you_editing', [model.item?.name || '']) }}</onyks-header>
            <onyks-text>{{ $t('common.enter_new_name_below') }}</onyks-text>
            <form @submit.prevent="model.handle_ok">
                <onyks-textfield :error="model.error != ''" v-model="model.name" @input="model.error = ''" @keydown.enter.prevent="model.handle_ok"></onyks-textfield>
            </form>
            <onyks-text>{{ model.error }}</onyks-text>
        </onyks-container>
        <onyks-button background="green" slot="footer" @click="model.handle_ok" :disabled="model.is_loading" size="m">OK</onyks-button>
    </onyks-dialog>
</template>

<style lang="css" scoped>
    onyks-text:empty::before 
    {
        content: "\00A0";
    }
</style>