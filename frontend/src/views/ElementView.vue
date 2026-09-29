<script setup lang="js">
    import { onMounted } from 'vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import { useLoaderStore } from '@/stores/loader';
    import { useRoute } from 'vue-router';
    import ElementForm from '@/components/ElementForm.vue';
    import { ref } from 'vue';
    import { services, suppliers } from '@/utils/api';


    const loaderStore = useLoaderStore();
    const form = ref(null);
    const route = useRoute();
    const type = route.name === 'ElementEdit' ? 'edit' : route.name === 'ElementDuplicate' ? 'duplicate' : route.name === 'ElementDetails' ? 'details' : 'create';
    
    const element = ref({
        uuid: '2adf1234',
        partName: 'Resistor 2k22 Ohm SMD',
        value: '2k22 Ohm',
        availability: 'In stock',
        description: '2k22 Ohm SMD resistor',
        manufacturer: '',
        table: '',

        libraryReference: '1',
        libraryPath: '2',

        footprintReferenceNo1: '3',
        footprintPathNo1: '4',

        footprintReferenceNo2: '5',
        footprintPathNo2: '6',

        footprintReferenceNo3: '7',
        footprintPathNo3: '8',

        createdAt: '12:12:2023, 12:12:12',

        suppliers: {
            '1':'1111',
            '2': '2222',
            '6': '6666'
        }
    });

    onMounted(async () =>
    {
        await form.value.init()
        loaderStore.hide()
        loaderStore.globalHide()
    })
</script>

<template>
    <ManagerPage :title="type == 'create' ? 'Create Element' : type == 'edit' ? 'Edit Element' : type == 'duplicate' ? 'Duplicate Element' : 'Element Details'">
        <!-- create edit duplicate details -->
        <ElementForm v-model="element" ref="form" :type="type"></ElementForm> 
        <onyks-container type="group" justify="end">
            <onyks-button background="green" @click="console.log(element)">Create</onyks-button>
        </onyks-container>
    </ManagerPage>
</template>

<style>

</style>