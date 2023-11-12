<template>
    <VAppBar
        :absolute="isAbs"
        color="#AD2A2A"
        class="pa-2"
    >
        <div class="px-16 d-flex justify-center align-center w-100">
            <NuxtLink to="/">
                <VImg
                    :src="Logo"
                    width="55"
                    height="55"
                    max-width="55"
                    max-height="55"
                />
            </NuxtLink>
        </div>
    </VAppBar>
</template>

<script setup lang="ts">
import Logo from "../assets/images/logo.png"

const isAbs = ref(false)
</script>