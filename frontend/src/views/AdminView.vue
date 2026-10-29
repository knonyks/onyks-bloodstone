<script setup lang="js">
    import { onMounted, reactive } from 'vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import { useLoaderStore } from '@/stores/loader';
    import SubTitle from '@/components/SubTitle.vue';
    import BasicButtonsPanel from '@/components/BasicButtonsPanel.vue';
    import BasicTable from '@/components/BasicTable.vue';
    import { useBasicTable } from '@/composables/useBasicTable';
    import { i18n } from '@/utils/localization';
    import { services } from '@/utils/api';

    const loaderStore = useLoaderStore()
    const usersTable = reactive(useBasicTable())
    usersTable.columns = [
        {
            label: i18n.global.t('common.selected'),
            key: 'selected'
        },
        {
            label: i18n.global.t('common.id'),
            key: 'id'
        },
        {
            label: i18n.global.t('users.name'),
            key: 'name'
        },
        {
            label: i18n.global.t('users.surname'),
            key: 'surname'
        },
        {
            label: i18n.global.t('users.email'),
            key: 'email'
        },
        {
            label: i18n.global.t('users.rank'),
            key: 'rank'
        },
        {
            label: i18n.global.t('users.expiration_time'),
            key: "expiration_time"
        },
        {
            label: i18n.global.t('common.created_at'),
            key: "created_at"
        }
    ]
    usersTable.service = services.users
    usersTable.format_data = (e) => {
        return {
            selected: e.selected ?? false,
            id: e.id,
            name: e.name || i18n.global.t('common.no_data'),
            surname: e.surname || i18n.global.t('common.no_data'),
            email: e.email || i18n.global.t('common.no_data'),
            rank: e.rank ? i18n.global.t(`users.ranks.${e.rank}`) : i18n.global.t('common.no_data'),
            expiration_time: e.expiration_time ? i18n.global.d(new Date(e.expiration_time), 'short') : '',
            created_at: e.created_at ? i18n.global.d(new Date(e.created_at), 'short') : ''
        }
    }

    

    onMounted(async () =>
    {
        try 
        {
            loaderStore.hide()
            loaderStore.globalHide()
            await usersTable.init()
        } 
        catch (err) 
        {}
    })
</script>

<template>
    <ManagerPage :title="$t('common.admin_panel')">
        <SubTitle>{{ $t('common.user_list') }}</SubTitle>
        <BasicButtonsPanel>
            <onyks-button background="green">{{ $t('common.add') }}</onyks-button>
            <onyks-button background="red">{{ $t('common.remove') }}</onyks-button>
            <onyks-button background="blue">{{ $t('common.edit') }}</onyks-button>
            <onyks-button background="orange">{{ $t('common.reset') }}</onyks-button>
            <onyks-button background="purple">{{ $t('common.import') }}</onyks-button>
        </BasicButtonsPanel>
        <BasicTable v-model="usersTable"></BasicTable>
        <SubTitle>{{ $t('common.backup') }}</SubTitle>
    </ManagerPage>
</template>

<style lang="css" scoped>

</style>