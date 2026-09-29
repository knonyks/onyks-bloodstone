<script setup lang="js">
    import { ref } from 'vue';
    import BasicSearch from './BasicSearch.vue';
    
    const props = defineProps({action: Function})
    const items = ref([])
    const page = ref(1)
    const total = ref(0)
    const counter = ref(0)
    const query = ref('')
    const model = defineModel()
    
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

    const changeValue = (e) =>
    {
        if(e.detail.selected)
        {
            model.value = e.detail.value
            // model.value.id = e.detail.value[0]
        }
        else
        {
            model.value = ''
        }
    }

    defineExpose({init})
</script>

<template>
    <onyks-container type="stack" gap="m" style="width: 100%;">
        <BasicSearch v-model="query" :search="search"></BasicSearch>
        <onyks-select ref="select" @scroll-end="nextPage" @change="changeValue">
            <onyks-select-option :selected="value.name == model" v-for="value in items" :key="value" :value="value.name">{{ value.name }}</onyks-select-option>
        </onyks-select>

        <onyks-text>Total:&emsp;{{counter}}&emsp;/&emsp;{{ total }}</onyks-text>


        <!-- <onyks-container type="grid" cols="3" padding="" gap="m">
            <onyks-button background="green" @click="emit('add-click')">Add</onyks-button>
            <onyks-button background="blue" @click="emit('edit-click')" :ref="(el) => { if (el) btns.edit = el }" disabled>Edit</onyks-button>
            <onyks-button @click="emit('delete-click')" :ref="(el) => { if (el) btns.delete = el }" disabled>Delete</onyks-button>
        </onyks-container> -->
    </onyks-container>
</template>

<style lang="css" scoped>
    onyks-button
    {
        width: 100%;
    }

    onyks-select
    {
        width: 100%;
        height: 300px;
    }
</style>