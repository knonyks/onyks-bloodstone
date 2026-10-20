<script setup lang="js">
    import ElementPath from './ElementPath.vue';
    import ValueSelector from './ValueSelector.vue';
    import { reactive } from 'vue';
    import { onMounted } from 'vue';
    import { useRepositoryModelDialog, useValueSelector, useSupplierSelector } from '../utils/tools';
    import RepositoryModelDialog from './RepositoryModelDialog.vue';
    import { OnyksHeader } from 'onyks-web-ui-system';
    import { services } from '@/utils/api.js';
    import SupplierSelector from './SupplierSelector.vue';
    import CreateElementFiles from './CreateElementFiles.vue';

    const props = defineProps(['schema'])
    const element = defineModel('element');

    const selectors = reactive(
    {
        manufacturer: useValueSelector(services.manufacturers, (value) => 
        { 
            if(value.selected)
            {
                element.value.manufacturer = value.value.name
            }
            else
            {
                element.value.manufacturer = ''
            }
        }),
        tables: useValueSelector(services.tables, (value) => 
        { 
            if(value.selected)
            {
                element.value.table = value.value.name
            }
            else
            {
                element.value.table = ''
            }
        }),
        suppliers: useSupplierSelector(services.suppliers)
    })

    const dialogs = reactive(
    {
        symbol: useRepositoryModelDialog('Select Symbol', (item) => item.type == 'schlib' || item.type == 'dir' || item.type == 'symbol', () => 
        { 
            if(dialogs.symbol.repository.currentSelected.type == 'symbol')
            {
                element.value.libraryPath = dialogs.symbol.repository.path.join('/')
                element.value.libraryReference = dialogs.symbol.repository.currentSelected.name
                dialogs.symbol.open = false
            }
            else
            {
                dialogs.symbol.error = 'Please select a symbol'
            }
        }, () => { dialogs.symbol.open = false; element.value.libraryPath = ''; element.value.libraryReference = ''; }),
        footprintNo1: useRepositoryModelDialog('Select Footprint No 1', (item) => item.type == 'pcblib' || item.type == 'dir' || item.type == 'footprint', () => 
        { 
            if(dialogs.footprintNo1.repository.currentSelected.type == 'footprint')
            {
                element.value.footprintPathNo1 = dialogs.footprintNo1.repository.path.join('/')
                element.value.footprintReferenceNo1 = dialogs.footprintNo1.repository.currentSelected.name
                dialogs.footprintNo1.open = false
            }
            else
            {
                dialogs.footprintNo1.error = 'Please select a footprint'
            }
        }, () => { dialogs.footprintNo1.open = false; element.value.footprintPathNo1 = ''; element.value.footprintReferenceNo1 = ''; }),
        footprintNo2: useRepositoryModelDialog('Select Footprint No 2', (item) => item.type == 'pcblib' || item.type == 'dir' || item.type == 'footprint', () => 
        { 
            if(dialogs.footprintNo2.repository.currentSelected.type == 'footprint')
            {
                element.value.footprintPathNo2 = dialogs.footprintNo2.repository.path.join('/')
                element.value.footprintReferenceNo2 = dialogs.footprintNo2.repository.currentSelected.name
                dialogs.footprintNo2.open = false
            }
            else
            {
                dialogs.footprintNo2.error = 'Please select a footprint'
            }
        }, () => { dialogs.footprintNo2.open = false; element.value.footprintPathNo2 = ''; element.value.footprintReferenceNo2 = ''; }),
        footprintNo3: useRepositoryModelDialog('Select Footprint No 3', (item) => item.type == 'pcblib' || item.type == 'dir' || item.type == 'footprint', () => 
        { 
            if(dialogs.footprintNo3.repository.currentSelected.type == 'footprint')
            {
                element.value.footprintPathNo3 = dialogs.footprintNo3.repository.path.join('/')
                element.value.footprintReferenceNo3 = dialogs.footprintNo3.repository.currentSelected.name
                dialogs.footprintNo3.open = false
            }
            else
            {
                dialogs.footprintNo3.error = 'Please select a footprint'
            }
        }, () => { dialogs.footprintNo3.open = false; element.value.footprintPathNo3 = ''; element.value.footprintReferenceNo3 = ''; })
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
    })
</script>

<template>
    <onyks-container gap="m">
        <onyks-header level="4">Basic information</onyks-header>

        <onyks-container type="grid" cols="2" mobile-breakpoint="900" gap="m">
            
            <onyks-container gap="m">

                <onyks-header level="6" v-if="props.schema == 'details'">UUID</onyks-header>
                <onyks-textfield v-if="props.schema == 'details'" v-model="element.uuid" :disabled="props.schema == 'details'"></onyks-textfield>

                <onyks-header level="6">Part Name</onyks-header>
                <onyks-textfield v-model="element.partName" :disabled="props.schema == 'details'"></onyks-textfield>

                <onyks-header level="6">Manufacturer</onyks-header>
                <onyks-textfield v-if="props.schema == 'details'" v-model="element.manufacturer" :disabled="props.schema == 'details'"></onyks-textfield>
                <ValueSelector v-if="props.schema != 'details'" v-model="selectors.manufacturer" v-model:value="element.manufacturer" :disabled="props.schema == 'details'"></ValueSelector>

                <onyks-header level="6">Value</onyks-header>
                <onyks-textfield v-model="element.value" :disabled="props.schema == 'details'"></onyks-textfield>

            </onyks-container>
            <onyks-container gap="m">

                <onyks-header level="6">Availability</onyks-header>
                <onyks-textfield v-model="element.availability" :disabled="props.schema == 'details'"></onyks-textfield>

                <onyks-header level="6" v-if="props.schema == 'details' || props.schema == 'edit'">Created At</onyks-header>
                <onyks-textfield disabled v-model="element.createdAt" v-if="props.schema == 'details' || props.schema == 'edit'" :disabled="props.schema == 'details'"></onyks-textfield>

                <onyks-header level="6">Table</onyks-header>
                <onyks-textfield v-if="props.schema == 'details'" v-model="element.table" :disabled="props.schema == 'details'"></onyks-textfield>
                <ValueSelector v-if="props.schema != 'details'" v-model="selectors.tables" v-model:value="element.table" :disabled="props.schema == 'details'"></ValueSelector>

            </onyks-container>

        </onyks-container>
        <onyks-header level="6">Description</onyks-header>
        <onyks-textarea v-model="element.description" size="m" placeholder="" resize="none" :disabled="props.schema == 'details'"></onyks-textarea>

        <onyks-header level="4">Symbol & Footprints</onyks-header>

        <onyks-container type="grid" cols="2" mobile-breakpoint="900" gap="m">
            <onyks-container gap="m" cols="1" type="grid">
                <onyks-header level="6">Symbol</onyks-header>
                <ElementPath class="element-path" v-model:path="element.libraryPath" v-model:obj="element.libraryReference"></ElementPath>
                <onyks-container type="group" gap="m" v-if="props.schema != 'details'">
                    <onyks-button background="blue" @click="dialogs.symbol.open = true">Select</onyks-button>
                    <onyks-button background="red" @click="element.libraryPath = ''; element.libraryReference = ''">Reset</onyks-button>
                </onyks-container>

                
                <onyks-header level="6">Footprint No 2</onyks-header>
                <ElementPath class="element-path" v-model:path="element.footprintPathNo2" v-model:obj="element.footprintReferenceNo2"></ElementPath>
                <onyks-container type="group" gap="m" v-if="props.schema != 'details'">
                    <onyks-button background="purple" @click="dialogs.footprintNo2.open = true">Select</onyks-button>
                    <onyks-button background="red" @click="element.footprintPathNo2 = ''; element.footprintReferenceNo2 = ''">Reset</onyks-button>
                </onyks-container>


            </onyks-container>
            <onyks-container gap="m" cols="1" type="grid">
                <onyks-header level="6">Footprint No 1</onyks-header>
                <ElementPath class="element-path" v-model:path="element.footprintPathNo1" v-model:obj="element.footprintReferenceNo1"></ElementPath>
                
                <onyks-container type="group" gap="m" v-if="props.schema != 'details'">
                    <onyks-button background="purple" @click="dialogs.footprintNo1.open = true">Select</onyks-button>
                    <onyks-button background="red" @click="element.footprintPathNo1 = ''; element.footprintReferenceNo1 = ''">Reset</onyks-button>
                </onyks-container>
                
                
                <onyks-header level="6">Footprint No 3</onyks-header>
                <ElementPath class="element-path" v-model:path="element.footprintPathNo3" v-model:obj="element.footprintReferenceNo3"></ElementPath>
                <onyks-container type="group" gap="m" v-if="props.schema != 'details'">
                    <onyks-button background="purple" @click="dialogs.footprintNo3.open = true">Select</onyks-button>
                    <onyks-button background="red" @click="element.footprintPathNo3 = ''; element.footprintReferenceNo3 = ''">Reset</onyks-button>
                </onyks-container>  
            </onyks-container>
            
            <RepositoryModelDialog v-model="dialogs.symbol"></RepositoryModelDialog>
            <RepositoryModelDialog v-model="dialogs.footprintNo1"></RepositoryModelDialog>
            <RepositoryModelDialog v-model="dialogs.footprintNo2"></RepositoryModelDialog>
            <RepositoryModelDialog v-model="dialogs.footprintNo3"></RepositoryModelDialog>
        </onyks-container>
        <onyks-header level="6">Suppliers</onyks-header>

        <onyks-container type="group" gap="m" v-if="props.schema == 'details'">
            <onyks-text v-for="(value, key) in element.suppliers" :key="key">{{ key }}: {{ value }}</onyks-text>
        </onyks-container>

        <SupplierSelector v-model="selectors.suppliers" v-model:value="element.suppliers" v-else></SupplierSelector>

    </onyks-container>
</template>

<style>

</style>