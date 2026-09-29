<script setup>
    import { services } from '@/utils/api.js';
    import ValueSelector from './ValueSelector.vue';
    import { ref } from 'vue';
    import SuppliersSelector from './SuppliersSelector.vue';

    const props = defineProps({
        type: 
        {
            type: String,
            required: true,
            default: 'create'
        }
    })

    const model = defineModel({
        uuid: '',
        partName: '',
        value: '',
        availability: '',
        description: '',
        manufacturer: '',
        table: '',
        suppliers: {},
    })
    
    const manufacturerSelector = ref(null)
    const tableSelector = ref(null)
    const suppliersSelector = ref(null)
    const suppliersNames = ref({})

    const init = async () =>
    {
        if(props.type === 'details')
        {
            for(const supplierId in model.value.suppliers)
            {
                console.log(supplierId)
                suppliersNames.value[supplierId] = (await services.suppliers.get(supplierId)).data.name
            }
        }
        else
        {
            await manufacturerSelector.value.init()
            await tableSelector.value.init()
            await suppliersSelector.value.init()
        }
    }

    defineExpose({init})
</script>

<template>
    <onyks-container gap="m" type="grid" cols="2" mobile-breakpoint="800">
        <onyks-card title="Basic information" size="xl" cols="2">
            <onyks-container gap="m" type="grid" cols="2" mobile-breakpoint="800">
                <onyks-container gap="m">

                    <onyks-header level="6" v-if="props.type == 'details' || props.type == 'edit'">UUID</onyks-header>
                    <onyks-textfield v-model="model.uuid" disabled v-if="props.type == 'details' || props.type == 'edit'"></onyks-textfield>
                    
                    <onyks-header level="6">Part name</onyks-header>
                    <onyks-textfield v-model="model.partName" placeholder="e.g. Resistor 2k22 Ohm SMD" :disabled="props.type === 'details'" />
                    
                    <onyks-header level="6" v-if="props.type == 'details' || props.type == 'edit'">Created At</onyks-header>
                    <onyks-textfield v-model="model.createdAt" disabled v-if="props.type == 'details' || props.type == 'edit'"></onyks-textfield>
                
                </onyks-container>
                <onyks-container gap="m">
                    
                    <onyks-header level="6">Value</onyks-header>
                    <onyks-textfield v-model="model.value" :disabled="props.type === 'details'" ></onyks-textfield>

                    <onyks-header level="6">Availability</onyks-header>
                    <onyks-textfield v-model="model.availability" :disabled="props.type === 'details'" ></onyks-textfield>
                
                </onyks-container>
                <onyks-container cols="2" gap="m">
                    
                    <onyks-header level="6">Description</onyks-header>
                    <onyks-textarea :disabled="props.type === 'details'" v-model="model.description" placeholder="e.g 2k22 Ohm SMD resistor" size="m" resize="none"></onyks-textarea>
                
                </onyks-container>
            </onyks-container>
        </onyks-card>

        <onyks-card title="Manufacturer and destination table" cols="2" size="xl">
            <onyks-container gap="m" type="grid" cols="2" mobile-breakpoint="800">
                <onyks-container gap="m">
                    <onyks-container gap="m" type="group">
                        <onyks-header level="6">Manufacturer</onyks-header>
                        <onyks-text>{{ model.manufacturer != ''? model.manufacturer:'Undefined' }}</onyks-text>
                    </onyks-container>
                    <ValueSelector v-if="props.type !== 'details'" ref="manufacturerSelector" v-model="model.manufacturer" :action="services.manufacturers.list"></ValueSelector>
                </onyks-container>
                <onyks-container cols="1" gap="m">
                    <onyks-container gap="m" type="group">
                        <onyks-header level="6">Table</onyks-header>
                        <onyks-text>{{ model.table != ''? model.table:'Undefined' }}</onyks-text>
                    </onyks-container>
                    <ValueSelector v-if="props.type !== 'details'" ref="tableSelector" v-model="model.table" :action="services.tables.list"></ValueSelector>
                </onyks-container>
            </onyks-container>
        </onyks-card>

        <onyks-card title="Symbol & Footprints" cols="2" size="xl">
            <onyks-container gap="m" type="grid" cols="2" mobile-breakpoint="800">
               <onyks-card title="Symbol" size="l">
                    <onyks-container gap="m" type="group">
                        <onyks-text>Symbol Reference</onyks-text>
                        <onyks-textfield disabled v-model="model.libraryReference"></onyks-textfield>
                        <onyks-text>Symbol Path</onyks-text>
                        <onyks-textfield disabled v-model="model.libraryPath"></onyks-textfield>
                        <onyks-button background="blue" v-if="props.type !== 'details'">Select</onyks-button>
                    </onyks-container>
               </onyks-card>
               <onyks-card title="Footprint No 1" size="l">
                    <onyks-container gap="m" type="group">
                        <onyks-text>Footprint Reference</onyks-text>
                        <onyks-textfield disabled v-model="model.footprintReferenceNo1"></onyks-textfield>
                        <onyks-text>Footprint Path</onyks-text>
                        <onyks-textfield disabled v-model="model.footprintPathNo1"></onyks-textfield>
                        <onyks-button background="yellow" v-if="props.type !== 'details'">Select</onyks-button>
                    </onyks-container>
               </onyks-card>
               <onyks-card title="Footprint No 2" size="l">
                    <onyks-container gap="m" type="group">
                        <onyks-text>Footprint Reference</onyks-text>
                        <onyks-textfield disabled v-model="model.footprintReferenceNo2"></onyks-textfield>
                        <onyks-text>Footprint Path</onyks-text>
                        <onyks-textfield disabled v-model="model.footprintPathNo2"></onyks-textfield>
                        <onyks-button background="yellow" v-if="props.type !== 'details'">Select</onyks-button>
                    </onyks-container>
               </onyks-card>
               <onyks-card title="Footprint No 3" size="l">
                    <onyks-container gap="m" type="group">
                        <onyks-text>Footprint Reference</onyks-text>
                        <onyks-textfield disabled v-model="model.footprintReferenceNo3"></onyks-textfield>
                        <onyks-text>Footprint Path</onyks-text>
                        <onyks-textfield disabled v-model="model.footprintPathNo3"></onyks-textfield>
                        <onyks-button background="yellow" v-if="props.type !== 'details'">Select</onyks-button>
                    </onyks-container>
               </onyks-card>
            </onyks-container>
        </onyks-card>

        <onyks-card title="Suppliers" cols="2" size="xl">
            <SuppliersSelector v-if="props.type !== 'details'" v-model="model.suppliers" :action="services.suppliers.list" ref="suppliersSelector"></SuppliersSelector>
            
            <onyks-container gap="m" v-else>
                <onyks-container v-for="(supplierName, supplierId) in model.suppliers" :key="supplierId" type="grid" gap="m" cols="2">
                    <onyks-header level="6">{{ suppliersNames[supplierId] }}</onyks-header>
                    <onyks-text>{{ supplierName }}</onyks-text>
                </onyks-container>
            </onyks-container>
        </onyks-card>


        <!-- <onyks-card title="Suppliers" cols="1" size="l">
            <onyks-container gap="m" type="grid" cols="1" mobile-breakpoint="800">
                <ValueSelector v-model:name="model.suppliers"></ValueSelector>
            </onyks-container>
        </onyks-card>

        <onyks-card title="Datasheets" cols="1" size="l">
            <onyks-container gap="m" type="grid" cols="1" mobile-breakpoint="800">
                <ValueSelector v-model:name="model.suppliers"></ValueSelector>
            </onyks-container>
        </onyks-card> -->

    </onyks-container>
</template>

<style scoped>
    onyks-textarea
    {
        height: 200px;
    }
</style>