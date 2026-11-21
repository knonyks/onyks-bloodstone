<script setup lang="js">
    import { reactive } from 'vue';
    import ManagerPage from '../components/ManagerPage.vue';
    import { onMounted } from 'vue';
    import { services } from '../utils/api';
    import { useLoaderStore } from '../stores/loader';
    import SubTitle from '../components/SubTitle.vue';

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
                data.elements.lastAdded = (await services.elements.last_added()).data
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
  
    <ManagerPage :title="$t('common.dashboard')">
        <SubTitle>{{ $t('common.overview') }}</SubTitle>
        <onyks-container gap="m" type="grid" mobile-breakpoint="700" cols="4" rows="1">

            <onyks-card title-size="l" :title="$t('common.last_added_element')" size="l" class="card" subcols="2">

                <onyks-container gap="m" cols="2" rows="4" type="grid" mobile-breakpoint="900" style="grid-template-columns: 125px auto;">

                    <onyks-header size="m" cols="1">{{ $t('elements.part_name') }}</onyks-header>
                    <onyks-text size="m" cols="1">{{ data.elements?.lastAdded?.part_name || $t('common.no_data') }}</onyks-text>

                    <onyks-header size="m" cols="1">{{ $t('elements.manufacturer') }}</onyks-header>
                    <onyks-text size="m" cols="1">{{ data.elements?.lastAdded?.manufacturer || $t('common.no_data') }}</onyks-text>

                    <onyks-header size="m" cols="1">{{ $t('elements.table') }}</onyks-header>
                    <onyks-text size="m" cols="1">{{ data.elements?.lastAdded?.table || $t('common.no_data') }}</onyks-text>

                    <onyks-header size="m" cols="1">{{ $t('common.created_at') }}</onyks-header>
                    <onyks-text size="m" cols="1">{{ data.elements?.lastAdded?.created_at ? $d(new Date(data.elements.lastAdded.created_at), 'long') : $t('common.no_data') }}</onyks-text>

                </onyks-container>
            </onyks-card>

            <onyks-card title-size="l" :title="$t('common.repository')" size="l" class="card" subcols="2">
                <onyks-container gap="m" cols="10" rows="4" type="grid" mobile-breakpoint="900" style="grid-template-columns: 250px auto;">

                    <onyks-header size="m" cols="1">{{ $t('common.symbols_files') }} (*.SchLib)</onyks-header>
                    <onyks-text size="m" cols="1">{{ data.repository?.schlib_count || 0 }}</onyks-text>

                    <onyks-header size="m" cols="1">{{ $t('common.footprints_files') }} (*.PcbLib)</onyks-header>
                    <onyks-text size="m" cols="1">{{data.repository?.pcblib_count || 0}}</onyks-text>

                    <onyks-header size="m" cols="1">{{ $t('common.symbols') }}</onyks-header>
                    <onyks-text size="m" cols="1">{{data.repository?.symbols_count || 0}}</onyks-text>

                    <onyks-header size="m" cols="1">{{ $t('common.footprints') }}</onyks-header>
                    <onyks-text size="m" cols="1">{{data.repository?.footprints_count || 0}}</onyks-text>

                </onyks-container>
            </onyks-card>

        </onyks-container>

        <onyks-container cols="4" rows="1" type="grid" gap="m" mobile-breakpoint="950">

            <onyks-card title-size="l" :title="$t('common.elements')" cols="1" size="l">
                <onyks-text size="xl">{{ data?.elements?.count || 0 }}</onyks-text>
            </onyks-card>

            <onyks-card title-size="l" :title="$t('common.tables')" cols="1" size="l">
                <onyks-text size="xl">{{ data?.tables?.count || 0 }}</onyks-text>
            </onyks-card>

            <onyks-card title-size="l" :title="$t('common.manufacturers')" cols="1" size="l">
                <onyks-text size="xl">{{ data?.manufacturers?.count || 0 }}</onyks-text>
            </onyks-card>

            <onyks-card title-size="l" :title="$t('common.suppliers')" cols="1" size="l">
                <onyks-text size="xl">{{ data?.suppliers?.count || 0 }}</onyks-text>
            </onyks-card>
        </onyks-container>

        <SubTitle>{{ $t('common.tables') }}</SubTitle>

        <onyks-container type="grid" cols="6" v-if="Object.keys(data.tables.counts || {}).length > 0"  gap="m" mobile-breakpoint="800">
            <onyks-card title-size="l" v-for="(number, name) in data.tables.counts" :key="name" :title="name" size="l" subcols="2">
                <onyks-text size="l">{{ number }}</onyks-text>
            </onyks-card>
        </onyks-container>

        <onyks-text v-else>{{ $t('common.no_tables') }}</onyks-text>

        <SubTitle>{{ $t('common.manufacturers') }}</SubTitle>
        
        <onyks-container type="grid" cols="6" v-if="Object.keys(data.manufacturers.counts || {}).length > 0" gap="m" mobile-breakpoint="800">
            <onyks-card title-size="l" v-for="(number, name) in data.manufacturers.counts" :title="name" subcols="2" size="l">
                <onyks-text size="l">{{ number }}</onyks-text>
            </onyks-card>
        </onyks-container>

        <onyks-text v-else>{{ $t('common.no_manufacturers') }}</onyks-text>

    </ManagerPage>

</template>