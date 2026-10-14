<script setup lang="js">
    import { computed } from 'vue';
    const props = defineProps(['path', 'obj']);

    const convertedContent = computed(() => 
    {
        let pathArray = props.path.split('/');
        if(props.obj == '')
            return pathArray;
        return pathArray.concat(props.obj);
    });
</script>

<template>
    <onyks-path :content="convertedContent" disabled></onyks-path>
</template>

<style scoped>
    onyks-path
    {
        width: 100%;
        max-width: 100%;
    }
</style>