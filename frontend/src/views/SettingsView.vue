<script setup>
    import ManagerPage from '@/components/ManagerPage.vue';
    import { onMounted } from 'vue';
    import { useLoaderStore } from '@/stores/loader';

    const loaderStore = useLoaderStore()

    onMounted(async () =>
    {
        loaderStore.hide()
        loaderStore.globalHide()
    })

</script>

<template>

    <ManagerPage title="Settings">

        <!-- <onyks-container gap="m" type="grid" cols="2" mobile-breakpoint="900"> -->
            <onyks-card title="Account details" size="l">
                <onyks-container gap="m">
                    <onyks-container type="grid" cols="10" gap="m" mobile-breakpoint="500">
                        <onyks-header level="6" cols="4">First Name</onyks-header>
                        <onyks-text  cols="6">Jan</onyks-text>
                    </onyks-container>

                    <onyks-container type="grid" cols="10" gap="m" mobile-breakpoint="500">
                        <onyks-header level="6" cols="4">Family Name</onyks-header>
                        <onyks-text  cols="6">Kowalski</onyks-text>
                    </onyks-container>

                    <onyks-container type="grid" cols="10" gap="m" mobile-breakpoint="500">
                        <onyks-header level="6" cols="4">Username</onyks-header>
                        <onyks-text  cols="6">JanKowal67</onyks-text>
                    </onyks-container>
                    
                    <onyks-container type="grid" cols="10" gap="m" mobile-breakpoint="500">
                        <onyks-header level="6" cols="4">E-mail</onyks-header>
                        <onyks-text  cols="6">jankowal67@gmail.com</onyks-text>
                    </onyks-container>

                    <onyks-text size="s">Change</onyks-text>

                    <onyks-container type="grid" cols="10" gap="m" mobile-breakpoint="500">
                        <onyks-header level="6" cols="4">Password</onyks-header>
                        <onyks-text  cols="6">********</onyks-text>
                    </onyks-container>

                    <onyks-text size="s">Change</onyks-text>


                    <onyks-container type="grid" cols="10" gap="m" mobile-breakpoint="500">
                        <onyks-header level="6" cols="4">Rank</onyks-header>
                        <onyks-text  cols="6">Admin</onyks-text>
                    </onyks-container>

                    <onyks-text size="s">About ranks</onyks-text>
                    <onyks-text size="s">Request for a new rank</onyks-text>

                    <onyks-container type="grid" cols="10" gap="m" mobile-breakpoint="500">
                        <onyks-header level="6" cols="4">Expiration Date</onyks-header>
                        <onyks-text  cols="6">2023-12-31, 23:59:59</onyks-text>
                    </onyks-container>

                    <onyks-text size="s">Request for extension</onyks-text>

                </onyks-container>

            </onyks-card>

            <!-- change e-mail -->
            <onyks-dialog corner-close modal title="Change the e-mail" bottom-buttons>
                <onyks-container gap="m">
                    <onyks-text>Enter a new e-mail</onyks-text>
                    <onyks-textfield></onyks-textfield>
                    <onyks-text>Repeat the e-mail</onyks-text>
                    <onyks-textfield></onyks-textfield>
                </onyks-container>
                <onyks-button slot="footer" background="green">Confirm</onyks-button>
            </onyks-dialog>

            <!-- change password -->
            <onyks-dialog corner-close modal title="Change the password" bottom-buttons>
                <onyks-container gap="m">
                    <onyks-header level="6">Enter the old password</onyks-header>
                    <onyks-textfield type="password"></onyks-textfield>
                    <onyks-header level="6">Enter a new password</onyks-header>
                    <onyks-textfield  type="password"></onyks-textfield>
                    <onyks-header level="6">Repeat the new password</onyks-header>
                    <onyks-textfield  type="password"></onyks-textfield>
                </onyks-container>
                <onyks-button slot="footer" background="green">Confirm</onyks-button>
            </onyks-dialog>

            <!-- about ranks -->
            <onyks-dialog corner-close open modal title="Available ranks" bottom-buttons>
                <onyks-container gap="m">
                    <onyks-text>There are a few available ranks:</onyks-text>

                        <onyks-header level="6" cols="1">Admin</onyks-header>
                        <onyks-text cols="9">has a full access to the system; editing, deleting and other actions on all the content of the system.</onyks-text>

                        <onyks-header level="6" cols="1">Editor</onyks-header>
                        <onyks-text cols="9">has access to edit and delete the content of the system; but cannot manage the users of the system.</onyks-text>

                        <onyks-header level="6" cols="1">Viewer</onyks-header>
                        <onyks-text>has only access to view the content of the system - downloading the repository and viewing the database.</onyks-text>
                </onyks-container>
                <onyks-button slot="footer" background="green">Confirm</onyks-button>
            </onyks-dialog>

            <!-- request for a new rank -->
            <onyks-dialog corner-close open modal title="Request for a new rank" bottom-buttons>
                <onyks-container gap="m">
                    <onyks-container gap="m" type="group" align="center">
                        <onyks-header level="6">Current rank:</onyks-header>
                        <onyks-text>Editor</onyks-text>
                    </onyks-container>
                    <onyks-text>Select a new rank</onyks-text>
                </onyks-container>
                <onyks-button slot="footer" background="green">Confirm</onyks-button>
            </onyks-dialog>

            <!-- request etension -->
            <onyks-dialog corner-close modal title="Available ranks" bottom-buttons>
                <onyks-container gap="m">
                </onyks-container>
                <onyks-button slot="footer" background="green">Confirm</onyks-button>
            </onyks-dialog>
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