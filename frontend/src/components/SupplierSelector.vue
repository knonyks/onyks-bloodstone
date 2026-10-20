<script setup lang="js">
    import BasicSearch from './BasicSearch.vue';

    const model = defineModel()
    const value = defineModel('value', {
        type: Object,
        default: () => ({})
    })

    function updateValue(id, event) {
        const nextValue = event.detail?.value ?? event.target?.value ?? event.detail ?? ''
        value.value = {
            ...value.value,
            [String(id)]: nextValue
        }
    }
</script>

<template>
    <BasicSearch v-model="model.searchPhrase" :search="model.search"></BasicSearch>
    <onyks-select v-model="model.items" @scroll-end="model.handleScrollEnd" @change="model.handleChange($event.detail)">
        <onyks-select-option  v-for="item in model.items" :key="item.id" :value="item" :selected="item.name === value">
            
            <onyks-container gap="m">
                <onyks-text>{{ item.name }}</onyks-text>
                <onyks-textfield :value="value[String(item.id)] ?? ''" @input="updateValue(item.id, $event)" style="position: relative; z-index: 10; pointer-events: auto;"></onyks-textfield>
            </onyks-container>

        </onyks-select-option>
    </onyks-select>
    <onyks-text>Total:&emsp;{{ model.items.length }}&emsp;/&emsp;{{ model.total }}</onyks-text>
</template>

<style>
    onyks-select
    {
        height: 300px;
        width: 100%;
    }
</style>