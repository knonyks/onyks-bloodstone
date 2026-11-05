<script setup lang="js">
    import { onMounted, ref, reactive, onBeforeUnmount } from 'vue';
    import ManagerPage from '../components/ManagerPage.vue'
    import { useLoaderStore } from '../stores/loader';
    import { useRoute } from 'vue-router';
    import { useRouter } from 'vue-router';
    import ElementForm from '../components/ElementForm.vue';
    import { services } from '../utils/api';
    import { models } from '../utils/models';
    import ProcessingElementDialog from '../components/ProcessingElementDialog.vue';
    import { delay } from '../utils/tools';
    import { OnyksContainer, OnyksToastContainer } from 'onyks-web-ui-system';
    import { i18n } from '../utils/localization';
    import { labels_generate } from '../utils/generateLabels';
    import RemoveItemsDialog from '../components/RemoveItemsDialog.vue';
    import { useRemoveItemsDialog } from '../composables/useRemoveItemsDialog';

    const loaderStore = useLoaderStore();
    const route = useRoute();
    const router = useRouter();
    const schema = route.name === 'element-edit' ? 'edit' : route.name === 'element-duplicate' ? 'duplicate' : route.name === 'element-details' ? 'details' : 'create';
    
    const obj = reactive(
    {
        details: models.elements.getModel(),
        files: []
    })

    const dialogs = reactive(
    {
        create:
        {
            open: false
        },
        edit:
        {
            open: false
        },
        duplicate:
        {
            open: false
        },
        remove: useRemoveItemsDialog(services.elements, i18n.global.t('elements.remove'), ['uuid', 'part_name'], () =>
        {
            OnyksToastContainer.error(i18n.global.t('elements.removed_successfully'))
            router.push('/manager/management')
        })
    })

    onMounted(async () =>
    {
        if(schema == 'edit' || schema == 'duplicate' || schema == 'details')
        {
            let result = await services.elements.get(route.params.uuid);
            const details = Object.fromEntries(
                Object.entries(result.data || {}).filter(([, value]) => value !== null)
            );
            Object.assign(obj.details, details);
        }   
        
        // for (const [key, value] of Object.entries(obj.details))
        // {
        //     if (typeof value === 'string' && !value)
        //     {
        //         obj.details[key] = i18n.global.t('common.no_data')
        //     }
        // }
        // if(schema == 'edit')
        // {

        // }
        loaderStore.hide()
        loaderStore.globalHide()
    })

    const btns = 
    {
        add:
        {
            action: async () =>
            {
                try
                {
                    dialogs.create.open = true;
                    let result = await services.elements.create(obj.details, obj.files)
                    await delay(1000)
                    dialogs.create.open = false;
                    OnyksToastContainer.success(i18n.global.t('elements.created_successfully'))
                    router.push('/manager/elements/details/' + result.data.uuid)
                }
                catch(err)
                {
                    await delay(1000)
                    dialogs.create.open = false;
                    OnyksToastContainer.error(i18n.global.t(`error_codes.${err?.response?.data?.detail?.error_code}`) || err?.message || 'An error occurred')
                }
            }
        },
        edit:
        {
            action: async () =>
            {
                try
                {
                    dialogs.edit.open = true;
                    let result = await services.elements.update(route.params.uuid, obj.details, obj.files)
                    await delay(1000)
                    dialogs.edit.open = false;
                    OnyksToastContainer.success(i18n.global.t('elements.edited_successfully'))
                    router.push('/manager/elements/details/' + result.data.uuid)
                }
                catch(err)
                {
                    await delay(1000)
                    dialogs.edit.open = false;
                    OnyksToastContainer.error(i18n.global.t(`error_codes.${err?.response?.data?.detail?.error_code}`) || err?.message || 'An error occurred')
                }
            }
        },
        duplicate:
        {
            action: async () =>
            {
                try
                {
                    dialogs.duplicate.open = true;
                    let result = await services.elements.duplicate(route.params.uuid, obj.details, obj.files)
                    await delay(1000)
                    dialogs.duplicate.open = false;
                    OnyksToastContainer.success(i18n.global.t('elements.duplicated_successfully'))
                    router.push('/manager/elements/details/' + result.data.uuid)
                }
                catch(err)
                {
                    await delay(1000)
                    dialogs.duplicate.open = false;
                    OnyksToastContainer.error(i18n.global.t(`error_codes.${err?.response?.data?.detail?.error_code}`) || err?.message || 'An error occurred')
                }
            }
        }
    }
</script>

<template>
    <ManagerPage :title="$t('elements.' + schema)">
        <onyks-container gap="m" type="group">
            <onyks-button background="red" @click="router.back()">{{$t('common.back')}}</onyks-button>
            <onyks-button v-if="schema != 'details' && schema != 'create'" background="blue" @click="router.push(`/manager/elements/details/${route.params.uuid}`)">{{$t('common.details')}}</onyks-button>
        </onyks-container>
        
        <ElementForm :schema="schema" v-model="obj"></ElementForm>

        <onyks-container align="end" v-if="schema !== 'details'">
            <onyks-button v-if="schema == 'create'" background="green" @click="btns.add.action()">{{$t('common.create')}}</onyks-button>
            <onyks-button v-if="schema == 'edit'" background="green" @click="btns.edit.action()">{{$t('common.edit')}}</onyks-button>
            <onyks-button v-if="schema == 'duplicate'" background="green" @click="btns.duplicate.action()">{{$t('common.duplicate')}}</onyks-button>
        </onyks-container>
        <onyks-container justify="end" v-if="schema === 'details'" type="group" gap="m" mobile-breakpoint="600">

            <onyks-button background="blue" @click="router.push(`/manager/elements/edit/${route.params.uuid}`)">{{$t('common.edit')}}</onyks-button>
            <onyks-button background="yellow" @click="router.push(`/manager/elements/duplicate/${route.params.uuid}`)">{{$t('common.duplicate')}}</onyks-button>
            <onyks-button background="red" @click="dialogs.remove.items = [obj.details]; dialogs.remove.first_open = true">{{$t('common.remove')}}</onyks-button>
            <onyks-button @click="labels_generate([obj.details])" background="green">{{$t('common.labels')}}</onyks-button>

        </onyks-container>

        <ProcessingElementDialog :open="dialogs.create.open" :message="$t('elements.creating')"></ProcessingElementDialog>
        <ProcessingElementDialog :open="dialogs.duplicate.open" :message="$t('elements.duplicating')"></ProcessingElementDialog>
        <ProcessingElementDialog :open="dialogs.edit.open" :message="$t('elements.editing')"></ProcessingElementDialog>
        <RemoveItemsDialog v-model="dialogs.remove"></RemoveItemsDialog>

    </ManagerPage>
</template>

<style>

</style>