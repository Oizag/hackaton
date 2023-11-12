<template>
    <VContainer
        fluid
        class="d-flex justify-center align-center py-0 px-0"
    >
        <VFooter
            color="#262525"
            :elevation="18"
            class="d-flex justify-space-between align-center"
            height="100"
        >
            <NuxtLink
                to="https://www.rzd.ru/"
                target="_blank"
            >
                <VBtn
                    variant="text"
                    width="125"
                    height="100"
                >
                    <VImg
                        :src="logoRzhd"
                        min-width="100"
                        min-height="100"
                    />
                </VBtn>
            </NuxtLink>
            <p class="text-subtitle-1 font-weight-bold">2023 - team "template"</p>
            <NuxtLink to="">
                <VBtn
                    variant="text"
                    icon
                    width="90"
                    height="90"
                >
                    <VImg
                        :src="logoGit"
                        min-width="70"
                        min-height="70"
                    />
                </VBtn>
            </NuxtLink>
        </VFooter>
    </VContainer>
</template>

<script setup lang="ts">
import logoRzhd from 'images/logo_rzhd.svg'
import logoGit from 'images/logo_git.svg'
</script>