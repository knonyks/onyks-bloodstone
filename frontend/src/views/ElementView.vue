<script setup lang="js">
    import { onMounted, ref, reactive } from 'vue';
    import ManagerPage from '@/components/ManagerPage.vue'
    import { useLoaderStore } from '@/stores/loader';
    import { useRoute } from 'vue-router';
    import { useRouter } from 'vue-router';
    import ElementForm from '@/components/ElementForm.vue';


    


    const loaderStore = useLoaderStore();
    const route = useRoute();
    const router = useRouter();
    const schema = route.name === 'element-edit' ? 'edit' : route.name === 'element-duplicate' ? 'duplicate' : route.name === 'element-details' ? 'details' : 'create';
    
    const element = reactive({
        uuid: '2adf1234',
        partName: 'Resistor 2k22 Ohm SMD',
        value: '2k22 Ohm',
        availability: 'In stock',
        description: '2k22 Ohm SMD resistor',





    //     manufacturer: '',
    //     table: 'MCUsSS',
    //     tableId: 0,

        libraryReference: '',
        libraryPath: '',

        footprintReferenceNo1: '3',
        footprintPathNo1: '4',

        footprintReferenceNo2: '5',
        footprintPathNo2: '6',

        footprintReferenceNo3: '7',
        footprintPathNo3: '8',

        createdAt: '12:12:2023, 12:12:12',

    //     suppliers: {
    //         '1':'1111',
    //         '2': '2222',
    //         '6': '6666'
    //     }
    });

    onMounted(async () =>
    {
        loaderStore.hide()
        loaderStore.globalHide()
    })
</script>

<template>
    <ManagerPage :title="schema === 'edit' ? 'Edit Element' : schema === 'duplicate' ? 'Duplicate Element' : schema === 'details' ? 'Element Details' : 'Create Element'">
        <onyks-button background="red" @click="router.back()">Back</onyks-button>
        <ElementForm :schema="schema" v-model:element="element"></ElementForm> 
    </ManagerPage>
</template>

<style>

</style>