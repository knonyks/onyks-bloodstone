<script setup lang="js">
    defineProps(['text', 'type', 'show'])
</script>

<template>
    <div class="alert-wrapper" :class="{ 'alert-hidden': !show }">
        <div class="alert-content">
            <onyks-alert :type="type" size="m">{{ text }}</onyks-alert>
        </div>
    </div>
</template>


<style scoped>
    .alert-wrapper 
    {
        display: grid;
        grid-template-rows: 1fr;
        overflow: hidden;
        transition: grid-template-rows 250ms ease;
    }

    .alert-wrapper.alert-hidden 
    {
        grid-template-rows: 0fr;
    }

    .alert-content 
    {
        min-height: 0;
        overflow: hidden;
    }

</style>