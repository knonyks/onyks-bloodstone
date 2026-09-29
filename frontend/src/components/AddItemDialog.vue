<script setup>
    import { defineModel } from 'vue';
    import { ref } from 'vue';

    const model = defineModel()
    const dialog = ref(null)

    const open = () => 
    {
        model.value.name = ''
        model.value.error = ''
        dialog.value.open = true
    }

    const close = () =>
    {
        dialog.value.open = false
    }

    defineExpose(
    {
        open,
        close
    });
</script>

<template>
    <onyks-dialog :title="`Add a ${model.subject}`" corner-close bottom-buttons modal ref="dialog">
        <onyks-container gap="m" type="stack">
            <onyks-text>Enter a name of a new {{ model.subject }} below:</onyks-text>
            <onyks-textfield :placeholder="`${model.placeholder}`" v-model="model.name" @input="model.error = ''"></onyks-textfield>
            <onyks-text :class="model.error === '' ? 'error-invisible' : ''">{{ model.error }}</onyks-text>
        </onyks-container>
        <onyks-button background="green" slot="footer" @click="model.add" size="m">OK</onyks-button>
        <onyks-button background="red" slot="footer" @click="dialog.open = false">Close</onyks-button>
    </onyks-dialog>
</template>

<style lang="css" scoped>

</style>