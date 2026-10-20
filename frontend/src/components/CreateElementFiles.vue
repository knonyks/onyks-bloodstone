<script setup>
    import { ref } from 'vue';
    const files = ref([]);
    const y = ref(null);

    const handleChange = (event) => 
    {
        files.value = event.target.files;
    };

    const handleClose = (file) => 
    {
        files.value = Array.from(files.value).filter(f => f.name !== file.name);
    };
</script>
    
<template>
    <onyks-container type="group" cols="10" gap="m">
        <onyks-panel cols="6">
            <onyks-container type="group" gap="m">
                <onyks-tag v-for="file in files" :key="file.name" icon="F756" background="accent" closable @close="handleClose(file)">{{ file.name }}</onyks-tag>
            </onyks-container>
        </onyks-panel>
        <onyks-file-upload cols="4" ref="y" size="m" @change="handleChange" multiple message="Add docs, datasheets etc." accept=".pdf"></onyks-file-upload>
    </onyks-container>
</template>

<style scoped>
    onyks-panel, onyks-file-upload
    {
        width: 100%;
        box-sizing: border-box;
        height: fit-content;
    }

    onyks-tag
    {
        box-sizing: border-box;
        height: fit-content;
    }
</style>