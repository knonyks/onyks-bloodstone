<script setup>
    import { defineModel } from 'vue';
    const text = defineModel('text');
    const emit = defineEmits(['search']);

    function handleInput(event) 
    {
        emit('search', event.target?.value ?? text.value);
    }
</script>

<template>
    <onyks-textfield placeholder="Search..." v-model="text" @input="handleInput"></onyks-textfield>
</template>

<style>
    onyks-textfield
    {
        width: 100%;
    }
</style>