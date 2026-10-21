<script setup lang="js">
    import { ref } from 'vue';
    const tags = defineModel('tags', {default: []});
    const model = defineModel({default: []});
</script>



<template>
    <onyks-panel>
        <onyks-container gap="m" type="group">
            <onyks-tag closable v-for="tag in tags" :key="tag" @close="tags.splice(tags.indexOf(tag), 1)">{{ tag }}</onyks-tag>
        </onyks-container>
    </onyks-panel>

    <onyks-textfield @option-selected="model.select" @input="model.search" id="country" dropdown @keydown="model.keydownHandler" :options="model.options" v-model="model.text"></onyks-textfield>

</template>


<style lang="css" scoped>
    onyks-panel
    {
        height: fit-content;
        width: 100%;
        box-sizing: border-box;
    }
</style>