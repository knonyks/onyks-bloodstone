<script setup lang="js">
    import BasicSearch from './BasicSearch.vue';

    const model = defineModel()
    const value = defineModel('value')
</script>

<template>
    <onyks-text>{{ $t('elements.selected') }}: {{ value || $t('elements.none') }}</onyks-text>
    <BasicSearch v-model="model.search_phrase" :search="model.search"></BasicSearch>
    <onyks-select v-model="model.items" @scroll-end="model.handle_scroll_end" @change="model.handle_change($event.detail)">
        <onyks-select-option  v-for="item in model.items" :key="item.id" :value="item" :selected="item.name === value">{{ item.name }}</onyks-select-option>
    </onyks-select>
    <onyks-text>{{ $t('common.total') }}:&emsp;{{ model.items.length }}&emsp;/&emsp;{{ model.total }}</onyks-text>
</template>