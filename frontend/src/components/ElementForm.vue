<script setup lang="js">
    import ElementPath from './ElementPath.vue';
    import ValueSelector from './ValueSelector.vue';
    import { reactive, toRef } from 'vue';
    import { onMounted } from 'vue';
    import { useRepositoryModelDialog, useValueSelector, useSupplierSelector } from '../utils/tools';
    import RepositoryModelDialog from './RepositoryModelDialog.vue';
    import { OnyksHeader } from 'onyks-web-ui-system';
    import { services } from '@/utils/api.js';
    import SupplierSelector from './SupplierSelector.vue';
    import UploadFiles from './UploadFiles.vue';
    import TagsSelector from './TagsSelector.vue';
    import { ref } from 'vue';
    import { useTagsSelector } from '../utils/tools';

    const props = defineProps(['schema'])
    const obj = defineModel()

    const selectors = reactive(
    {
        manufacturer: useValueSelector(services.manufacturers, (value) => 
        { 

            console.log()
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
        suppliers: useSupplierSelector(services.suppliers),
        tags: useTagsSelector(services.tags, toRef(obj.value.details, 'tags'))
    })

    const dialogs = reactive(
    {
        symbol: useRepositoryModelDialog('Select Symbol', (item) => item.type == 'schlib' || item.type == 'dir' || item.type == 'symbol', () => 
        { 
            if(dialogs.symbol.repository.currentSelected.type == 'symbol')
            {
                obj.value.details.libraryPath = dialogs.symbol.repository.path.join('/')
                obj.value.details.libraryReference = dialogs.symbol.repository.currentSelected.name
                dialogs.symbol.open = false
            }
            else
            {
                dialogs.symbol.error = 'Please select a symbol'
            }
        }, () => { dialogs.symbol.open = false; obj.value.details.libraryPath = ''; obj.value.details.libraryReference = ''; }),
        footprintNo1: useRepositoryModelDialog('Select Footprint No 1', (item) => item.type == 'pcblib' || item.type == 'dir' || item.type == 'footprint', () => 
        { 
            if(dialogs.footprintNo1.repository.currentSelected.type == 'footprint')
            {
                obj.value.details.footprintPathNo1 = dialogs.footprintNo1.repository.path.join('/')
                obj.value.details.footprintReferenceNo1 = dialogs.footprintNo1.repository.currentSelected.name
                dialogs.footprintNo1.open = false
            }
            else
            {
                dialogs.footprintNo1.error = 'Please select a footprint'
            }
        }, () => { dialogs.footprintNo1.open = false; obj.value.details.footprintPathNo1 = ''; obj.value.details.footprintReferenceNo1 = ''; }),
        footprintNo2: useRepositoryModelDialog('Select Footprint No 2', (item) => item.type == 'pcblib' || item.type == 'dir' || item.type == 'footprint', () => 
        { 
            if(dialogs.footprintNo2.repository.currentSelected.type == 'footprint')
            {
                obj.value.details.footprintPathNo2 = dialogs.footprintNo2.repository.path.join('/')
                obj.value.details.footprintReferenceNo2 = dialogs.footprintNo2.repository.currentSelected.name
                dialogs.footprintNo2.open = false
            }
            else
            {
                dialogs.footprintNo2.error = 'Please select a footprint'
            }
        }, () => { dialogs.footprintNo2.open = false; obj.value.details.footprintPathNo2 = ''; obj.value.details.footprintReferenceNo2 = ''; }),
        footprintNo3: useRepositoryModelDialog('Select Footprint No 3', (item) => item.type == 'pcblib' || item.type == 'dir' || item.type == 'footprint', () => 
        { 
            if(dialogs.footprintNo3.repository.currentSelected.type == 'footprint')
            {
                obj.value.details.footprintPathNo3 = dialogs.footprintNo3.repository.path.join('/')
                obj.value.details.footprintReferenceNo3 = dialogs.footprintNo3.repository.currentSelected.name
                dialogs.footprintNo3.open = false
            }
            else
            {
                dialogs.footprintNo3.error = 'Please select a footprint'
            }
        }, () => { dialogs.footprintNo3.open = false; obj.value.details.footprintPathNo3 = ''; obj.value.details.footprintReferenceNo3 = ''; })
    })


    onMounted(async () => 
    {
        dialogs.symbol.init()
        dialogs.footprintNo1.init()
        dialogs.footprintNo2.init()
        dialogs.footprintNo3.init()
        selectors.manufacturer.init()
        selectors.tables.init()
        selectors.suppliers.init()
        selectors.tags.init()
    })
</script>

<template>
    <onyks-container gap="m">
        <onyks-header level="4">Basic information</onyks-header>

        <onyks-container type="grid" cols="2" mobile-breakpoint="900" gap="m">

            <onyks-container gap="m">

                <onyks-header level="6" v-if="props.schema == 'details' || props.schema == 'edit'">UUID</onyks-header>
                <onyks-textfield v-if="props.schema == 'details' || props.schema == 'edit'" v-model="obj.details.uuid" disabled></onyks-textfield>

                <onyks-header level="6">Part Name</onyks-header>
                <onyks-textfield v-model="obj.details.partName" :disabled="props.schema == 'details'"></onyks-textfield>

                <onyks-header level="6">Manufacturer</onyks-header>
                <onyks-textfield v-if="props.schema == 'details'" v-model="obj.details.manufacturer" :disabled="props.schema == 'details'"></onyks-textfield>
                <ValueSelector v-if="props.schema != 'details'" v-model="selectors.manufacturer" v-model:value="obj.details.manufacturer"></ValueSelector>

                <onyks-header level="6">Value</onyks-header>
                <onyks-textfield v-model="obj.details.value" :disabled="props.schema == 'details'"></onyks-textfield>

            </onyks-container>
            <onyks-container gap="m">

                <onyks-header level="6">Availability</onyks-header>
                <onyks-textfield v-model="obj.details.availability" :disabled="props.schema == 'details'"></onyks-textfield>

                <onyks-header level="6" v-if="props.schema == 'details' || props.schema == 'edit'">Created At</onyks-header>
                <onyks-textfield disabled v-model="obj.details.createdAt" v-if="props.schema == 'details' || props.schema == 'edit'" :disabled="props.schema == 'details'"></onyks-textfield>

                <onyks-header level="6">Table</onyks-header>
                <onyks-textfield v-if="props.schema == 'details'" v-model="obj.details.table" :disabled="props.schema == 'details'"></onyks-textfield>
                <ValueSelector v-if="props.schema != 'details'" v-model="selectors.tables" v-model:value="obj.details.table"></ValueSelector>

            </onyks-container>

        </onyks-container>
        <onyks-header level="6">Description</onyks-header>
        <onyks-textarea maxlength="1024" v-model="obj.details.description" size="m" placeholder="" resize="none" :disabled="props.schema == 'details'"></onyks-textarea>

        <onyks-header level="4">Symbol & Footprints</onyks-header>

        <onyks-container type="grid" cols="2" mobile-breakpoint="900" gap="m">
            <onyks-container gap="m" cols="1" type="grid">
                <onyks-header level="6">Symbol</onyks-header>
                <ElementPath class="element-path" v-model:path="obj.details.libraryPath" v-model:obj="obj.details.libraryReference"></ElementPath>
                <onyks-container type="group" gap="m" v-if="props.schema != 'details'">
                    <onyks-button background="blue" @click="dialogs.symbol.open = true">Select</onyks-button>
                    <onyks-button background="red" @click="obj.details.libraryPath = ''; obj.details.libraryReference = ''">Reset</onyks-button>
                </onyks-container>

                <onyks-header level="6">Footprint No 2</onyks-header>
                <ElementPath class="element-path" v-model:path="obj.details.footprintPathNo2" v-model:obj="obj.details.footprintReferenceNo2"></ElementPath>
                <onyks-container type="group" gap="m" v-if="props.schema != 'details'">
                    <onyks-button background="purple" @click="dialogs.footprintNo2.open = true">Select</onyks-button>
                    <onyks-button background="red" @click="obj.details.footprintPathNo2 = ''; obj.details.footprintReferenceNo2 = ''">Reset</onyks-button>
                </onyks-container>

            </onyks-container>
            <onyks-container gap="m" cols="1" type="grid">
                <onyks-header level="6">Footprint No 1</onyks-header>
                <ElementPath class="element-path" v-model:path="obj.details.footprintPathNo1" v-model:obj="obj.details.footprintReferenceNo1"></ElementPath>

                <onyks-container type="group" gap="m" v-if="props.schema != 'details'">
                    <onyks-button background="purple" @click="dialogs.footprintNo1.open = true">Select</onyks-button>
                    <onyks-button background="red" @click="obj.details.footprintPathNo1 = ''; obj.details.footprintReferenceNo1 = ''">Reset</onyks-button>
                </onyks-container>

                <onyks-header level="6">Footprint No 3</onyks-header>
                <ElementPath class="element-path" v-model:path="obj.details.footprintPathNo3" v-model:obj="obj.details.footprintReferenceNo3"></ElementPath>
                <onyks-container type="group" gap="m" v-if="props.schema != 'details'">
                    <onyks-button background="purple" @click="dialogs.footprintNo3.open = true">Select</onyks-button>
                    <onyks-button background="red" @click="obj.details.footprintPathNo3 = ''; obj.details.footprintReferenceNo3 = ''">Reset</onyks-button>
                </onyks-container>  
            </onyks-container>

            <RepositoryModelDialog v-model="dialogs.symbol"></RepositoryModelDialog>
            <RepositoryModelDialog v-model="dialogs.footprintNo1"></RepositoryModelDialog>
            <RepositoryModelDialog v-model="dialogs.footprintNo2"></RepositoryModelDialog>
            <RepositoryModelDialog v-model="dialogs.footprintNo3"></RepositoryModelDialog>
        </onyks-container>

        <onyks-header level="4">Other details</onyks-header>
        <onyks-header level="6">Suppliers</onyks-header>

        <onyks-container type="stack" gap="m" v-if="props.schema == 'details' && Object.keys(obj.details.suppliers).length > 0" padding="m">
            <onyks-container type="group" gap="m" v-for="(value, key) in obj.details.suppliers" :key="key" align="center">
                <onyks-text size="m">{{ value.name }}</onyks-text>
                <onyks-tag background="red">{{ value.value }}</onyks-tag>
            </onyks-container>
        </onyks-container>

        <onyks-text v-if="props.schema == 'details'">No suppliers defined</onyks-text>

        <SupplierSelector v-model="selectors.suppliers" v-model:value="obj.details.suppliers" v-if="props.schema != 'details'"></SupplierSelector>

        <onyks-header level="6">Datasheets</onyks-header>

        <!-- <UploadFiles v-model:datasheets="element.datasheets"></UploadFiles> -->

        <onyks-header level="6">Tags</onyks-header>
        <TagsSelector v-model:tags="obj.details.tags" v-model="selectors.tags" v-if="props.schema != 'details'"></TagsSelector>
        <onyks-container gap="m" type="group" v-else-if="obj.details.tags.length > 0">
            <onyks-tag v-for="tag in obj.details.tags" :key="tag">{{ tag }}</onyks-tag>
        </onyks-container>
        <onyks-text v-else>No tags defined</onyks-text>


    </onyks-container>
</template>

<style>
    onyks-textarea
    {
        height: 250px;
    }
</style>