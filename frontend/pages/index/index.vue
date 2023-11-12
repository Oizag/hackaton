<template>
    <VContainer class="d-flex flex-column align-center pa-2 pa-md-16 mt-16 ">
        <p class="text-h5 font-weight-bold text-white">Здесь Вы можете загрузить свое видео!</p>
        <VImg
            :src="trainImg"
            width="500"
            style="position: absolute !important; left:0 !important; opacity: 0.9;"
        />

        <VImg
            :src="trainRight"
            width="500"
            style="position: absolute !important; right:0 !important; bottom:0 !important; opacity: 0.9;"
        />

        <VFileInput
            drag-target
            variant="solo-filled"
            class="drag-input w-50 mt-16 text-white"
            center-affix
            rounded="100"
            bg-color="#534B4B"
            label="Choose or move file"
            type="file"
            @change="onFileChange"
            accept="video/mp4"
            density="comfortable"
        />
        <v-snackbar
            v-model="snackbar"
            :timeout="timeout"
            color="error"
            class="mb-16"
        >
            <p class="font-weight-bold"> Выберите другой файл</p>
        </v-snackbar>
        <VSnackbar
            v-model="isUpload"
            color="gray"
            location="top"
            timeout="-1"
            class="d-flex flex-column justify-center align-center"
        > <v-progress-circular
                :width="5"
                :size="50"
                color="red"
                indeterminate
            ></v-progress-circular>
            <p class="text-subtitle-1 text-white">Пожалуйста, ожидайте</p>
        </VSnackbar>
    </VContainer>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import trainImg from 'images/img_train.png'
import trainRight from 'images/train_right.png'
const router = useRouter()
// Для снэкбара
const snackbar = ref(false)
const timeout = 2000
const isUpload = ref(false)

const myFile = ref<File | null>(null);
const jsData = ref()

// Обработчик события change для vfileinput
const onFileChange = (event: FileInputEvent) => {

    if (!event.target.files[0].type.match('video/mp4')) {
        snackbar.value = true
    }
    else {
        // Получаем файл, выбранный пользователем
        myFile.value = event.target.files[0];
        // Get filename
        const filesName = myFile.value.name;
        // Добавляем файл в запрос
        const formData = new FormData();
        formData.append("file", myFile.value);

        // Отправляем файл на сервер
        uploadFile(formData);
        getResults(filesName);
    }
};

async function uploadFile(formData: FormData) {
    // Создаем запрос POST к серверу Flask
    const response = await fetch("http://localhost:5000/api/upload", {
        method: "POST",
        body: formData,
    });
};

async function getResults(filename) {
    isUpload.value = true
    // Создаем запрос POST к серверу Flask
    const response = await fetch(`http://localhost:5000/api/analyse/${filename}`)
        .then((response) => response.json())
        .then((data) => {
            jsData.value = data
            alert(jsData.value)
        })
        .then(() => {
            router.push({
                path: "/results-page",
                query: {
                    jsData: jsData.value,
                    nameFile: filename,
                }
            });
        });
};



</script>