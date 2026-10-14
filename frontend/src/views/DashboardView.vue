<script setup lang="js">
    import { reactive } from 'vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import { onMounted } from 'vue';
    import { services } from '@/utils/api';
    import { useLoaderStore } from '@/stores/loader';

    const loaderStore = useLoaderStore()

    const data = reactive(
    {
        elements: {},
        tables: {},
        suppliers: {},
        manufacturers: {},
        repository: {}
    })

    onMounted(async () =>
    {
        try
        {
            data.elements = (await services.elements.count()).data

            try
            {
                data.elements.lastAdded = (await services.elements.lastAdded()).data
            }
            catch(e)
            {
                console.dir(e)
            }

            data.tables = (await services.tables.count()).data
            data.tables.counts = (await services.tables.counts()).data
            data.suppliers = (await services.suppliers.count()).data
            data.manufacturers = (await services.manufacturers.count()).data
            data.repository = (await services.repository.statistics()).data
            data.manufacturers.counts = (await services.manufacturers.counts()).data
            loaderStore.hide()
            loaderStore.globalHide()
        }
        catch (err)
        {
            console.dir(err)
        }
    })
</script>

<template>
  
    <ManagerPage title="Dashboard">
        <onyks-header level="3">Overview</onyks-header>

        <onyks-container gap="m" type="grid" mobile-breakpoint="600" cols="4" rows="1">

            <onyks-card title="Last added element" size="l" class="card" cols="2">

                <onyks-container gap="m" cols="10" rows="4" type="grid" mobile-breakpoint="900">

                    <onyks-header level="6" cols="3">Part name</onyks-header>
                    <onyks-text size="l" cols="7">{{ data.elements?.lastAdded?.partName || 'None' }}</onyks-text>

                    <onyks-header level="6" cols="3">Manufacturer</onyks-header>
                    <onyks-text size="l" cols="7">{{data.elements?.lastAdded?.manufacturer || 'None'}}</onyks-text>

                    <onyks-header level="6" cols="3">Table</onyks-header>
                    <onyks-text size="l" cols="7">{{data.elements?.lastAdded?.table || 'None'}}</onyks-text>

                    <onyks-header level="6" cols="3">Created At</onyks-header>
                    <onyks-text size="l" cols="7">{{data.elements?.lastAdded?.createdAt || 'None'}}</onyks-text>

                </onyks-container>
            </onyks-card>

            <onyks-card title="Repository" size="l" class="card" cols="2">
                <onyks-container gap="m" cols="10" rows="4" type="grid" mobile-breakpoint="900">

                    <onyks-header level="6" cols="6">Symbols files (*.SchLib)</onyks-header>
                    <onyks-text size="l" cols="4">{{ data.repository?.schlib_count || 0 }}</onyks-text>

                    <onyks-header level="6" cols="6">Footprints files (*.PcbLib)</onyks-header>
                    <onyks-text size="l" cols="4">{{data.repository?.pcblib_count || 0}}</onyks-text>

                    <onyks-header level="6" cols="6">Symbols</onyks-header>
                    <onyks-text size="l" cols="4">{{data.repository?.symbols_count || 0}}</onyks-text>

                    <onyks-header level="6" cols="6">Footprints</onyks-header>
                    <onyks-text size="l" cols="4">{{data.repository?.footprints_count || 0}}</onyks-text>

                </onyks-container>
            </onyks-card>

        </onyks-container>

        <onyks-container cols="4" rows="1" type="grid" gap="m" mobile-breakpoint="950">

            <onyks-card title="Elements" cols="1" size="l">
                <onyks-header level="3">{{ data?.elements?.count || 0 }}</onyks-header>
            </onyks-card>

            <onyks-card title="Tables" cols="1" size="l">
                <onyks-header level="3">{{ data?.tables?.count || 0 }}</onyks-header>
            </onyks-card>

            <onyks-card title="Manufacturers" cols="1" size="l">
                <onyks-header level="3">{{ data?.manufacturers?.count || 0 }}</onyks-header>
            </onyks-card>

            <onyks-card title="Suppliers" cols="1" size="l">
                <onyks-header level="3">{{ data?.suppliers?.count || 0 }}</onyks-header>
            </onyks-card>
        </onyks-container>

        <onyks-header level="3">Tables</onyks-header>

        <onyks-container type="grid" cols="6" v-if="Object.keys(data.tables.counts || {}).length > 0"  gap="m" mobile-breakpoint="800">
            <onyks-card v-for="(number, name) in data.tables.counts" :key="name" :title="name" size="l" cols="2">
                <onyks-header level="2">{{ number }}</onyks-header>
            </onyks-card>
        </onyks-container>

        <onyks-text v-else>There are no tables to show.</onyks-text>

        <onyks-header level="3">Manufacturers</onyks-header>
        
        <onyks-container type="grid" cols="6" v-if="Object.keys(data.manufacturers.counts || {}).length > 0" gap="m" mobile-breakpoint="800">
            <onyks-card v-for="(number, name) in data.manufacturers.counts" :title="name" cols="2" size="l">
                <onyks-header level="2">{{ number }}</onyks-header>
            </onyks-card>
        </onyks-container>

        <onyks-text v-else>There are no manufacturers to show.</onyks-text>

    </ManagerPage>

</template>