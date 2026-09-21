<script setup lang="js">
    import { ref } from 'vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import { onMounted } from 'vue';
    import { services } from '@/utils/api';
    import DataLoader from '@/components/DataLoader.vue';
    import { useWindowSize } from '@vueuse/core';
    import { MyError, MyTime } from '@/utils/tools';
    import { MyLoaderState } from '@/utils/tools';

    const {width} = useWindowSize()
    const loading = ref(new MyLoaderState())
 
    const data = ref(
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
            loading.value.state += 100/8
            data.value.elements = (await services.elements.count()).data
            loading.value.state += 100/8
            data.value.elements.lastAdded = (await services.elements.lastAdded()).data
            data.value.elements.lastAdded.createdAt = MyTime.getLocalTime(data.value.elements.lastAdded.createdAt, 'en')
            loading.value.state += 100/8
            data.value.tables = (await services.tables.count()).data
            loading.value.state += 100/8
            data.value.tables.counts = (await services.tables.counts()).data
            loading.value.state += 100/8
            data.value.suppliers = (await services.suppliers.count()).data
            loading.value.state += 100/8
            data.value.manufacturers = (await services.manufacturers.count()).data
            loading.value.state += 100/8
            data.value.repository = (await services.repository.statistics()).data
            loading.value.state = 100
            data.value.manufacturers.counts = (await services.manufacturers.counts()).data
            loading.value.isLoading = false
        }
        catch (err)
        {
            loading.value.error = MyError.process(err)
            loading.value.isLoading = false
        }
    })
</script>

<template>
    <DataLoader v-model="loading">

        <ManagerPage title="Dashboard">
            <onyks-header level="3">Overview</onyks-header>
   
            <onyks-container gap="m" type="grid" mobile-breakpoint="600" cols="4" rows="1">

                <onyks-card title="Last added element" size="l" class="card" cols="2">

                    <onyks-container gap="m" cols="10" rows="4" type="grid" mobile-breakpoint="900">

                        <onyks-header level="6" cols="3">Part name</onyks-header>
                        <onyks-text size="l" cols="7">{{ data.elements?.lastAdded?.partName || 'Undefined' }}</onyks-text>

                        <onyks-header level="6" cols="3">Manufacturer</onyks-header>
                        <onyks-text size="l" cols="7">{{data.elements?.lastAdded?.manufacturer || 'Undefined'}}</onyks-text>

                        <onyks-header level="6" cols="3">Table</onyks-header>
                        <onyks-text size="l" cols="7">{{data.elements?.lastAdded?.table || 'Undefined'}}</onyks-text>

                        <onyks-header level="6" cols="3">Created At</onyks-header>
                        <onyks-text size="l" cols="7">{{data.elements?.lastAdded?.createdAt || 'Undefined'}}</onyks-text>

                    </onyks-container>
                </onyks-card>

                <onyks-card title="Repository" size="l" class="card" cols="2">
                    <onyks-container gap="m" cols="10" rows="4" type="grid" mobile-breakpoint="900">

                        <onyks-header level="6" cols="6">Symbols files (*.SchLib)</onyks-header>
                        <onyks-text size="l" cols="4">{{ data.repository?.schlib_count || 'Undefined' }}</onyks-text>

                        <onyks-header level="6" cols="6">Footprints files (*.PcbLib)</onyks-header>
                        <onyks-text size="l" cols="4">{{data.repository?.pcblib_count || 'Undefined'}}</onyks-text>

                        <onyks-header level="6" cols="6">Symbols</onyks-header>
                        <onyks-text size="l" cols="4">{{data.repository?.symbols_count || 'Undefined'}}</onyks-text>

                        <onyks-header level="6" cols="6">Footprints</onyks-header>
                        <onyks-text size="l" cols="4">{{data.repository?.footprints_count || 'Undefined'}}</onyks-text>

                    </onyks-container>
                </onyks-card>

            </onyks-container>

            <onyks-container cols="4" rows="1" type="grid" gap="m" mobile-breakpoint="950">

                <onyks-card title="Elements" cols="1" size="l">
                    <onyks-header level="3">{{ data?.elements?.count || 'Undefined' }}</onyks-header>
                </onyks-card>

                <onyks-card title="Tables" cols="1" size="l">
                    <onyks-header level="3">{{ data?.tables?.count || 'Undefined' }}</onyks-header>
                </onyks-card>

                <onyks-card title="Manufacturers" cols="1" size="l">
                    <onyks-header level="3">{{ data?.manufacturers?.count || 'Undefined' }}</onyks-header>
                </onyks-card>

                <onyks-card title="Suppliers" cols="1" size="l">
                    <onyks-header level="3">{{ data?.suppliers?.count || 'Undefined' }}</onyks-header>
                </onyks-card>
            </onyks-container>

            <onyks-header level="3">Tables</onyks-header>

            <onyks-container type="grid" cols="6" v-if="Object.keys(data.tables.counts || {}).length > 0"  gap="m" mobile-breakpoint="800">
                <onyks-card v-for="(number, name) in data.tables.counts" :key="name" :title="name" size="l" cols="2">
                    <onyks-header level="2">{{ number }}</onyks-header>
                </onyks-card>
            </onyks-container>

            <onyks-text v-else>There is no tables to show.</onyks-text>

            <onyks-header level="3">Manufacturers</onyks-header>
            
            <onyks-container type="grid" cols="6" v-if="Object.keys(data.manufacturers.counts || {}).length > 0" gap="m" mobile-breakpoint="800">
                <onyks-card v-for="(number, name) in data.manufacturers.counts" :title="name" cols="2" size="l">
                    <onyks-header level="2">{{ number }}</onyks-header>
                </onyks-card>
            </onyks-container>

            <onyks-text v-else>There is no manufacturers to show.</onyks-text>

        </ManagerPage>
    </DataLoader>
</template>

<style scoped>

</style>