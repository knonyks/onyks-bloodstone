<script setup lang="js">
    import { ref } from 'vue';

    const uploader = ref(null);
    let resetting = false;

    const datasheets = defineModel('datasheets', 
    {
        type: Object,
        default: () => (
            [

            ]
        )
    });

    const files = defineModel('files', 
    {
        type: Array,
        default: () => ([])
    });

    const change = (event) => 
    {
        if (resetting) return;
        const newFiles = event.detail?.files ?? [];
        if (!newFiles.length) return;

        datasheets.value = [...datasheets.value, ...newFiles.map(file => ({ name: file.name.replace('.pdf', '') }))]
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
        <onyks-container gap="m" style="height: 100%; overflow-y: auto; box-sizing: border-box;">
            <onyks-panel v-for="(item, index) in datasheets" :key="index" class="sub-panel">
                <onyks-container gap="m" type="stack">
                    <onyks-tag background="blue" v-if="item.uuid">Already uploaded</onyks-tag>
                    <onyks-tag background="yellow" v-else>Not uploaded yet</onyks-tag>
                    <onyks-container gap="m" type="stack" align="end" @click.stop>
                        <onyks-text>
                            {{ item.name }}
                        </onyks-text>
                        <onyks-textfield style="position: relative; z-index: 10; pointer-events: auto;" :value="item.name ?? ''" @input="updateValue(item.id, $event)"></onyks-textfield>
                        <onyks-container type="group" gap="m">
                            <onyks-tag background="green" v-if="item.uuid">Open</onyks-tag>
                            <onyks-tag background="red" @click="deleteFile(item.id)">Delete</onyks-tag>
                        </onyks-container>
                    </onyks-container>
                </onyks-container>
            </onyks-panel>
        </onyks-container>
    </onyks-panel>

    <onyks-file-upload ref="uploader" size="m" @change="change" multiple message="Add docs, datasheets etc." accept=".pdf"></onyks-file-upload>
</template>

<style scoped>
    .main-panel
    {
        height: 300px;
        width: 100%;
        box-sizing: border-box;
    }

    .sub-panel
    {
        height: fit-content;
        width: 100%;
        box-sizing: border-box;
    }
</style>