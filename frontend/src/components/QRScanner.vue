<script setup>
    defineProps({
        open: {
            type: Boolean,
            default: false
        }
    });
</script>

<template>
    <onyks-container class="qr-container" :class="{ 'is-open': open }" padding="m">
        <onyks-panel class="qr-panel">
            <onyks-container gap="m" type="stack">
                <!-- <onyks-container gap="m" type="stack">
                    <video></video>
                    <onyks-tag>Hide</onyks-tag>
                </onyks-container> -->
                <onyks-container gap="m" type="stack">
                    <onyks-header level="6">UUID</onyks-header>
                    <onyks-text>Example UUID</onyks-text>
                    <onyks-header level="6">Part Name</onyks-header>
                    <onyks-text>Example Part Name</onyks-text>
                    <onyks-header level="6">Manufacturer</onyks-header>
                    <onyks-text>Example Manufacturer</onyks-text>
                    <onyks-header level="6">Availability</onyks-header>
                    <onyks-text>Example Availability</onyks-text>
                    <onyks-textfield></onyks-textfield>
                    <onyks-container gap="m" type="group">
                        <onyks-tag icon="F2E6" background="red" size="xl"></onyks-tag>
                        <onyks-tag icon="F4FA" background="green" size="xl"></onyks-tag>
                        <onyks-tag icon="F8C4" background="green">Details</onyks-tag>
                    </onyks-container>
                </onyks-container>
            </onyks-container>
        </onyks-panel>
    </onyks-container>
</template>

<style scoped>
    video 
    {
        height: 200px;
        width: 100%;
        background-color: red;
        border-radius: var(--onyks-radius-md);
    }

    .qr-container
    {
        width: 100%;
        height: 100%;
        position: fixed;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        box-sizing: border-box;
        background-color: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(5px);
        align-items: end;
        justify-content: flex-end;
        opacity: 0;
        visibility: hidden;
        pointer-events: none;
        transition: opacity 500ms ease, visibility 0s linear 500ms;
    }

    .qr-container.is-open
    {
        opacity: 1;
        visibility: visible;
        pointer-events: auto;
        transition: opacity 500ms ease, visibility 0s;
    }

    .qr-panel
    {
        max-width: 600px;
        width: 100%;
        max-height: 70vh;
        height: 100%;
        box-sizing: border-box;
        align-self: center;
        transform: translateY(100%);
        transition: transform 500ms ease;
    }

    .qr-container.is-open .qr-panel
    {
        transform: translateY(0);
    }
</style>