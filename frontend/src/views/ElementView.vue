<script setup lang="js">
    import { onMounted, ref, reactive } from 'vue';
    import ManagerPage from '@/components/ManagerPage.vue'
    import { useLoaderStore } from '@/stores/loader';
    import { useRoute } from 'vue-router';
    import { useRouter } from 'vue-router';
    import ElementForm from '@/components/ElementForm.vue';
    import { services } from '@/utils/api';
    import { models } from '@/utils/models';

    const loaderStore = useLoaderStore();
    const route = useRoute();
    const router = useRouter();
    const schema = route.name === 'element-edit' ? 'edit' : route.name === 'element-duplicate' ? 'duplicate' : route.name === 'element-details' ? 'details' : 'create';
    
    const obj = reactive(
    {
        details: models.elements.getModel(),
        files: []
    })

    onMounted(async () =>
    {
        if(schema == 'edit' || schema == 'duplicate' || schema == 'details')
        {
            let result = await services.elements.get(route.params.uuid);
            Object.assign(obj.details, result.data || {});
        }
        loaderStore.hide()
        loaderStore.globalHide()
    })


    const btns = 
    {
        add:
        {
            action: async () =>
            {
                console.log(obj.details)
                console.log(await services.elements.create(obj.details, obj.files))
            }
        },
        edit:
        {
            action: async () =>
            {
                // console.log(await services.elements.update(element))
            }
        },
        duplicate:
        {
            action: async () =>
            {
                // console.log(await services.elements.create(element))
            }
        }
    }
</script>

<template>
    <ManagerPage :title="schema === 'edit' ? 'Edit Element' : schema === 'duplicate' ? 'Duplicate Element' : schema === 'details' ? 'Element Details' : 'Create Element'">
        <onyks-button background="red" @click="router.back()">Back</onyks-button>
        <ElementForm :schema="schema" v-model="obj"></ElementForm>

        <onyks-container align="end" v-if="schema !== 'details'">
            <onyks-button v-if="schema == 'create'" background="green" @click="btns.add.action()">Create</onyks-button>
            <onyks-button v-if="schema == 'edit'" background="green" @click="btns.edit.action()">Save</onyks-button>
            <onyks-button v-if="schema == 'duplicate'" background="green" @click="btns.duplicate.action()">Duplicate</onyks-button>
        </onyks-container>
        
    </ManagerPage>
</template>

<style>

</style>