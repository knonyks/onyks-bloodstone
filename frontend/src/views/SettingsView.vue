<script setup>
    import ManagerPage from '../components/ManagerPage.vue';
    import { computed, onMounted } from 'vue';
    import { useLoaderStore } from '../stores/loader';
    import { useAuthStore } from '../stores/auth.js';
    import { i18n } from '../utils/localization.js';

    const loaderStore = useLoaderStore()
    const authStore = useAuthStore()

    const remainingTime = computed(() =>
    {
        const expiration = authStore.user.expiration_time
        if (!expiration) return { years: 0, days: 0, hours: 0, minutes: 0 }

        const utcExpiration = /(?:Z|[+-]\d{2}:?\d{2})$/i.test(expiration) ? expiration : `${expiration}Z`
        const expirationTimestamp = Date.parse(utcExpiration)
        if (Number.isNaN(expirationTimestamp)) return { years: 0, days: 0, hours: 0, minutes: 0 }

        let minutes = Math.max(0, Math.floor((expirationTimestamp - Date.now()) / 60000))
        const years = Math.floor(minutes / (365 * 24 * 60))
        minutes %= 365 * 24 * 60
        const days = Math.floor(minutes / (24 * 60))
        minutes %= 24 * 60
        const hours = Math.floor(minutes / 60)
        minutes %= 60

        return { years, days, hours, minutes }
    })

    onMounted(async () =>
    {
        loaderStore.hide()
        loaderStore.globalHide()
    })

</script>

<template>
    <ManagerPage :title="$t('common.settings')">
        <onyks-card :title="$t('users.basic_information')" title-size="l">
            <onyks-container type="grid" cols="2" mobile-breakpoint="550" gap="m" align="center" justify="center">
                <onyks-header>{{ i18n.global.t('users.username') }}</onyks-header>
                <onyks-text>{{ authStore.user.username || i18n.global.t('common.no_data') }}</onyks-text>
                <onyks-header>{{ i18n.global.t('users.name') }}</onyks-header>
                <onyks-text>{{ authStore.user.name || i18n.global.t('common.no_data') }}</onyks-text>
                <onyks-header>{{ i18n.global.t('users.surname') }}</onyks-header>
                <onyks-text>{{ authStore.user.surname || i18n.global.t('common.no_data') }}</onyks-text>
                <onyks-header>{{ i18n.global.t('users.email') }}</onyks-header>
                <onyks-text>{{ authStore.user.email || i18n.global.t('common.no_data') }}</onyks-text>
                <onyks-header>{{ i18n.global.t('users.rank') }}</onyks-header>
                <onyks-text>{{ authStore.user.rank == 'editor'? i18n.global.t('users.editor'):i18n.global.t('users.admin') }}</onyks-text>
                <onyks-header>{{ i18n.global.t('users.expiration_time') }}</onyks-header>
                <onyks-text>{{ i18n.global.d(authStore.user.expiration_time, 'short') }}</onyks-text>
                <onyks-text></onyks-text>
                <onyks-container type="grid" gap="s">
                    <onyks-text>{{ i18n.global.t('users.how_much_time.years', remainingTime.years) }},
                        {{ i18n.global.t('users.how_much_time.days', remainingTime.days) }},
                        {{ i18n.global.t('users.how_much_time.hours', remainingTime.hours) }},
                        {{ i18n.global.t('users.how_much_time.minutes', remainingTime.minutes) }}
                    </onyks-text>
                </onyks-container>
                <onyks-header>{{ i18n.global.t('common.created_at') }}</onyks-header>
                <onyks-text>{{ i18n.global.d(authStore.user.created_at, 'short') }}</onyks-text>
            </onyks-container>
        </onyks-card>
    </ManagerPage>
</template>

<style lang="css">
    onyks-dialog::part(content)
    {
        overflow-y: unset;
    }

    onyks-dialog::part(container)
    {
        max-height: unset;
    }
</style>