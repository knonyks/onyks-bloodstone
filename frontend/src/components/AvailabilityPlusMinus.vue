<script setup>
    const model = defineModel(
    {
        type: Number,
        default: 0
    })
</script>

<template>
    <onyks-container type="group" gap="s" justify="center" align="center" style="width: fit-content; height: fit-content;">
        <onyks-tag @click="() => model--" background="red" icon="F63B" style="gap: 0; height: 100%; box-sizing: border-box;"></onyks-tag>
        <onyks-textfield min="0" v-model="model" type="number" style="max-width: 100px;"></onyks-textfield>
        <onyks-tag @click="() => model++" size="m" icon="F64D" style="gap: 0; height: 100%; box-sizing: border-box;"></onyks-tag>
        <onyks-tag background="blue" icon="" style="width: fit-content; height: fit-content; box-sizing: border-box;">Save</onyks-tag>
        <onyks-tag background="red" icon="" style="width: fit-content; height: fit-content; box-sizing: border-box;">Reset</onyks-tag>
    </onyks-container>
</template>