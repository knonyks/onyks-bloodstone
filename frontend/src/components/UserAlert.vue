<script setup>
    import { useAuthStore } from '../stores/auth';
    import router from '../router';
    const authStore = useAuthStore();

    const props = defineProps({
        username: String,
        expiration_time: String
    })
</script>

<template>
    <onyks-alert type="info">
        <onyks-container type="group" justify="center" gap="m" style="width: 100%; flex-wrap: nowrap;">
            <onyks-container align="center" justify="left" style="flex-grow: 1;" gap="s" type="group">
                <onyks-text>You are logged in as</onyks-text>
                <onyks-tag background="yellow" icon="F4D5">{{ props.username }}</onyks-tag>
                <onyks-text>Your account is valid until</onyks-text>
                <onyks-tag background="green" icon="F214">{{ props.expiration_time }}</onyks-tag>
            </onyks-container>
            <!-- <onyks-button>Logout</onyks-button> -->
            <onyks-container align="center" justify="center">
                <onyks-tag @click="authStore.logout(); router.push('/login')" icon="F1C2" background="red" style="height: fit-content;">Logout</onyks-tag>
            </onyks-container>
        </onyks-container>
    </onyks-alert>
</template>