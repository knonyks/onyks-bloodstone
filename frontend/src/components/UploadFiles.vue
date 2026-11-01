<script setup lang="js">
    import { ref } from 'vue';

    const files = defineModel('files', {default: []});
    const datasheets = defineModel('datasheets', {default: []});
    const datasheets_old_names = ref([])

    const uploader = ref(null);
    let resetting = false;

    const handle_change = (event) => 
    {
        if (resetting) return;
        const newFiles = event.detail?.files ?? [];
        if (!newFiles.length) return;

        datasheets.value = [...datasheets.value, ...newFiles.map(file => {
            const name = file.name.replace('.pdf', '');
            datasheets_old_names.value.push(file.name);
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

    const open_file = (uuid) =>
    {
        window.open('/files/' + uuid + '.pdf', '_blank');
    };

    const delete_file = (index) => 
    {
        if (index !== -1)
        {
            datasheets_old_names.value.splice(index, 1);
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
                    <onyks-tag background="blue" v-if="item.uuid">{{ $t('elements.already_uploaded') }}</onyks-tag>
                    <onyks-tag background="yellow" v-else>{{ $t('elements.not_uploaded_yet') }}</onyks-tag>
                    <onyks-text>{{index + 1}}: {{ datasheets_old_names[index] }}</onyks-text>
                    <onyks-textfield v-model="item.name"></onyks-textfield>
                    <onyks-container align="end" type="group" gap="m" style="width: 100%;">
                        <onyks-tag icon="F756" background="green" v-if="item.uuid" @click="open_file(item.uuid)">{{ $t('common.open') }}</onyks-tag>
                        <onyks-tag icon="F78B" background="red" @click="delete_file(index)">{{ $t('common.remove') }}</onyks-tag>
                    </onyks-container>
                </onyks-container>
            </onyks-panel>
        </onyks-container>
    </onyks-panel>
    <onyks-file-upload ref="uploader" @change="handle_change" size="m" multiple :message="$t('elements.add_datasheets')" accept=".pdf"></onyks-file-upload>
</template>

<style scoped>
    .main-panel
    {
        width: 100%;
        height: 300px;
        min-height: 300px;
        flex-shrink: 0;
        box-sizing: border-box;
        overflow-y: auto;
    }

    .sub-container
    {
        width: 100%;
        box-sizing: border-box;
        height: 100%;
    }

    .sub-panel
    {
        width: calc(100%);
        height: fit-content;
        flex-shrink: 0;
        box-sizing: border-box;
    }
</style>