<script setup lang="js">
    import { ref } from 'vue';

    const files = defineModel('files', {default: []});
    const datasheets = defineModel('datasheets', {default: []});
    const uploader = ref(null);
    let resetting = false;

    const handleChange = (event) => 
    {
        if (resetting) return;
        const newFiles = event.detail?.files ?? [];
        if (!newFiles.length) return;

        datasheets.value = [...datasheets.value, ...newFiles.map(file => {
            const name = file.name.replace('.pdf', '');
            return { name };
        })]
        files.value = [...files.value, ...newFiles]

        resetting = true;
        try
        {
            uploader.value.reset();
        }
        finally
        {
            resetting = false;
        }
    };

    const openFile = (uuid) =>
    {
        window.open('/files/' + uuid + '.pdf', '_blank');
    };

    const deleteFile = (id) => 
    {
        const index = datasheets.value.findIndex(item => item.id === id);
        if (index !== -1)
        {
            datasheets.value.splice(index, 1);
            files.value.splice(index, 1);
        }
    };
</script>

<template>
    <onyks-panel class="main-panel">
        <onyks-container gap="m" class="sub-container" >
            <onyks-panel class="sub-panel" v-for="(item, index) in datasheets" :key="index">
                <onyks-container gap="m" type="stack">
                    <onyks-tag background="blue" v-if="item.uuid">Already uploaded</onyks-tag>
                    <onyks-tag background="yellow" v-else>Not uploaded yet</onyks-tag>
                    <onyks-textfield v-model="item.name"></onyks-textfield>
                    <onyks-container align="end" type="group" gap="m" style="width: 100%;">
                        
                        <onyks-tag background="green" v-if="item.uuid" @click="openFile(item.uuid)">Open</onyks-tag>
                        <onyks-tag background="red" @click="deleteFile(item.id)">Delete</onyks-tag>
                    </onyks-container>
                </onyks-container>
            </onyks-panel>
        </onyks-container>
    </onyks-panel>
    <onyks-file-upload ref="uploader" @change="handleChange" size="m" multiple message="Add datasheets etc." accept=".pdf"></onyks-file-upload>
</template>

<style scoped>
    .main-panel
    {
        width: 100%;
        height: 300px;
        box-sizing: border-box;
        overflow-y: hidden;
    }

    .sub-container
    {
        width: 100%;
        box-sizing: border-box;
        overflow-y: auto;
        height: 100%;
    }

    .sub-panel
    {
        width: calc(100%);
        height: fit-content;
        flex-shrink: 0;
        box-sizing: border-box;
        /* margin-right: var(--onyks-spacing-md); */
    }
</style>