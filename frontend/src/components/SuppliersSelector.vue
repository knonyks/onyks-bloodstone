<script setup lang="js">
    import BasicSearch from './BasicSearch.vue';

    const model = defineModel()
    const value = defineModel('value', {
        type: Object,
        default: () => ({})
    })

    function update_value(id, event) 
    {
        const nextValue = event.detail?.value ?? event.target?.value ?? event.detail ?? ''
        value.value = {
            ...value.value,
            [String(id)]: {
                value: nextValue
            }
        }
    }
</script>

<template>
    <BasicSearch v-model="model.search_phrase" :search="model.search"></BasicSearch>
    <onyks-select v-model="model.items" @scroll-end="model.handle_scroll_end" @change="model.handle_change($event.detail)">
        <onyks-select-option  v-for="item in model.items" :key="item.id" :value="item" :selected="item.name === value">
            
            <onyks-container gap="m">
                <onyks-text>{{ item.name }}</onyks-text>
                <onyks-textfield :value="value?.[String(item.id)]?.['value'] ?? ''" @input="update_value(item.id, $event)" style="position: relative; z-index: 10; pointer-events: auto;"></onyks-textfield>
            </onyks-container>

        </onyks-select-option>
    </onyks-select>
    <onyks-text>{{ $t('common.total') }}:&emsp;{{ model.items.length }}&emsp;/&emsp;{{ model.total }}</onyks-text>
</template>

<style>
    onyks-select
    {
        height: 300px;
        width: 100%;
    }
</style>