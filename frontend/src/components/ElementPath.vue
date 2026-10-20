<script setup lang="js">
    import { computed } from 'vue';
    const props = defineProps({
        path: {
            type: String,
            default: ''
        },
        obj: {
            type: String,
            default: ''
        },
        disabled: {
            type: Boolean,
            default: true
        }
    });

    const convertedContent = computed(() => 
    {
        let result = []
        if(props.path != '')
            result = result.concat(props.path.split('/'));
        if(props.obj != '')
            result = result.concat(props.obj);

        result = result.filter(item => item !== '');    
        return result;
    });
</script>

<template>
    <onyks-path :content="convertedContent" :disabled="props.disabled"></onyks-path>
</template>

<style scoped>
    onyks-path
    {
        width: 100%;
        max-width: 100%;
    }
</style>