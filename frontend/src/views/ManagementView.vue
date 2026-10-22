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
    import { addToast } from '@/utils/tools';
    import { html } from 'lit';
import router from '@/router';

    const loaderStore = useLoaderStore();
    const expandPage = ref(false);

    window.x = services.elements
    // tables
    const suppliersTable = reactive(useBasicTable(services.suppliers, [
        { label: 'Selected', key: 'selected' },
        { label: 'ID', key: 'id' },
        { label: 'Name', key: 'name' },
        { label: 'Created At', key: 'createdAt' }
    ]))

    const manufacturersTable = reactive(useBasicTable(services.manufacturers, [
        { label: 'Selected', key: 'selected' },
        { label: 'ID', key: 'id' },
        { label: 'Name', key: 'name' },
        { label: 'Created At', key: 'createdAt' }
    ]))

    const tablesTable = reactive(useBasicTable(services.tables, [
        { label: 'Selected', key: 'selected' },
        { label: 'ID', key: 'id' },
        { label: 'Name', key: 'name' },
        { label: 'Created At', key: 'createdAt' }
    ]))

    const elementsTable = reactive(useBasicTable(services.elements, [
        { label: 'Selected', key: 'selected' },
        { label: 'Part Name', key: 'partName' },
        { label: 'Manufacturer', key: 'manufacturer'},
        { label: 'Table', key: 'table'},
        { label: 'Value', key: 'value' },
        { label: 'Availability', key: 'availability' },
        { label: 'Created At', key: 'createdAt' }
    ], true, (row) => html`
        <onyks-container gap="m" type="stack">
            <onyks-container type="group" gap="m">
                <onyks-tag background="blue" icon="" style="width: 75px; text-align: center;" @click=${() => router.push(`elements/edit/${row?.uuid}`)}>Edit</onyks-tag>
                <onyks-tag background="yellow" icon="" style="width: 75px; text-align: center;" @click=${() => router.push(`elements/duplicate/${row?.uuid}`)}>Duplicate</onyks-tag>
                <onyks-tag background="red" icon="" style="width: 75px; text-align: center;">Delete</onyks-tag>
            </onyks-container>
        

            <onyks-container style="background-color: transparent; width: 100%; height: fit-content;" type="group" gap="m" mobile-breakpoint="900">
                <onyks-container type="stack" gap="m" cols="1" style="max-width: 50%;">
                    
                    <onyks-header level="6">UUID</onyks-header>
                    <onyks-text>${row?.uuid || ''}</onyks-text>
                    <onyks-header level="6" style="width: 100%; text-align: left;">Suppliers Names</onyks-header>
                    <onyks-text>${Object.values(row.suppliers || {}).map(supplier => supplier.value).join(', ')}</onyks-text>
                    <onyks-header level="6">Symbol</onyks-header>
                    ${row.libraryPath != '' && row.libraryReference != '' ? html`<onyks-path .content=${(row.libraryPath.split('/')).concat(row.libraryReference)} size="s"></onyks-path>` : html`<onyks-text>Not defined</onyks-text>`}
                    
                    <onyks-header level="6">Footprints</onyks-header>
                    <onyks-text>Footprint No 1</onyks-text>
                    ${row.footprintPathNo1 != '' && row.footprintReferenceNo1 != '' ? html`<onyks-path .content=${row.footprintPathNo1.split('/').concat(row.footprintReferenceNo1)} size="s"></onyks-path>` : html`<onyks-text>Not defined</onyks-text>`}
                    <onyks-text>Footprint No 2</onyks-text>
                    ${row.footprintPathNo2 != '' && row.footprintReferenceNo2 != '' ? html`<onyks-path .content=${row.footprintPathNo2.split('/').concat(row.footprintReferenceNo2)} size="s"></onyks-path>` : html`<onyks-text>Not defined</onyks-text>`}
                    <onyks-text>Footprint No 3</onyks-text>
                    ${row.footprintPathNo3 != '' && row.footprintReferenceNo3 != '' ? html`<onyks-path .content=${row.footprintPathNo3.split('/').concat(row.footprintReferenceNo3)} size="s"></onyks-path>` : html`<onyks-text>Not defined</onyks-text>`}
                </onyks-container>
                <onyks-container type="stack" gap="m" style="max-width: 50%;">
                    <onyks-header level="6">Description</onyks-header>
                    <onyks-text>${row.description}</onyks-text>
                    <onyks-header level="6">Tags</onyks-header>
                    <onyks-container gap="m" type="group">
                        ${row.tags.map(tag => html`<onyks-tag background="blue">${tag}</onyks-tag>`)}
                    </onyks-container>
                    <onyks-header level="6">Datasheets</onyks-header>
                    <onyks-container type="group" gap="m">
                        ${row.datasheets.map(datasheet => html`<onyks-tag size="s" @click=${() => window.open('/files/' + datasheet.uuid + '.pdf', '_blank')}>${datasheet.name}</onyks-tag>`)}
                    </onyks-container>
                </onyks-container>
            </onyks-container>
        </onyks-container>
    `))
            // <onyks-header level="6" cols="1">Symbol</onyks-header>
            // <onyks-path .content=${['a', 'b']} size="s" disabled style="overflow-y: hidden;" cols="9"></onyks-path>
    // dialogs
    const suppliersDialogs = reactive(
    {
        add: useAddItemDialog(services.suppliers, 'Add Supplier', () => 
        {
            suppliersTable.search()
            addToast('Supplier added successfully', 3000, true, 'm', 'success')
        }),
        edit: useEditItemDialog(services.suppliers, 'Edit Supplier', () => 
        {
            suppliersTable.search()
            addToast('Supplier edited successfully', 3000, true, 'm', 'success')
        }, computed(() => suppliersTable.data.find(item => item.selected) || null)),
        delete: useDeleteItemsDialog(services.suppliers, 'Delete Supplier(s)', () => 
        {
            suppliersTable.search()
        }, computed(() => suppliersTable.data.filter(item => item.selected)))
    })
    
    const manufacturersDialogs = reactive(
    {
        add: useAddItemDialog(services.manufacturers, 'Add Manufacturer', () => 
        {
            manufacturersTable.search()
            addToast('Manufacturer added successfully', 3000, true, 'm', 'success')
        }),
        edit: useEditItemDialog(services.manufacturers, 'Edit Manufacturer', () => 
        {
            manufacturersTable.search()
            addToast('Manufacturer edited successfully', 3000, true, 'm', 'success')
        }, computed(() => manufacturersTable.data.find(item => item.selected) || null)),
        delete: useDeleteItemsDialog(services.manufacturers, 'Delete Manufacturer(s)', () => 
        {
            manufacturersTable.search()
        }, computed(() => manufacturersTable.data.filter(item => item.selected)))
    })

    const tablesDialogs = reactive(
    {
        add: useAddItemDialog(services.tables, 'Add Table', () => 
        {
            tablesTable.search()
            addToast('Table added successfully', 3000, true, 'm', 'success')
        }),
        edit: useEditItemDialog(services.tables, 'Edit Table', () => 
        {
            tablesTable.search()
            addToast('Table edited successfully', 3000, true, 'm', 'success')
        }, computed(() => tablesTable.data.find(item => item.selected) || null)),
        delete: useDeleteItemsDialog(services.tables, 'Delete Table(s)', () => 
        {
            tablesTable.search()
        }, computed(() => tablesTable.data.filter(item => item.selected)))
    })

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
    <ManagerPage title="Management" :expand="expandPage">
        
        <onyks-container type="group" align="center" justify="left" gap="m">
            <onyks-text>Expand Page</onyks-text>
            <onyks-checkbox @change="expandPage = !expandPage" :checked="expandPage"></onyks-checkbox>
        </onyks-container>
        

        <onyks-header level="3">Elements</onyks-header>

        
        <BasicButtonsPanel>
            <router-link to="/manager/elements/create">
                <onyks-button background="green">Add</onyks-button>
            </router-link>
            <onyks-button background="blue" :disabled="elementsTable.selected != 1" @click="router.push(`/manager/elements/edit/${elementsTable?.data.filter(item => item.selected)[0]?.uuid}`)">Edit</onyks-button>
            <onyks-button background="yellow" :disabled="elementsTable.selected != 1" @click="router.push(`/manager/elements/duplicate/${elementsTable?.data.filter(item => item.selected)[0]?.uuid}`)">Duplicate</onyks-button>
            <onyks-button background="red" :disabled="elementsTable.selected === 0">Delete</onyks-button>
            <onyks-button background="gray" @click="router.push(`/manager/elements/details/${elementsTable?.data.filter(item => item.selected)[0]?.uuid}`)">Details</onyks-button>
            <onyks-button background="green">Labels</onyks-button>
            <onyks-button background="blue">Scan</onyks-button>
        </BasicButtonsPanel>
        <BasicSearch v-model="elementsTable.searchPhrase" :search="elementsTable.search"></BasicSearch>
        <BasicTable v-model="elementsTable"></BasicTable>

        <onyks-header level="3">Tables</onyks-header>
        <BasicButtonsPanel>
            <onyks-button background="green" @click="tablesDialogs.add.open = true">Add</onyks-button>
            <onyks-button background="blue" :disabled="tablesTable.selected != 1" @click="tablesDialogs.edit.open = true">Edit</onyks-button>
            <onyks-button background="red" :disabled="tablesTable.selected === 0" @click="tablesDialogs.delete.firstOpen = true">Delete</onyks-button>
        </BasicButtonsPanel>
        <BasicSearch v-model="tablesTable.searchPhrase" :search="tablesTable.search"></BasicSearch>
        <BasicTable v-model="tablesTable"></BasicTable>
        <AddItemDialog v-model="tablesDialogs.add"></AddItemDialog>
        <EditItemDialog v-model="tablesDialogs.edit"></EditItemDialog>
        <DeleteItemsDialog v-model="tablesDialogs.delete"></DeleteItemsDialog>

        <onyks-header level="3">Manufacturers</onyks-header>
        <BasicSearch v-model="manufacturersTable.searchPhrase" :search="manufacturersTable.search"></BasicSearch>
        <BasicButtonsPanel>
            <onyks-button background="green" @click="manufacturersDialogs.add.open = true">Add</onyks-button>
            <onyks-button background="blue" :disabled="manufacturersTable.selected != 1" @click="manufacturersDialogs.edit.open = true">Edit</onyks-button>
            <onyks-button background="red" :disabled="manufacturersTable.selected === 0" @click="manufacturersDialogs.delete.firstOpen = true">Delete</onyks-button>
        </BasicButtonsPanel>
        <BasicTable v-model="manufacturersTable"></BasicTable>
        <AddItemDialog v-model="manufacturersDialogs.add"></AddItemDialog>
        <EditItemDialog v-model="manufacturersDialogs.edit"></EditItemDialog>
        <DeleteItemsDialog v-model="manufacturersDialogs.delete"></DeleteItemsDialog>

        <onyks-header level="3">Suppliers</onyks-header>
        <BasicButtonsPanel>
            <onyks-button background="green" @click="suppliersDialogs.add.open = true">Add</onyks-button>
            <onyks-button background="blue" :disabled="suppliersTable.selected != 1" @click="suppliersDialogs.edit.open = true">Edit</onyks-button>
            <onyks-button background="red" :disabled="suppliersTable.selected === 0" @click="suppliersDialogs.delete.firstOpen = true">Delete</onyks-button>
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