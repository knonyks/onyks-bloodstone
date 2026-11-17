<script setup>
    import { ref } from 'vue';
    import { useAuthStore } from '../stores/auth';
    import router from '../router';

    const authStore = useAuthStore();
    const is_open = ref(false);

    const props = defineProps(
    {
        username: String,
        expiration_time: String
    })
</script>


<template>
    <onyks-container padding="m" class="tile" gap="m" align="end" @wheel.prevent @touchmove.prevent>
        <Transition name="blur">
            <div v-if="is_open" class="background-blur" @wheel.prevent @touchmove.prevent></div>
        </Transition>
        <Transition name="card">
        <onyks-card title-size="l" v-if="is_open" :title="$t('common.user')" class="card" padding="m">
            <onyks-container gap="m" style="width: 100%;">
                <onyks-container gap="m" type="stack" style="width: 100%;">
                    <onyks-text>{{ $t('common.logged_in_as') }}</onyks-text>
                    <onyks-tag class="tag" background="lime" icon="F4D5">{{ props.username }}</onyks-tag>
                    <onyks-text>{{ $t('common.account_expires') }}</onyks-text>
                    <onyks-tag  class="tag" background="indigo" icon="F214">{{ props.expiration_time }}</onyks-tag>
                </onyks-container>
                <onyks-container align="end" justify="end">
                    <onyks-button size="m" class="logout-btn" @click="authStore.logout(); router.push('/login')" icon="F1C2" background="red">{{ $t('common.logout') }}</onyks-button>
                </onyks-container>
            </onyks-container>
        </onyks-card>
        </Transition>
        <onyks-tile size="m" icon="F4D7" class="user-tile" @click="is_open = !is_open"></onyks-tile>
    </onyks-container>
</template>

<style scoped>
    .background-blur
    {
        position: fixed;
        width: 100%;
        height: 100%;
        backdrop-filter: blur(50px);
        z-index: 0;
        top: 0;
        left: 0;
        pointer-events: auto;
        touch-action: none;
        overscroll-behavior: none;
    }

    .blur-enter-active,
    .blur-leave-active
    {
        transition: opacity 0.25s ease, backdrop-filter 0.25s ease;
    }

    .blur-enter-from,
    .blur-leave-to
    {
        opacity: 0;
        backdrop-filter: blur(0);
    }

    .card-enter-active,
    .card-leave-active
    {
        transition: opacity 0.25s ease, transform 0.25s ease;
    }

    .card-enter-from,
    .card-leave-to
    {
        opacity: 0;
        transform: translateY(12px);
    }

    .card
    {
        position: relative;
        width: 100%;
        min-width: 0;
        box-sizing: border-box;
        flex-shrink: 1;
        height: fit-content;
    }

    .tile
    {
        position: fixed;
        align-self: flex-end;
        margin-left: auto;
        box-sizing: border-box;
        pointer-events: none;
        height: fit-content;
        width: 100vw;
        max-width: 400px;
        bottom: 0;
        z-index: 20;
    }

    .tag
    {
        width: 100%;
        max-width: 100%;
    }

    .logout-btn
    {
        pointer-events: auto;
        width: fit-content;
    }

    .user-tile
    {
        position: relative;
        z-index: 0;
        pointer-events: auto;
        cursor: pointer;
    }
</style>