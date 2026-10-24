<script setup>
    import { useLoaderStore } from '@/stores/loader';
    import ManagerPage from '@/components/ManagerPage.vue';
    import { onMounted, ref, reactive, computed } from 'vue';
    import BasicButtonsPanel from '@/components/BasicButtonsPanel.vue';
    import BasicSearch from '@/components/BasicSearch.vue';
    import BasicTable from '@/components/BasicTable.vue';
    import { useBasicTable, useAddItemDialog, useEditItemDialog, useDeleteItemsDialog } from '@/utils/tools';
    import { services } from '@/utils/api';
    import AddItemDialog from '@/components/AddItemDialog.vue';
    import EditItemDialog from '@/components/EditItemDialog.vue';
    import DeleteItemsDialog from '@/components/DeleteItemsDialog.vue';
    import { html } from 'lit';
    import router from '@/router';
    import { i18n } from '@/utils/localization';
    import { OnyksToastContainer } from 'onyks-web-ui-system';
    import { useLabels } from '@/utils/tools';

    const loaderStore = useLoaderStore();
    const expandPage = ref(false);


    const suppliersTable = reactive(useBasicTable(services.suppliers, [
        { label: i18n.global.t('views.ManagementView.columns.selected'), key: 'selected' },
        { label: i18n.global.t('views.ManagementView.columns.id'), key: 'id' },
        { label: i18n.global.t('views.ManagementView.columns.name'), key: 'name' },
        { label: i18n.global.t('views.ManagementView.columns.createdAt'), key: 'createdAt' }
    ],undefined, undefined,  (item) => { item.selected = false; item.createdAt = i18n.global.d(new Date(item.createdAt), 'short')}))

    const manufacturersTable = reactive(useBasicTable(services.manufacturers, [
        { label: i18n.global.t('views.ManagementView.columns.selected'), key: 'selected' },
        { label: i18n.global.t('views.ManagementView.columns.id'), key: 'id' },
        { label: i18n.global.t('views.ManagementView.columns.name'), key: 'name' },
        { label: i18n.global.t('views.ManagementView.columns.createdAt'), key: 'createdAt' }
    ],undefined, undefined, (item) => { item.selected = false; item.createdAt = i18n.global.d(new Date(item.createdAt), 'short')}))

    const tablesTable = reactive(useBasicTable(services.tables, [
        { label: i18n.global.t('views.ManagementView.columns.selected'), key: 'selected' },
        { label: i18n.global.t('views.ManagementView.columns.id'), key: 'id' },
        { label: i18n.global.t('views.ManagementView.columns.name'), key: 'name' },
        { label: i18n.global.t('views.ManagementView.columns.createdAt'), key: 'createdAt' }
    ],undefined, undefined, (item) => { item.selected = false; item.createdAt = i18n.global.d(new Date(item.createdAt), 'short')}))

    const elementsTable = reactive(useBasicTable(services.elements, [
        { label: i18n.global.t('views.ManagementView.columns.selected'), key: 'selected' },
        { label: i18n.global.t('views.ManagementView.columns.partName'), key: 'partName' },
        { label: i18n.global.t('views.ManagementView.columns.manufacturer'), key: 'manufacturer'},
        { label: i18n.global.t('views.ManagementView.columns.table'), key: 'table'},
        { label: i18n.global.t('views.ManagementView.columns.value'), key: 'value' },
        { label: i18n.global.t('views.ManagementView.columns.availability'), key: 'availability' },
        { label: i18n.global.t('views.ManagementView.columns.createdAt'), key: 'createdAt' }
    ], true, (row) => html`
        <onyks-container gap="m" type="stack">
            <onyks-container type="group" gap="m">
                <onyks-tag style="cursor: pointer; width: 75px; text-align: center;" background="blue" icon="" style="width: 75px; text-align: center;" @click=${() => router.push(`elements/edit/${row?.uuid}`)}>${i18n.global.t('views.ManagementView.btns.edit')}</onyks-tag>
                <onyks-tag style="cursor: pointer; width: 75px; text-align: center; " background="yellow" icon="" style="width: 75px; text-align: center;" @click=${() => router.push(`elements/duplicate/${row?.uuid}`)}>${i18n.global.t('views.ManagementView.btns.duplicate')}</onyks-tag>
                <onyks-tag style="cursor: pointer; width: 75px; text-align: center;" background="red" icon="" style="width: 75px; text-align: center;">${i18n.global.t('views.ManagementView.btns.delete')}</onyks-tag>
            </onyks-container>
        
            <onyks-container style="grid-template-columns: 400px minmax(0, 1fr);" type="grid" gap="m">
                <onyks-container type="stack" gap="m" cols="1">
                    
                    <onyks-header level="6">${i18n.global.t('views.ManagementView.columns.uuid')}</onyks-header>
                    <onyks-text size="s">${row?.uuid || ''}</onyks-text>
                    <onyks-header level="6" style="width: 100%; text-align: left;">${i18n.global.t('views.ManagementView.columns.suppliers')}</onyks-header>
                    ${ Object.values(row.suppliers || {}).length > 0 ? html`<onyks-text size="s">${Object.values(row.suppliers || {}).map(supplier => supplier.value).join(', ')}</onyks-text>` : html`<onyks-text size="s">${i18n.global.t('views.ManagementView.columns.noData')}</onyks-text>`}
                    
                    
                    <onyks-header level="6">${i18n.global.t('views.ManagementView.columns.symbol')}</onyks-header>
                    ${row.libraryPath != '' && row.libraryReference != '' ? html`<onyks-path style="width: 100%; max-width: 100%; min-width: 0; overflow: hidden;" .content=${(row.libraryPath.split('/')).concat(row.libraryReference)} size="s"></onyks-path>` : html`<onyks-text size="s">${i18n.global.t('views.ManagementView.columns.noData')}</onyks-text>`}
                    
                    <onyks-header level="6">${i18n.global.t('views.ManagementView.columns.footprintNo1')}</onyks-header>
                    ${row.footprintPathNo1 != '' && row.footprintReferenceNo1 != '' ? html`<onyks-path style="width: 100%; max-width: 100%; min-width: 0; overflow: hidden;" .content=${row.footprintPathNo1.split('/').concat(row.footprintReferenceNo1)} size="s"></onyks-path>` : html`<onyks-text size="s">${i18n.global.t('views.ManagementView.columns.noData')}</onyks-text>`}
                    <onyks-header level="6">${i18n.global.t('views.ManagementView.columns.footprintNo2')}</onyks-header>
                    ${row.footprintPathNo2 != '' && row.footprintReferenceNo2 != '' ? html`<onyks-path style="width: 100%; max-width: 100%; min-width: 0; overflow: hidden;" .content=${row.footprintPathNo2.split('/').concat(row.footprintReferenceNo2)} size="s"></onyks-path>` : html`<onyks-text size="s">${i18n.global.t('views.ManagementView.columns.noData')}</onyks-text>`}
                    <onyks-header level="6">${i18n.global.t('views.ManagementView.columns.footprintNo3')}</onyks-header>
                    ${row.footprintPathNo3 != '' && row.footprintReferenceNo3 != '' ? html`<onyks-path style="width: 100%; max-width: 100%; min-width: 0; overflow: hidden;" .content=${row.footprintPathNo3.split('/').concat(row.footprintReferenceNo3)} size="s"></onyks-path>` : html`<onyks-text size="s">${i18n.global.t('views.ManagementView.columns.noData')}</onyks-text>`}
                </onyks-container>
                <onyks-container type="stack" gap="m">
                    <onyks-header level="6">${i18n.global.t('views.ManagementView.columns.description')}</onyks-header>
                    ${row.description != '' ? html`<onyks-text size="s" style="text-align: justify;">${row.description}</onyks-text>` : html`<onyks-text size="s">${i18n.global.t('views.ManagementView.columns.noData')}</onyks-text>`}
                    <onyks-header level="6">${i18n.global.t('views.ManagementView.columns.tags')}</onyks-header>
                    ${(row.tags || []).length > 0
                        ? html`<onyks-container gap="m" type="group">${row.tags.map(tag => html`<onyks-tag size="s" background="blue">${tag}</onyks-tag>`)}</onyks-container>`
                        : html`<onyks-text size="s">${i18n.global.t('views.ManagementView.columns.noData')}</onyks-text>`}

                    <onyks-header level="6">${i18n.global.t('views.ManagementView.columns.datasheets')}</onyks-header>
                    ${row.datasheets.length > 0
                        ? html`<onyks-container type="group" gap="m">${row.datasheets.map(datasheet => html`<onyks-tag background="yellow" size="s" icon="F756" @click=${() => window.open('/files/' + datasheet.uuid + '.pdf', '_blank')}>${datasheet.name}</onyks-tag>`)}</onyks-container>`
                        : html`<onyks-text size="s">${i18n.global.t('views.ManagementView.columns.noData')}</onyks-text>`}
                </onyks-container>
            </onyks-container>
        </onyks-container>
    `, (item) => 
    { 
        item.selected = false; 
        item.description = item.description || i18n.global.t('views.ManagementView.columns.noData')
        item.createdAt = i18n.global.d(new Date(item.createdAt), 'short'); 
        item.manufacturer = item.manufacturer || i18n.global.t('views.ManagementView.columns.noData') }))

    const suppliersDialogs = reactive(
    {
        add: useAddItemDialog(services.suppliers, i18n.global.t('views.ManagementView.dialogs.suppliers.add'), () => 
        {
            elementsTable.search()
            suppliersTable.search()
            OnyksToastContainer.success(i18n.global.t('views.ManagementView.toasts.supplierAdded'), 3000, true, 'm')
        }),
        edit: useEditItemDialog(services.suppliers, i18n.global.t('views.ManagementView.dialogs.suppliers.edit'), () => 
        {
            suppliersTable.search()
            elementsTable.search()
            OnyksToastContainer.success(i18n.global.t('views.ManagementView.toasts.supplierEdited'), 3000, true, 'm')
        }, computed(() => suppliersTable.data.find(item => item.selected) || null)),
        delete: useDeleteItemsDialog(services.suppliers, i18n.global.t('views.ManagementView.dialogs.suppliers.delete'), () => 
        {
            suppliersTable.search()
            elementsTable.search()
        }, computed(() => suppliersTable.data.filter(item => item.selected)))
    })
    
    const manufacturersDialogs = reactive(
    {
        add: useAddItemDialog(services.manufacturers, i18n.global.t('views.ManagementView.dialogs.manufacturers.add'), () => 
        {
            manufacturersTable.search()
            elementsTable.search()
            OnyksToastContainer.success(i18n.global.t('views.ManagementView.toasts.manufacturerAdded'), 3000, true, 'm')
        }),
        edit: useEditItemDialog(services.manufacturers, i18n.global.t('views.ManagementView.dialogs.manufacturers.edit'), () => 
        {
            manufacturersTable.search()
            elementsTable.search()
            OnyksToastContainer.success(i18n.global.t('views.ManagementView.toasts.manufacturerEdited'), 3000, true, 'm')
        }, computed(() => manufacturersTable.data.find(item => item.selected) || null)),
        delete: useDeleteItemsDialog(services.manufacturers, i18n.global.t('views.ManagementView.dialogs.manufacturers.delete'), () => 
        {
            manufacturersTable.search()
            elementsTable.search()
        }, computed(() => manufacturersTable.data.filter(item => item.selected)))
    })

    const tablesDialogs = reactive(
    {
        add: useAddItemDialog(services.tables, i18n.global.t('views.ManagementView.dialogs.tables.add'), () => 
        {
            tablesTable.search()
            elementsTable.search()
            OnyksToastContainer.success(i18n.global.t('views.ManagementView.toasts.tableAdded'), 3000, true, 'm')
        }),
        edit: useEditItemDialog(services.tables, i18n.global.t('views.ManagementView.dialogs.tables.edit'), () => 
        {
            tablesTable.search()
            elementsTable.search()
            OnyksToastContainer.success(i18n.global.t('views.ManagementView.toasts.tableEdited'), 3000, true, 'm')
        }, computed(() => tablesTable.data.find(item => item.selected) || null)),
        delete: useDeleteItemsDialog(services.tables, i18n.global.t('views.ManagementView.dialogs.tables.delete'), () => 
        {
            tablesTable.search()
            elementsTable.search()
        }, computed(() => tablesTable.data.filter(item => item.selected)))
    })

    const labels = reactive(useLabels())

    onMounted(async () =>
    {
        await suppliersTable.init()
        await manufacturersTable.init()
        await tablesTable.init()

        elementsTable.sortBy = "createdAt"
        await elementsTable.init()

        loaderStore.hide()
        loaderStore.globalHide()
    })
</script>

<template>
    <ManagerPage :title="$t('views.ManagementView.title')" :expand="expandPage">
        
        <onyks-container type="group" align="center" justify="left" gap="m">
            <onyks-text>{{$t('views.ManagementView.expandPage')}}</onyks-text>
            <onyks-checkbox @change="expandPage = !expandPage" :checked="expandPage"></onyks-checkbox>
        </onyks-container>
        

        <onyks-header level="3">{{$t('views.ManagementView.titles.elements')}}</onyks-header>

        
        <BasicButtonsPanel>
            <onyks-button @click="router.push('/manager/elements/create')" background="green">{{$t('views.ManagementView.btns.add')}}</onyks-button>
            <onyks-button background="blue" :disabled="elementsTable.selected != 1" @click="router.push(`/manager/elements/edit/${elementsTable?.data.filter(item => item.selected)[0]?.uuid}`)">{{$t('views.ManagementView.btns.edit')}}</onyks-button>
            <onyks-button background="yellow" :disabled="elementsTable.selected != 1" @click="router.push(`/manager/elements/duplicate/${elementsTable?.data.filter(item => item.selected)[0]?.uuid}`)">{{$t('views.ManagementView.btns.duplicate')}}</onyks-button>
            <onyks-button background="red" :disabled="elementsTable.selected === 0">{{$t('views.ManagementView.btns.delete')}}</onyks-button>
            <onyks-button background="gray" :disabled="elementsTable.selected != 1" @click="router.push(`/manager/elements/details/${elementsTable?.data.filter(item => item.selected)[0]?.uuid}`)">{{$t('views.ManagementView.btns.details')}}</onyks-button>
            <onyks-button @click="labels.generate(elementsTable?.data.filter(item => item.selected))" background="green" :disabled="elementsTable.selected === 0">{{$t('views.ManagementView.btns.labels')}}</onyks-button>
            <onyks-button background="blue">{{$t('views.ManagementView.btns.scan')}}</onyks-button>
        </BasicButtonsPanel>
        <BasicSearch v-model="elementsTable.searchPhrase" :search="elementsTable.search"></BasicSearch>
        <BasicTable v-model="elementsTable"></BasicTable>

        <onyks-header level="3">{{$t('views.ManagementView.titles.tables')}}</onyks-header>
        <BasicButtonsPanel>
            <onyks-button background="green" @click="tablesDialogs.add.open = true">{{$t('views.ManagementView.btns.add')}}</onyks-button>
            <onyks-button background="blue" :disabled="tablesTable.selected != 1" @click="tablesDialogs.edit.open = true">{{$t('views.ManagementView.btns.edit')}}</onyks-button>
            <onyks-button background="red" :disabled="tablesTable.selected === 0" @click="tablesDialogs.delete.firstOpen = true">{{$t('views.ManagementView.btns.delete')}}</onyks-button>
        </BasicButtonsPanel>
        <BasicSearch v-model="tablesTable.searchPhrase" :search="tablesTable.search"></BasicSearch>
        <BasicTable v-model="tablesTable"></BasicTable>
        <AddItemDialog v-model="tablesDialogs.add"></AddItemDialog>
        <EditItemDialog v-model="tablesDialogs.edit"></EditItemDialog>
        <DeleteItemsDialog v-model="tablesDialogs.delete"></DeleteItemsDialog>

        <onyks-header level="3">{{$t('views.ManagementView.titles.manufacturers')}}</onyks-header>
        <BasicSearch v-model="manufacturersTable.searchPhrase" :search="manufacturersTable.search"></BasicSearch>
        <BasicButtonsPanel>
            <onyks-button background="green" @click="manufacturersDialogs.add.open = true">{{$t('views.ManagementView.btns.add')}}</onyks-button>
            <onyks-button background="blue" :disabled="manufacturersTable.selected != 1" @click="manufacturersDialogs.edit.open = true">{{$t('views.ManagementView.btns.edit')}}</onyks-button>
            <onyks-button background="red" :disabled="manufacturersTable.selected === 0" @click="manufacturersDialogs.delete.firstOpen = true">{{$t('views.ManagementView.btns.delete')}}</onyks-button>
        </BasicButtonsPanel>
        <BasicTable v-model="manufacturersTable"></BasicTable>
        <AddItemDialog v-model="manufacturersDialogs.add"></AddItemDialog>
        <EditItemDialog v-model="manufacturersDialogs.edit"></EditItemDialog>
        <DeleteItemsDialog v-model="manufacturersDialogs.delete"></DeleteItemsDialog>

        <onyks-header level="3">{{$t('views.ManagementView.titles.suppliers')}}</onyks-header>
        <BasicButtonsPanel>
            <onyks-button background="green" @click="suppliersDialogs.add.open = true">{{$t('views.ManagementView.btns.add')}}</onyks-button>
            <onyks-button background="blue" :disabled="suppliersTable.selected != 1" @click="suppliersDialogs.edit.open = true">{{$t('views.ManagementView.btns.edit')}}</onyks-button>
            <onyks-button background="red" :disabled="suppliersTable.selected === 0" @click="suppliersDialogs.delete.firstOpen = true">{{$t('views.ManagementView.btns.delete')}}</onyks-button>
        </BasicButtonsPanel>
        <BasicSearch v-model="suppliersTable.searchPhrase" :search="suppliersTable.search"></BasicSearch>
        <BasicTable v-model="suppliersTable"></BasicTable>
        <AddItemDialog v-model="suppliersDialogs.add"></AddItemDialog>
        <EditItemDialog v-model="suppliersDialogs.edit"></EditItemDialog>
        <DeleteItemsDialog v-model="suppliersDialogs.delete"></DeleteItemsDialog>
        <DeleteItemsDialog v-model="suppliersDialogs.delete"></DeleteItemsDialog>

    </ManagerPage>
</template>

<style lang="css" scoped>
    :deep(onyks-table)
    {
        height: 600px;
    }
</style>