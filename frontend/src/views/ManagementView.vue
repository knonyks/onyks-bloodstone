<script setup>
    import { useLoaderStore } from '../stores/loader';
    import ManagerPage from '../components/ManagerPage.vue';
    import { onMounted, ref, reactive, computed } from 'vue';
    import BasicButtonsPanel from '../components/BasicButtonsPanel.vue';
    import BasicSearch from '../components/BasicSearch.vue';
    import BasicTable from '../components/BasicTable.vue';
    import { services } from '../utils/api';
    import AddItemDialog from '../components/AddItemDialog.vue';
    import EditItemDialog from '../components/EditItemDialog.vue';
    import RemoveItemsDialog from '../components/RemoveItemsDialog.vue';
    import router from '../router';
    import { i18n } from '../utils/localization';
    import { OnyksToastContainer } from 'onyks-web-ui-system';
    import { elements_table_expand_template } from '../utils/tools';
    import { useAddItemDialog } from '../composables/useAddItemDialog';
    import { useEditItemDialog } from '../composables/useEditItemDialog';
    import { useRemoveItemsDialog } from '../composables/useRemoveItemsDialog';
    import { useBasicTable } from '../composables/useBasicTable';
    import SubTitle from '../components/SubTitle.vue';
    import { labels_generate } from '../utils/generateLabels';
    
    const loaderStore = useLoaderStore()
    const expand_page = ref(false)
    const tables = reactive(
    {
        suppliers: useBasicTable(services.suppliers, [
            {
                label: i18n.global.t('common.selected'),
                key: 'selected'
            },
            {
                label: i18n.global.t('common.id'),
                key: 'id'
            },
            {
                label: i18n.global.t('suppliers.name'),
                key: 'name'
            },
            {
                label: i18n.global.t('common.created_at'),
                key: 'created_at'
            }
        ], 'id', (item) => {return { ...item, selected: false, created_at: i18n.global.d(new Date(item.created_at), 'short') }}),
        manufacturers: useBasicTable(services.manufacturers, [
            {
                label: i18n.global.t('common.selected'),
                key: 'selected'
            },
            {
                label: i18n.global.t('common.id'),
                key: 'id'
            },
            {
                label: i18n.global.t('manufacturers.name'),
                key: 'name'
            },
            {
                label: i18n.global.t('common.created_at'),
                key: 'created_at'
            }
        ], 'id', (item) => {return { ...item, selected: false, created_at: i18n.global.d(new Date(item.created_at), 'short') }}),
        tables: useBasicTable(services.tables, [
            {
                label: i18n.global.t('common.selected'),
                key: 'selected'
            },
            {
                label: i18n.global.t('common.id'),
                key: 'id'
            },
            {
                label: i18n.global.t('tables.name'),
                key: 'name'
            },
            {
                label: i18n.global.t('common.created_at'),
                key: 'created_at'
            }
        ], 'id', (item) => {return { ...item, selected: false, created_at: i18n.global.d(new Date(item.created_at), 'short') }}),
        elements: useBasicTable(services.elements, [
        { label: i18n.global.t('common.selected'), key: 'selected' },
        { label: i18n.global.t('elements.part_name'), key: 'part_name' },
        { label: i18n.global.t('elements.manufacturer'), key: 'manufacturer'},
        { label: i18n.global.t('elements.table'), key: 'table'},
        { label: i18n.global.t('elements.value'), key: 'value' },
        { label: i18n.global.t('elements.availability'), key: 'availability' },
        { label: i18n.global.t('common.created_at'), key: 'created_at' }
        ], 'created_at', (item) => {return { 
            ...item, 
            selected: false, 
            created_at: i18n.global.d(new Date(item.created_at), 'short') ,
            availability: item.availability || i18n.global.t('common.no_data'),
            value: item.value || i18n.global.t('common.no_data'),
            manufacturer: item.manufacturer || i18n.global.t('common.no_data'),
            footprint_path_1: item.footprint_path_1 || '',
            footprint_path_2: item.footprint_path_2 || '',
            footprint_path_3: item.footprint_path_3 || '',
            footprint_reference_1: item.footprint_reference_1 || '',
            footprint_reference_2: item.footprint_reference_2 || '',
            footprint_reference_3: item.footprint_reference_3 || '',
            library_reference: item.library_reference || '',
            library_path: item.library_path || ''
        }}, elements_table_expand_template)
    })  

    tables.elements.expandable = true

    const dialogs = reactive(
    {
        suppliers:
        {
            add: useAddItemDialog(services.suppliers, i18n.global.t('suppliers.add'), (item) => 
            { 
                OnyksToastContainer.success(i18n.global.t('suppliers.added'))
                tables.suppliers.search()
            }),
            edit: useEditItemDialog(services.suppliers, i18n.global.t('suppliers.edit'), (item) =>
            {
                OnyksToastContainer.success(i18n.global.t('suppliers.edited'))
                tables.suppliers.search()
            }, () => tables.suppliers.data.find(item => item.selected) || null),
            remove: useRemoveItemsDialog(services.suppliers, i18n.global.t('suppliers.delete'), ['id', 'name'], (item) =>
            {
                OnyksToastContainer.success(i18n.global.t('common.supplier_deleted'))
                tables.suppliers.search()
            }, () => tables.suppliers.data.filter(item => item.selected))
        },
        manufacturers: 
        {
            add: useAddItemDialog(services.manufacturers, i18n.global.t('manufacturers.add'), (item) => 
            { 
                OnyksToastContainer.success(i18n.global.t('manufacturers.added'))
                tables.manufacturers.search()
            }),
            edit: useEditItemDialog(services.manufacturers, i18n.global.t('manufacturers.edit'), (item) =>
            {
                OnyksToastContainer.success(i18n.global.t('manufacturers.edited'))
                tables.manufacturers.search()
            }, () => tables.manufacturers.data.find(item => item.selected) || null),
            remove: useRemoveItemsDialog(services.manufacturers, i18n.global.t('manufacturers.delete'), ['id', 'name'], (item) =>
            {
                OnyksToastContainer.success(i18n.global.t('common.manufacturer_deleted'))
                tables.manufacturers.search()
            }, () => tables.manufacturers.data.filter(item => item.selected))
        },
        tables:
        {
            add: useAddItemDialog(services.tables, i18n.global.t('tables.add'), (item) => 
            { 
                OnyksToastContainer.success(i18n.global.t('tables.added'))
                tables.tables.search()
            }),
            edit: useEditItemDialog(services.tables, i18n.global.t('tables.edit'), (item) =>
            {
                OnyksToastContainer.success(i18n.global.t('tables.edited'))
                tables.tables.search()
            }, () => tables.tables.data.find(item => item.selected) || null),
            remove: useRemoveItemsDialog(services.tables, i18n.global.t('tables.delete'), ['id', 'name'], (item) =>
            {
                tables.tables.search()
            }, () => tables.tables.data.filter(item => item.selected))
        },
        elements: 
        {
            remove: useRemoveItemsDialog(services.elements, i18n.global.t('elements.delete'), ['uuid', 'part_name'], (item) =>
            {
                tables.elements.search()
            }, () => tables.elements.data.filter(item => item.selected))
        }
    })

    onMounted(async () =>
    {
        await tables.suppliers.init()
        await tables.manufacturers.init()
        await tables.tables.init()
        await tables.elements.init()
        
        loaderStore.hide()
        loaderStore.globalHide()
    })
</script>

<template>
    <ManagerPage :title="$t('common.management')" :expand="expand_page">
        <onyks-container type="group" align="center" justify="left" gap="m">
            <onyks-text>{{$t('common.expand_page')}}</onyks-text>
            <onyks-checkbox @change="expand_page = !expand_page" :checked="expand_page"></onyks-checkbox>
        </onyks-container>

        <!-- Elements -->
        <SubTitle>{{ $t('common.elements') }}</SubTitle>
        <BasicButtonsPanel>
            <onyks-button @click="router.push('/manager/elements/create')" background="green">{{$t('common.add')}}</onyks-button>
            <onyks-button background="blue" :disabled="tables.elements.selected != 1" @click="router.push(`/manager/elements/edit/${tables.elements?.data.filter(item => item.selected)[0]?.uuid}`)">{{$t('common.edit')}}</onyks-button>
            <onyks-button background="yellow" :disabled="tables.elements.selected != 1" @click="router.push(`/manager/elements/duplicate/${tables.elements?.data.filter(item => item.selected)[0]?.uuid}`)">{{$t('common.duplicate')}}</onyks-button>
            <onyks-button background="red" :disabled="tables.elements.selected === 0" @click="dialogs.elements.remove.items = tables.elements.data.filter(item => item.selected); dialogs.elements.remove.first_open = true">{{$t('common.remove')}}</onyks-button>
            <onyks-button background="gray" :disabled="tables.elements.selected != 1" @click="router.push(`/manager/elements/details/${tables.elements?.data.filter(item => item.selected)[0]?.uuid}`)">{{$t('common.details')}}</onyks-button>
            <onyks-button @click="labels_generate(tables.elements?.data.filter(item => item.selected))" background="green" :disabled="tables.elements.selected === 0">{{$t('common.labels')}}</onyks-button>
            <onyks-button background="blue">{{$t('common.scan')}}</onyks-button>
        </BasicButtonsPanel>
        <BasicSearch v-model="tables.elements.search_phrase" :search="tables.elements.search"></BasicSearch>
        <BasicTable v-model="tables.elements" @remove-element="(event) => {
            dialogs.elements.remove.items = [event.detail];
            dialogs.elements.remove.first_open = true;
        }"></BasicTable>
        <RemoveItemsDialog v-model="dialogs.elements.remove"></RemoveItemsDialog>
        <RemoveItemsDialog v-model="dialogs.elements.remove"></RemoveItemsDialog>

        <!-- Tables -->
        <SubTitle>{{ $t('common.tables') }}</SubTitle>
        <BasicButtonsPanel>
            <onyks-button background="green" @click="dialogs.tables.add.open = true">{{$t('common.add')}}</onyks-button>
            <onyks-button background="blue" :disabled="!(tables.tables.selected == 1)" @click="dialogs.tables.edit.name = dialogs.tables.edit.item.name; dialogs.tables.edit.open = true">{{$t('common.edit')}}</onyks-button>
            <onyks-button background="red" :disabled="!(tables.tables.selected > 0)" @click="dialogs.tables.remove.items = tables.tables.data.filter(item => item.selected); dialogs.tables.remove.first_open = true">{{$t('common.remove')}}</onyks-button>
        </BasicButtonsPanel>
        <BasicSearch v-model="tables.tables.search_phrase" :search="tables.tables.search"></BasicSearch>
        <BasicTable v-model="tables.tables"></BasicTable>
        <AddItemDialog v-model="dialogs.tables.add"></AddItemDialog>
        <EditItemDialog v-model="dialogs.tables.edit"></EditItemDialog>
        <RemoveItemsDialog v-model="dialogs.tables.remove"></RemoveItemsDialog>

        <!-- Manufacturers -->
        <SubTitle>{{ $t('common.manufacturers') }}</SubTitle>
        <BasicButtonsPanel>
            <onyks-button background="green" @click="dialogs.manufacturers.add.open = true">{{$t('common.add')}}</onyks-button>
            <onyks-button background="blue" :disabled="!(tables.manufacturers.selected == 1)" @click="dialogs.manufacturers.edit.name = dialogs.manufacturers.edit.item.name; dialogs.manufacturers.edit.open = true">{{$t('common.edit')}}</onyks-button>
            <onyks-button background="red" :disabled="!(tables.manufacturers.selected > 0)" @click="dialogs.manufacturers.remove.items = tables.manufacturers.data.filter(item => item.selected); dialogs.manufacturers.remove.first_open = true">{{$t('common.remove')}}</onyks-button>
        </BasicButtonsPanel>
        <BasicSearch v-model="tables.manufacturers.search_phrase" :search="tables.manufacturers.search"></BasicSearch>
        <BasicTable v-model="tables.manufacturers"></BasicTable>
        <AddItemDialog v-model="dialogs.manufacturers.add"></AddItemDialog>
        <EditItemDialog v-model="dialogs.manufacturers.edit"></EditItemDialog>
        <RemoveItemsDialog v-model="dialogs.manufacturers.remove"></RemoveItemsDialog>

        <!-- Suppliers -->
        <SubTitle>{{ $t('common.suppliers') }}</SubTitle>
        <BasicButtonsPanel>
            <onyks-button background="green" @click="dialogs.suppliers.add.open = true">{{$t('common.add')}}</onyks-button>
            <onyks-button background="blue" :disabled="!(tables.suppliers.selected == 1)" @click="dialogs.suppliers.edit.name = dialogs.suppliers.edit.item.name; dialogs.suppliers.edit.open = true">{{$t('common.edit')}}</onyks-button>
            <onyks-button background="red" :disabled="!(tables.suppliers.selected > 0)" @click="() =>
                {
                    dialogs.suppliers.remove.items = tables.suppliers.data.filter(item => item.selected); dialogs.suppliers.remove.first_open = true
                }">{{$t('common.remove')}}</onyks-button>
        </BasicButtonsPanel>
        <BasicSearch v-model="tables.suppliers.search_phrase" :search="tables.suppliers.search"></BasicSearch>
        <BasicTable v-model="tables.suppliers"></BasicTable>
        <AddItemDialog v-model="dialogs.suppliers.add"></AddItemDialog>
        <EditItemDialog v-model="dialogs.suppliers.edit"></EditItemDialog>
        <RemoveItemsDialog v-model="dialogs.suppliers.remove"></RemoveItemsDialog>
    </ManagerPage>
</template>

<style lang="css" scoped>
    :deep(onyks-table)
    {
        height: 600px;
    }
</style>