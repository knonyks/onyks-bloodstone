<script setup>
    import Logos from '../components/Logos.vue';
    import { useLoaderStore } from '../stores/loader';
    import { ref } from 'vue'
    import { useRouter, useRoute } from 'vue-router'
    import { useAuthStore } from '../stores/auth';
    import { OnyksToastContainer } from 'onyks-web-ui';

    const auth = useAuthStore()   
    const loaderStore = useLoaderStore()
    const router = useRouter()
    const route = useRoute()
    const username = ref('')
    const password = ref('')
    const expired_account_dialog = ref(false)

    loaderStore.globalHide()

    const handle_login = async () =>
    {
        try
        {
            const response = await auth.login(username.value, password.value)
            router.push(route.query.redirect || '/')
        }
        catch (error)
        {
            if(error.response.data.detail.error_code === "INVALID_CREDENTIALS")
            {
                OnyksToastContainer.error(error.response.data.detail.message)
            }
            else if(error.response.data.detail.error_code === "ACCOUNT_EXPIRED")
            {
                expired_account_dialog.value = true
            }
            else
            {
                OnyksToastContainer.error('An unexpected error occurred.')
            }
        }
    }
</script>

<template>
    <onyks-container class="content" align="center" justify="center" padding="m" type="stack" gap="m" cols="10" rows="1">
        <logos class="logos"></logos>    
        <onyks-container gap="m" class="login">
            <onyks-header level="6">Login</onyks-header>
            <onyks-textfield type="text" v-model="username"></onyks-textfield>
            <onyks-header level="6">Password</onyks-header>
            <onyks-textfield type="password" v-model="password"></onyks-textfield>
            
            <onyks-button background="green" @click="handle_login">Login!</onyks-button>
        
            <router-link to="/manager/dashboard" class="link"><onyks-text size="s">Forgot password?</onyks-text></router-link>
            <!-- <router-link to="/manager/dashboard" class="link"><onyks-text size="s">Request for create an account</onyks-text></router-link> -->
            <onyks-dialog :open="expired_account_dialog" title="Account Expired" open scroll-target="none" size="m" title-size="l" corner-close @dialog-close="expired_account_dialog = false">
                <onyks-text>Your account has expired. Please contact with your support to resolve this issue.</onyks-text>
            </onyks-dialog>
        </onyks-container>
    </onyks-container>
</template>

<style lang="css" scoped>
    .logos
    {
        top: 0;
        left: 0;
        position: fixed;
    }

    .content
    {
        width: 100%;
        height: 100%;
        box-sizing: border-box;
    }

    .login
    {
        max-width: 350px;
        width: 100%;
        height: fit-content;
    }

    .loginBtn > *
    {
        width: 100%;
    }

    .link
    {
        text-decoration: none;
        color: inherit;
    }

    onyks-textfield
    {
        width: 100%;
    }

    onyks-button
    {
        width: 100%;
    }
</style>