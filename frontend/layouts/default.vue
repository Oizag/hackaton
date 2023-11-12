<template>
    <VLayout class="d-flex flex-column">
        <AppBar />
        <VLayout class="pt-16 mt-2">
            <VMain>
                <slot />
            </VMain>
        </VLayout>
        <Footer />
    </VLayout>
</template>

<script setup lang="ts">
import AppBar from './AppBar.vue'
import Footer from './Footer.vue'
</script>