<script setup lang="js">
    import ElementPath from './ElementPath.vue';
    import ValueSelector from './ValueSelector.vue';
    import { computed, reactive, toRef } from 'vue';
    import { onMounted } from 'vue';
    import RepositoryModelDialog from './RepositoryModelDialog.vue';
    import { OnyksHeader } from 'onyks-web-ui-system';
    import { services, suppliers } from '@/utils/api.js';
    import UploadFiles from './UploadFiles.vue';
    import TagsSelector from './TagsSelector.vue';
    import { open_datasheet } from '../utils/tools';
    import { useValueSelector } from '@/composables/useValueSelector.js';
    import AddItemDialog from './AddItemDialog.vue';
    import EditItemDialog from './EditItemDialog.vue';
    import RemoveItemsDialog from './RemoveItemsDialog.vue';
    import { useAddItemDialog } from '@/composables/useAddItemDialog.js';
    import { useEditItemDialog } from '@/composables/useEditItemDialog.js';
    import { useRemoveItemsDialog } from '@/composables/useRemoveItemsDialog.js';
    import { i18n } from '@/utils/localization.js';
    import { OnyksToastContainer } from 'onyks-web-ui-system';
    import {usePCBModelSelector} from '@/composables/usePCBModelSelector.js';
    import PCBModelSelector from './PCBModelSelector.vue';
    import { useSuppliersSelector } from '@/composables/useSuppliersSelector.js';
    import SuppliersSelector from './SuppliersSelector.vue';
    import BasicTable from './BasicTable.vue';
    import { useBasicTable } from '@/composables/useBasicTable.js';
    import { useTagsSelector } from '@/composables/useTagsSelector.js';

    const props = defineProps(['schema'])
    const obj = defineModel({
        details: {
            manufacturer: '',
            table: '',
            suppliers: []
        }
    })

    const selectors = reactive(
    {
        manufacturer: useValueSelector(services.manufacturers, (value) => 
        {
            if(value.selected)
            {
                obj.value.details.manufacturer = value.value.name
            }
            else
            {
                obj.value.details.manufacturer = ''
            }
        }),
        tables: useValueSelector(services.tables, (value) => 
        { 
            if(value.selected)
            {
                obj.value.details.table = value.value.name
            }
            else
            {
                obj.value.details.table = ''
            }
        }),
        suppliers: useSuppliersSelector(services.suppliers),
        tags: useTagsSelector(services.tags, toRef(obj.value.details, 'tags'))
    })

    const dialogs = reactive(
    {
        tables:
        {
            add: useAddItemDialog(services.tables, i18n.global.t('tables.add'), (item) => 
            { 
                OnyksToastContainer.success(i18n.global.t('tables.added'))
                selectors.tables.search()
            }),
            edit: useEditItemDialog(services.tables, i18n.global.t('tables.edit'), (item) =>
            {
                OnyksToastContainer.success(i18n.global.t('tables.edited'))
                selectors.tables.search()
            }, () => selectors.tables.item[0]),
            remove: useRemoveItemsDialog(services.tables, i18n.global.t('tables.delete'), ['id', 'name'], (item) =>
            {
                selectors.tables.search()
            }, () => selectors.tables.item)
        },
        manufacturer:
        {
            add: useAddItemDialog(services.manufacturers, i18n.global.t('manufacturers.add'), () =>
            {
                OnyksToastContainer.success(i18n.global.t('manufacturers.added'))
                selectors.manufacturer.search()
            }),
            edit: useEditItemDialog(services.manufacturers, i18n.global.t('manufacturers.edit'), () =>
            {
                OnyksToastContainer.success(i18n.global.t('manufacturers.edited'))
                selectors.manufacturer.search()
            }, () => selectors.manufacturer.item[0]),
            remove: useRemoveItemsDialog(services.manufacturers, i18n.global.t('manufacturers.delete'), ['id', 'name'], (item) =>
            {
                selectors.manufacturer.search()
            }, () => selectors.manufacturer.item)
        },
        symbol: usePCBModelSelector(i18n.global.t('elements.select_symbol'), (item) => item.type == 'schlib' || item.type == 'dir' || item.type == 'symbol', () => 
        { 
            if(dialogs.symbol.repository.current_selected.type == 'symbol')
            {
                obj.value.details.library_path = dialogs.symbol.repository.path.join('/')
                obj.value.details.library_reference = dialogs.symbol.repository.current_selected.name
                dialogs.symbol.open = false
            }
            else
            {
                dialogs.symbol.error = i18n.global.t('elements.please_select_symbol')
            }
        }, () => { dialogs.symbol.open = false; obj.value.details.library_path = ''; obj.value.details.library_reference = ''; }),
        footprint_1: usePCBModelSelector(i18n.global.t('elements.select_footprint_no', [1]), (item) => item.type == 'pcblib' || item.type == 'dir' || item.type == 'footprint', () => 
        { 
            if(dialogs.footprint_1.repository.current_selected.type == 'footprint')
            {
                obj.value.details.footprint_path_1 = dialogs.footprint_1.repository.path.join('/')
                obj.value.details.footprint_reference_1 = dialogs.footprint_1.repository.current_selected.name
                dialogs.footprint_1.open = false
            }
            else
            {
                dialogs.footprint_1.error = i18n.global.t('elements.please_select_footprint')
            }
        }, () => { dialogs.footprint_1.open = false; obj.value.details.footprint_path_1 = ''; obj.value.details.footprint_reference_1 = ''; }),
        footprint_2: usePCBModelSelector(i18n.global.t('elements.select_footprint_no', [2]), (item) => item.type == 'pcblib' || item.type == 'dir' || item.type == 'footprint', () => 
        { 
            if(dialogs.footprint_2.repository.current_selected.type == 'footprint')
            {
                obj.value.details.footprint_path_2 = dialogs.footprint_2.repository.path.join('/')
                obj.value.details.footprint_reference_2 = dialogs.footprint_2.repository.current_selected.name
                dialogs.footprint_2.open = false
            }
            else
            {
                dialogs.footprint_2.error = i18n.global.t('elements.please_select_footprint')
            }
        }, () => { dialogs.footprint_2.open = false; obj.value.details.footprint_path_2 = ''; obj.value.details.footprint_reference_2 = ''; }),
        footprint_3: usePCBModelSelector(i18n.global.t('elements.select_footprint_no', [3]), (item) => item.type == 'pcblib' || item.type == 'dir' || item.type == 'footprint', () => 
        { 
            if(dialogs.footprint_3.repository.current_selected.type == 'footprint')
            {
                obj.value.details.footprint_path_3 = dialogs.footprint_3.repository.path.join('/')
                obj.value.details.footprint_reference_3 = dialogs.footprint_3.repository.current_selected.name
                dialogs.footprint_3.open = false
            }
            else
            {
                dialogs.footprint_3.error = i18n.global.t('elements.please_select_footprint')
            }
        }, () => { dialogs.footprint_3.open = false; obj.value.details.footprint_path_3 = ''; obj.value.details.footprint_reference_3 = ''; }),
        suppliers:
        {
            add: useAddItemDialog(services.suppliers, i18n.global.t('suppliers.add'), (item) => 
            { 
                OnyksToastContainer.success(i18n.global.t('tables.added'))
                selectors.suppliers.search()
            }),
            edit: useEditItemDialog(services.suppliers, i18n.global.t('suppliers.edit'), (item) =>
            {
                OnyksToastContainer.success(i18n.global.t('tables.edited'))
                selectors.suppliers.search()
            }, () => selectors.suppliers.item[0]),
            remove: useRemoveItemsDialog(services.suppliers, i18n.global.t('suppliers.delete'), ['id', 'name'], (item) =>
            {
                selectors.suppliers.search()
            }, () => selectors.suppliers.item)
        }
    })

    const tables = reactive({
        suppliers: computed(() => 
        {
            let tab = []
            Object.keys(obj.value.details.suppliers).forEach(key => 
            {
                tab.push(obj.value.details.suppliers[key])
            })
            return tab
        }),
    })

    onMounted(async () => 
    {
        dialogs.symbol.init()
        dialogs.footprint_1.init()
        dialogs.footprint_2.init()
        dialogs.footprint_3.init()
        selectors.manufacturer.init()
        selectors.tables.init()
        selectors.suppliers.init()
        selectors.tags.init()
    })
</script>

<template>
    <onyks-container gap="m">
        <!-- Basic information -->
        <onyks-header level="4">{{ $t('elements.basic_information') }}</onyks-header>
        <onyks-container type="grid" cols="2" mobile-breakpoint="600" gap="m">

            <onyks-container gap="m">

                <onyks-header level="6" v-if="props.schema == 'details' || props.schema == 'edit'">{{ $t('common.uuid') }}</onyks-header>
                <onyks-textfield v-if="props.schema == 'details' || props.schema == 'edit'" v-model="obj.details.uuid" disabled></onyks-textfield>

                <onyks-header level="6">{{ $t('elements.part_name') }}</onyks-header>
                <onyks-textfield v-model="obj.details.part_name" :disabled="props.schema == 'details'"></onyks-textfield>

                <onyks-header level="6">{{ $t('elements.manufacturer') }}</onyks-header>
                <onyks-textfield v-if="props.schema == 'details'" v-model="obj.details.manufacturer" :disabled="props.schema == 'details'"></onyks-textfield>
                <ValueSelector v-if="props.schema != 'details'" v-model="selectors.manufacturer" v-model:value="obj.details.manufacturer"></ValueSelector>

                <onyks-container gap="m" type="grid" cols="3" mobile-breakpoint="900" v-if="props.schema != 'details'">
                    <onyks-button class="selector-btns" background="green" @click="dialogs.manufacturer.add.open = true">{{ $t('common.add') }}</onyks-button>
                    <onyks-button @click="dialogs.manufacturer.edit.name = obj.details.manufacturer; dialogs.manufacturer.edit.open = true" class="selector-btns" background="blue" :disabled="!obj.details.manufacturer">{{ $t('common.edit') }}</onyks-button>
                    <onyks-button @click="dialogs.manufacturer.remove.first_open = true" class="selector-btns" background="red" :disabled="!obj.details.manufacturer">{{ $t('common.remove') }}</onyks-button>
                </onyks-container>

                <AddItemDialog v-model="dialogs.manufacturer.add"></AddItemDialog>
                <EditItemDialog v-model="dialogs.manufacturer.edit"></EditItemDialog>
                <RemoveItemsDialog v-model="dialogs.manufacturer.remove"></RemoveItemsDialog>

                <onyks-header level="6">{{ $t('elements.value') }}</onyks-header>
                <onyks-textfield v-model="obj.details.value" :disabled="props.schema == 'details'"></onyks-textfield>

            </onyks-container>
            <onyks-container gap="m">

                <onyks-header level="6">{{ $t('elements.availability') }}</onyks-header>
                <onyks-textfield v-model="obj.details.availability" :disabled="props.schema == 'details'"></onyks-textfield>

                <onyks-header level="6" v-if="props.schema == 'details' || props.schema == 'edit'">{{ $t('common.created_at') }}</onyks-header>
                <onyks-textfield disabled v-model="obj.details.created_at" v-if="props.schema == 'details' || props.schema == 'edit'" :disabled="props.schema == 'details'"></onyks-textfield>

                <onyks-header level="6">{{ $t('elements.table') }}</onyks-header>
                <onyks-textfield v-if="props.schema == 'details'" v-model="obj.details.table" :disabled="props.schema == 'details'"></onyks-textfield>
                <ValueSelector v-if="props.schema != 'details'" v-model="selectors.tables" v-model:value="obj.details.table"></ValueSelector>

                <onyks-container gap="m" type="grid" cols="3" mobile-breakpoint="900" v-if="props.schema != 'details'">
                    <onyks-button @click="dialogs.tables.add.open = true" class="selector-btns" background="green">{{ $t('common.add') }}</onyks-button>
                    <onyks-button @click="dialogs.tables.edit.name = obj.details.table; dialogs.tables.edit.open = true" class="selector-btns" background="blue" :disabled="!obj.details.table">{{ $t('common.edit') }}</onyks-button>
                    <onyks-button @click="dialogs.tables.remove.first_open = true" class="selector-btns" background="red" :disabled="!obj.details.table">{{ $t('common.remove') }}</onyks-button>
                </onyks-container>

                <AddItemDialog v-model="dialogs.tables.add"></AddItemDialog>
                <EditItemDialog v-model="dialogs.tables.edit"></EditItemDialog>
                <RemoveItemsDialog v-model="dialogs.tables.remove"></RemoveItemsDialog>
            </onyks-container>

        </onyks-container>
        <onyks-header level="6">{{ $t('elements.description') }}</onyks-header>
        <onyks-textarea maxlength="1024" v-model="obj.details.description" size="m" placeholder="" resize="none" :disabled="props.schema == 'details'"></onyks-textarea>

        <!-- Symbol & Footprints -->
        <onyks-header level="4">{{ $t('elements.symbols_and_footprints') }}</onyks-header>
        <onyks-container type="grid" cols="2" mobile-breakpoint="900" gap="m">
            <onyks-container gap="m" cols="1" type="grid">
                <onyks-header level="6">{{ $t('elements.symbol') }}</onyks-header>
                <ElementPath class="element-path" v-model:path="obj.details.library_path" v-model:obj="obj.details.library_reference"></ElementPath>
                <onyks-container type="group" gap="m" v-if="props.schema != 'details'">
                    <onyks-button background="blue" @click="dialogs.symbol.open = true">{{ $t('common.select') }}</onyks-button>
                    <onyks-button background="red" @click="obj.details.library_path = ''; obj.details.library_reference = ''">{{ $t('common.reset') }}</onyks-button>
                </onyks-container>

                <onyks-header level="6">{{ $t('elements.footprint_no_2') }}</onyks-header>
                <ElementPath class="element-path" v-model:path="obj.details.footprint_path_2" v-model:obj="obj.details.footprint_reference_2"></ElementPath>
                <onyks-container type="group" gap="m" v-if="props.schema != 'details'">
                    <onyks-button background="purple" @click="dialogs.footprint_2.open = true">{{ $t('common.select') }}</onyks-button>
                    <onyks-button background="red" @click="obj.details.footprint_path_2 = ''; obj.details.footprint_reference_2 = ''">{{ $t('common.reset') }}</onyks-button>
                </onyks-container>

            </onyks-container>
            <onyks-container gap="m" cols="1" type="grid">
                <onyks-header level="6">{{ $t('elements.footprint_no_1') }}</onyks-header>
                <ElementPath class="element-path" v-model:path="obj.details.footprint_path_1" v-model:obj="obj.details.footprint_reference_1"></ElementPath>

                <onyks-container type="group" gap="m" v-if="props.schema != 'details'">
                    <onyks-button background="purple" @click="dialogs.footprint_1.open = true">{{ $t('common.select') }}</onyks-button>
                    <onyks-button background="red" @click="obj.details.footprint_path_1 = ''; obj.details.footprint_reference_1 = ''">{{ $t('common.reset') }}</onyks-button>
                </onyks-container>

                <onyks-header level="6">{{ $t('elements.footprint_no_3') }}</onyks-header>
                <ElementPath class="element-path" v-model:path="obj.details.footprint_path_3" v-model:obj="obj.details.footprint_reference_3"></ElementPath>
                <onyks-container type="group" gap="m" v-if="props.schema != 'details'">
                    <onyks-button background="purple" @click="dialogs.footprint_3.open = true">{{ $t('common.select') }}</onyks-button>
                    <onyks-button background="red" @click="obj.details.footprint_path_3 = ''; obj.details.footprint_reference_3 = ''">{{ $t('common.reset') }}</onyks-button>
                </onyks-container>  
            </onyks-container>

            <PCBModelSelector v-model="dialogs.symbol"></PCBModelSelector>
            <PCBModelSelector v-model="dialogs.footprint_1"></PCBModelSelector>
            <PCBModelSelector v-model="dialogs.footprint_2"></PCBModelSelector>
            <PCBModelSelector v-model="dialogs.footprint_3"></PCBModelSelector>
        </onyks-container>

        <onyks-header level="4">{{ $t('elements.other_details') }}</onyks-header>
        <onyks-header level="6">{{ $t('elements.suppliers_codes') }}</onyks-header>

        <onyks-table v-if="props.schema == 'details' && Object.keys(obj.details.suppliers).length > 0" :columns="[{'label':$t('suppliers.supplier_name'), 'key': 'name'},{'label':$t('suppliers.suppliers_code'), 'key': 'value'}]" :data="tables.suppliers"></onyks-table>

        <onyks-text v-if="props.schema == 'details' && Object.keys(obj.details.suppliers).length == 0">{{ $t('elements.no_suppliers_codes_defined') }}</onyks-text>

        <SuppliersSelector v-model="selectors.suppliers" v-model:value="obj.details.suppliers" v-if="props.schema != 'details'"></SuppliersSelector>

        <onyks-container gap="m" type="grid" cols="3" mobile-breakpoint="900" v-if="props.schema != 'details'" style="max-width: 500px;">
            <onyks-button @click="dialogs.suppliers.add.open = true" class="selector-btns" background="green">{{ $t('common.add') }}</onyks-button>
            <onyks-button @click="dialogs.suppliers.edit.name = obj.details.table; dialogs.suppliers.edit.open = true" class="selector-btns" background="blue" :disabled="!dialogs.suppliers.edit.item">{{ $t('common.edit') }}</onyks-button>
            <onyks-button @click="dialogs.suppliers.remove.first_open = true" class="selector-btns" background="red" :disabled="!dialogs.suppliers.remove.items.length">{{ $t('common.remove') }}</onyks-button>
        </onyks-container>

        <AddItemDialog v-model="dialogs.suppliers.add"></AddItemDialog>
        <EditItemDialog v-model="dialogs.suppliers.edit"></EditItemDialog>
        <RemoveItemsDialog v-model="dialogs.suppliers.remove"></RemoveItemsDialog>

        <onyks-header level="6">{{ $t('common.datasheets') }}</onyks-header>

        <onyks-container v-if="props.schema == 'details'" gap="m" type="group">
            <onyks-tag background="yellow" @click="() => open_datasheet(x.uuid)" icon="F756" v-for="x in obj.details.datasheets" :key="x.name" class="tag">{{ x.name }}</onyks-tag>
        </onyks-container>

        <UploadFiles v-else  v-model:datasheets="obj.details.datasheets" v-model:files="obj.files"></UploadFiles>

        <onyks-header level="6">{{ $t('common.tags') }}</onyks-header>

        <TagsSelector v-model:tags="obj.details.tags" v-model="selectors.tags" v-if="props.schema != 'details'"></TagsSelector>
        <onyks-container gap="m" type="group" v-else-if="obj.details.tags.length > 0">
            <onyks-tag v-for="tag in obj.details.tags" :key="tag">{{ tag }}</onyks-tag>
        </onyks-container>
        <onyks-text v-else>{{ $t('common.no_tags_defined') }}</onyks-text>

    </onyks-container>
</template>

<style>
    onyks-textarea
    {
        height: 250px;
    }

    .selector-btns
    {
        width: 100%;
    }

    .tag
    {
        min-width: 100px;
    }
</style>