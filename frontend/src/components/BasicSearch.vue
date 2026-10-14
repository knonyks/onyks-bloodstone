<script setup>
    const model = defineModel()
    const props = defineProps({search: Function})
</script>

<template>
    <onyks-textfield placeholder="Search..." @input="props.search" v-model="model"></onyks-textfield>
</template>

<style>
    onyks-textfield
    {
        width: 100%;
    }
</style>