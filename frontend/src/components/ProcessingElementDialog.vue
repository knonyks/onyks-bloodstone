<script setup>
    defineProps({
        message: String,
        open: Boolean
    });
</script>

<template>
    <onyks-dialog :open="open" no-title>
        <onyks-text>{{ message }}</onyks-text>
    </onyks-dialog>
</template>