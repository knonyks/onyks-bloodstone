<script setup>
    import Logos from '@/components/Logos.vue';

</script>

<template>
    <onyks-container class="content" align="center" justify="center" padding="s" type="stack" gap="m" cols="10" rows="1">
        <logos class="logos"></logos>    
        <onyks-container gap="m" class="login">
            <onyks-text>Login</onyks-text>
            <onyks-textfield type="text"></onyks-textfield>
            <onyks-text>Password</onyks-text>
            <onyks-textfield type="password"></onyks-textfield>
            <onyks-container class="rememberMe" align="center" type="group" gap="s">
                <onyks-checkbox></onyks-checkbox>
                <onyks-text>Remember me</onyks-text>
            </onyks-container>
            
            <router-link to="/manager/dashboard" class="loginBtn"><onyks-button background="green">Login!</onyks-button></router-link>
        
            <router-link to="/manager/dashboard" class="link"><onyks-text size="s">Forgot password?</onyks-text></router-link>
            <router-link to="/manager/dashboard" class="link"><onyks-text size="s">Request for create an account</onyks-text></router-link>
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
        max-width: 325px;
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
</style>