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
  
    <ManagerPage :title="$t('views.DashboardView.title')">
        <onyks-header level="3">{{ $t('views.DashboardView.overview') }}</onyks-header>

        <onyks-container gap="m" type="grid" mobile-breakpoint="700" cols="4" rows="1">

            <onyks-card :title="$t('views.DashboardView.lastAddedElement')" size="l" class="card" cols="2">

                <onyks-container gap="m" cols="2" rows="4" type="grid" mobile-breakpoint="900" style="grid-template-columns: 125px auto;">

                    <onyks-header level="6" cols="1">{{ $t('views.DashboardView.partName') }}</onyks-header>
                    <onyks-text size="m" cols="1">{{ data.elements?.lastAdded?.partName || $t('DashboardView.none') }}</onyks-text>

                    <onyks-header level="6" cols="1">{{ $t('views.DashboardView.manufacturer') }}</onyks-header>
                    <onyks-text size="m" cols="1">{{data.elements?.lastAdded?.manufacturer || $t('DashboardView.none')}}</onyks-text>

                    <onyks-header level="6" cols="1">{{ $t('views.DashboardView.table') }}</onyks-header>
                    <onyks-text size="m" cols="1">{{data.elements?.lastAdded?.table || $t('DashboardView.none')}}</onyks-text>

                    <onyks-header level="6" cols="1">{{ $t('views.DashboardView.createdAt') }}</onyks-header>
                    <onyks-text size="m" cols="1">{{ data.elements?.lastAdded?.createdAt ? $d(new Date(data.elements.lastAdded.createdAt), 'long') : $t('DashboardView.none') }}</onyks-text>

                </onyks-container>
            </onyks-card>

            <onyks-card :title="$t('views.DashboardView.repository')" size="l" class="card" cols="2">
                <onyks-container gap="m" cols="10" rows="4" type="grid" mobile-breakpoint="900" style="grid-template-columns: 250px auto;">

                    <onyks-header level="6" cols="1">{{ $t('views.DashboardView.symbolsFiles') }} (*.SchLib)</onyks-header>
                    <onyks-text size="m" cols="1">{{ data.repository?.schlib_count || 0 }}</onyks-text>

                    <onyks-header level="6" cols="1">{{ $t('views.DashboardView.footprintsFiles') }} (*.PcbLib)</onyks-header>
                    <onyks-text size="m" cols="1">{{data.repository?.pcblib_count || 0}}</onyks-text>

                    <onyks-header level="6" cols="1">{{ $t('views.DashboardView.symbols') }}</onyks-header>
                    <onyks-text size="m" cols="1">{{data.repository?.symbols_count || 0}}</onyks-text>

                    <onyks-header level="6" cols="1">{{ $t('views.DashboardView.footprints') }}</onyks-header>
                    <onyks-text size="m" cols="1">{{data.repository?.footprints_count || 0}}</onyks-text>

                </onyks-container>
            </onyks-card>

        </onyks-container>

        <onyks-container cols="4" rows="1" type="grid" gap="m" mobile-breakpoint="950">

            <onyks-card :title="$t('views.DashboardView.elements')" cols="1" size="l">
                <onyks-header level="3">{{ data?.elements?.count || 0 }}</onyks-header>
            </onyks-card>

            <onyks-card :title="$t('views.DashboardView.tables')" cols="1" size="l">
                <onyks-header level="3">{{ data?.tables?.count || 0 }}</onyks-header>
            </onyks-card>

            <onyks-card :title="$t('views.DashboardView.manufacturers')" cols="1" size="l">
                <onyks-header level="3">{{ data?.manufacturers?.count || 0 }}</onyks-header>
            </onyks-card>

            <onyks-card :title="$t('views.DashboardView.suppliers')" cols="1" size="l">
                <onyks-header level="3">{{ data?.suppliers?.count || 0 }}</onyks-header>
            </onyks-card>
        </onyks-container>

        <onyks-header level="3">{{ $t('views.DashboardView.tables') }}</onyks-header>

        <onyks-container type="grid" cols="6" v-if="Object.keys(data.tables.counts || {}).length > 0"  gap="m" mobile-breakpoint="800">
            <onyks-card v-for="(number, name) in data.tables.counts" :key="name" :title="name" size="l" cols="2">
                <onyks-header level="2">{{ number }}</onyks-header>
            </onyks-card>
        </onyks-container>

        <onyks-text v-else>{{ $t('views.DashboardView.noTables') }}</onyks-text>

        <onyks-header level="3">{{ $t('views.DashboardView.manufacturers') }}</onyks-header>
        
        <onyks-container type="grid" cols="6" v-if="Object.keys(data.manufacturers.counts || {}).length > 0" gap="m" mobile-breakpoint="800">
            <onyks-card v-for="(number, name) in data.manufacturers.counts" :title="name" cols="2" size="l">
                <onyks-header level="2">{{ number }}</onyks-header>
            </onyks-card>
        </onyks-container>

        <onyks-text v-else>{{ $t('views.DashboardView.noManufacturers') }}</onyks-text>

    </ManagerPage>

</template>