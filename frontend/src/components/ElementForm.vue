<script setup lang="js">
    import ElementPath from './ElementPath.vue';
    import { reactive } from 'vue';
    import { onMounted } from 'vue';
    import { useRepositoryModelDialog } from '../utils/tools';
    import RepositoryModelDialog from './RepositoryModelDialog.vue';

    const props = defineProps(['schema'])
    const element = defineModel('element');

    const dialogs = reactive(
    {
        symbol: useRepositoryModelDialog('Select Symbol')
    })


    onMounted(async () => 
    {
        dialogs.symbol.init()
    })
</script>

<template>
    <onyks-container gap="m">
        <onyks-header level="4">Basic information</onyks-header>
        <onyks-container type="grid" cols="2" mobile-breakpoint="900" gap="m">
            
            <onyks-container gap="m">

                <onyks-header level="6" v-if="props.schema == 'details' || props.schema == 'edit'">UUID</onyks-header>
                <onyks-textfield v-model="element.uuid" v-if="props.schema == 'details' || props.schema == 'edit'" disabled></onyks-textfield>

                <onyks-header level="6">Part Name</onyks-header>
                <onyks-textfield v-model="element.partName" :disabled="props.schema == 'details'"></onyks-textfield>

                <onyks-header level="6">Value</onyks-header>
                <onyks-textfield v-model="element.value" :disabled="props.schema == 'details'"></onyks-textfield>

            </onyks-container>
            <onyks-container gap="m">

                <onyks-header level="6">Availability</onyks-header>
                <onyks-textfield v-model="element.availability" :disabled="props.schema == 'details'"></onyks-textfield>

                <onyks-header level="6" v-if="props.schema == 'details' || props.schema == 'edit'">Created At</onyks-header>
                <onyks-textfield disabled v-model="element.createdAt" v-if="props.schema == 'details' || props.schema == 'edit'" :disabled="props.schema == 'details'"></onyks-textfield>

            </onyks-container>
        </onyks-container>
        <onyks-header level="6">Description</onyks-header>
        <onyks-textarea v-model="element.description" :disabled="props.schema == 'details'" size="m" placeholder="" resize="none"></onyks-textarea>

        <onyks-header level="4">Symbol & Footprints</onyks-header>

        <onyks-container type="grid" cols="2" mobile-breakpoint="900" gap="m">
            
            <onyks-container gap="m" cols="1">
                <onyks-header level="6">Symbol</onyks-header>
                <onyks-container>
                    <ElementPath v-model:path="element.libraryPath" v-model:obj="element.libraryReference"></ElementPath>

                </onyks-container>
                <onyks-button background="yellow" @click="dialogs.symbol.open = true">Select</onyks-button>
                <onyks-header level="6">Footprint No 2</onyks-header>
                <ElementPath v-model:path="element.footprintPathNo2" v-model:obj="element.footprintReferenceNo2"></ElementPath>
                <onyks-button background="grey">Select</onyks-button>

                <RepositoryModelDialog v-model="dialogs.symbol" v-model:path="element.libraryPath" v-model:obj="element.libraryReference"></RepositoryModelDialog>
            </onyks-container>
            <onyks-container gap="m" cols="1">
                <onyks-header level="6">Footprint No 1</onyks-header>
                <ElementPath :path="element.footprintPathNo1" :obj="element.footprintReferenceNo1"></ElementPath>
                <onyks-button background="grey">Select</onyks-button>
                <onyks-header level="6">Footprint No 3</onyks-header>
                <ElementPath :path="element.footprintPathNo3" :obj="element.footprintReferenceNo3"></ElementPath>
                <onyks-button background="grey">Select</onyks-button>
            </onyks-container>
        </onyks-container>
    </onyks-container>
    <onyks-header level="4">Suppliers</onyks-header>
    <onyks-header level="4">Datasheets</onyks-header>
    <onyks-header level="4">Tags</onyks-header>
</template>

<style>
    onyks-textarea 
    {
        width: 100%;
        height: 300px;
    }
    
</style>