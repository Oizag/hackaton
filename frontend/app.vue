<template>
    <VApp class="">
        <NuxtLayout style="background-color: #363535 !important;">
            <NuxtPage />
        </NuxtLayout>
    </VApp>
</template>

<script setup lang="ts">
useHead({
    title: 'Flow Sentinel',
    link: [
        {
            rel: 'icon',
            href: 'favicon.ico',
        },
    ],
})
</script>