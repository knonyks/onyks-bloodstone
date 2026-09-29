<script setup>
    import BasicSearch from '@/components/BasicSearch.vue';
    import BasicTable from '@/components/BasicTable.vue';
    import ManagerPage from '@/components/ManagerPage.vue'
    import { useLoaderStore } from '@/stores/loader';
    import { services } from '@/utils/api';
    import { onMounted, ref } from 'vue';
    import { MyTable } from '@/utils/tools';

    const loaderStore = useLoaderStore();

    const elementsModel = ref(new MyTable(services.elements.list, 'uuid',
    [
        {
            "key": "selected",
            "label": "Select"
        },
        {
            'key': 'uuid',
            'label': 'UUID'
        },
        {
            'key': 'partName',
            'label': 'Part Name'
        },
        {
            'key': 'manufacturer',
            'label': 'Manufacturer'
        },
        {
            'key': 'table',
            'label': 'Table'
        },
        {
            'key': 'description',
            'label': 'Description'
        },
        {
            'key': 'availability',
            'label': 'Availability'
        },
        {
            'key': 'value',
            'label': 'Value'
        },
        {
            'key': 'sub_suppliers',
            'label': 'Suppliers Names'
        }
    ], async (e) => 
    {
        e.selected = false;
        e.sub_suppliers = ''
        for(const supplier in e.suppliers)
        {
            e.sub_suppliers += e.suppliers[supplier] + ', ';
        }
        e.sub_suppliers = e.sub_suppliers.slice(0, -2);
        return e
    }))

    const tablesModel = ref(new MyTable(services.tables.list, 'id',
    [
        {
            "key": "selected",
            "label": "Select"
        },
        {
            'key': 'id',
            'label': 'ID'
        },
        {
            "key": "name",
            "label": "Name"
        },
        {
            "key": "createdAt",
            "label": "Created At"
        },
    ], (e) => {e.selected = false; return e}))

    const manufacturersModel = ref(new MyTable(services.manufacturers.list, 'id',
    [
        {
            "key": "selected",
            "label": "Select"
        },
        {
            'key': 'id',
            'label': 'ID'
        },
        {
            "key": "name",
            "label": "Name"
        },
        {
            "key": "createdAt",
            "label": "Created At"
        },
    ], (e) => {e.selected = false; return e}))

    const suppliersModel = ref(new MyTable(services.suppliers.list, 'id',
    [
        {
            "key": "selected",
            "label": "Select"
        },
        {
            'key': 'id',
            'label': 'ID'
        },
        {
            "key": "name",
            "label": "Name"
        },
        {
            "key": "createdAt",
            "label": "Created At"
        },
    ], (e) => {e.selected = false; return e}))

    onMounted(async () => 
    {
        await elementsModel.value.init();
        await tablesModel.value.init();
        await manufacturersModel.value.init();
        await suppliersModel.value.init();

        loaderStore.hide()
        loaderStore.globalHide()
    });
</script>

<template>
    <ManagerPage title="Management">
        <onyks-header level=3>Elements</onyks-header>
        <BasicSearch v-model="elementsModel.data.search" @search="() => {elementsModel.search()}"></BasicSearch>
        <BasicTable v-model="elementsModel"></BasicTable>
        <onyks-header level=3>Tables</onyks-header>
        <BasicSearch v-model="tablesModel.data.search" @search="() => {tablesModel.search()}"></BasicSearch>
        <BasicTable v-model="tablesModel"></BasicTable>
        <onyks-header level=3>Manufacturers</onyks-header>
        <BasicSearch v-model="manufacturersModel.data.search" @search="() => {manufacturersModel.search()}"></BasicSearch>
        <BasicTable v-model="manufacturersModel"></BasicTable>
        <onyks-header level=3>Suppliers</onyks-header>
        <BasicSearch v-model="suppliersModel.data.search" @search="() => {suppliersModel.search()}"></BasicSearch>
        <BasicTable v-model="suppliersModel"></BasicTable>
    </ManagerPage>
</template>

<style lang="css">

</style>