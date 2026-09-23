<script setup>
    import { ref } from 'vue';
    import { onMounted } from 'vue';
    import DataLoader from '@/components/DataLoader.vue';
    import ManagerPage from '@/components/ManagerPage.vue';
    import BasicButtonsPanel from '@/components/BasicButtonsPanel.vue';
    import { services } from '@/utils/api';
    import { MyLoaderState, MyTime } from '@/utils/tools';
    import BasicTable from '@/components/BasicTable.vue';
    import { MyTable } from '@/utils/tools';
    import BasicSearch from '@/components/BasicSearch.vue';
    import { useLoaderStore } from '@/stores/loader';

    const loaderStore = useLoaderStore()

    const users = ref(new MyTable(services.users.list, 
    [
        {
            "key": "selected",
            "label": "Select"
        },
        {
            'key': 'id',
            'label': 'ID'
        },
        {
            "key": "login",
            "label": "Login"
        },
        {
            "key": "expirationTime",
            "label": "Expiration Time"
        },
    ], (e) => {e.selected = false; e.createdAt = MyTime.getLocalTime(e.expirationTime, 'en'); return e}))


    onMounted(async () =>
    {
        await users.value.init()
        loaderStore.hide()
        loaderStore.globalHide()
    })
</script>

<template>

    <ManagerPage title="Admin">
        <!-- #region Users -->
        <onyks-header level=3>Users</onyks-header>
        <BasicButtonsPanel>
            <onyks-button background="green">Add</onyks-button>
            <onyks-button background="blue">Edit</onyks-button>
            <onyks-button background="yellow">Reset</onyks-button>
            <onyks-button>Delete</onyks-button>
        </BasicButtonsPanel>
        <BasicTable v-model="users"></BasicTable>
        <!-- #endregion -->
    </ManagerPage>

</template>

<style lang="css">
</style>