<template>
    <onyks-container type="group" :class="$style.container" gap="m" align="center" justify="center" padding="m">
        <img src="../assets/logo.png">
        <img src="../../node_modules/onyks-web-ui-system/dist/logo.png">
    </onyks-container>
</template>

<style module>
    .container
    {
        height: 55px;
        width: fit-content;
    }

    .container img
    {
        height: 100%;
    }
</style>