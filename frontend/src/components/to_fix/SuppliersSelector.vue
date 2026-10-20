<script setup lang="js">
    import { ref } from 'vue';
    import BasicSearch from './BasicSearch.vue';
    
    const props = defineProps({action: Function})
    const items = ref([])
    const page = ref(1)
    const total = ref(0)
    const counter = ref(0)
    const query = ref('')
    const model = defineModel({ default: () => ({}) })
    
    const init = async () => 
    {
        let data = await props.action(1, 50)
        items.value = data.data.items
        total.value = data.data.total
        counter.value = items.value.length
        page.value = 1
    }

    const nextPage = async () => 
    {
        let data = await props.action(page.value + 1, 50, query.value)
        items.value = items.value.concat(data.data.items)
        total.value = data.data.total
        counter.value = items.value.length
        page.value++
    }

    const search = async () =>
    {
        let data = await props.action(1, 50, query.value)
        items.value = data.data.items
        total.value = data.data.total
        counter.value = items.value.length
        page.value = 1
    }

    defineExpose({init})
</script>

<template>
    <onyks-container type="stack" gap="m" style="width: 100%;">
        <BasicSearch v-model="query" :search="search"></BasicSearch>
        <onyks-select ref="select" @scroll-end="nextPage">
            <onyks-select-option :selected="value.name == model" v-for="value in items" :key="value" :value="value.id">
                <onyks-container gap="m">
                    <onyks-header level="6">{{ value.name }}</onyks-header>
                    <onyks-textfield v-model="model[String(value.id)]" style="position: relative; z-index: 10; pointer-events: auto;"></onyks-textfield>
                </onyks-container>
            </onyks-select-option>
        </onyks-select>

        <onyks-text>Total:&emsp;{{counter}}&emsp;/&emsp;{{ total }}</onyks-text>
    </onyks-container>
</template>

<style lang="css" scoped>
    onyks-button
    {
        width: 100%;
    }
</style>