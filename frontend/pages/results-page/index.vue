<template>
    <VContainer class="results pa-16 d-flex flex-column justify-center align-center ">
        <p class="results__title text-h5 font-weight-bold text-white">Результаты</p>

        <VCard class="w-auto h-auto pa-4 d-flex flex-row">
            <video
                class="results-card__video"
                :src="srcs"
                controls
                height="300"
                width="500"
            />
            <div class="results-card__info d-flex flex-column justify-start align-center ms-4">
                <p class="text-h5"> Название файла:</p>
                <p class="text-h6">{{ $route.query.nameFile }}</p>
                <p class="text-h5"> Частые действия:</p>
                <p
                    class="text-h6"
                    v-for="key in jsData"
                >{{ jsData(key) }}</p>
            </div>
        </VCard>
    </VContainer>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const router = useRouter()
const srcs = ref()
const jsData = ref()

srcs.value = `http://127.0.0.1:5000/static/${router.currentRoute.value.query.nameFile}`
jsData.value = router.currentRoute.value.query.jsData

</script>