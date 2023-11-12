import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'
import { fileURLToPath } from 'node:url'

export default defineNuxtConfig({
    devtools: { enabled: false },
    alias: {
        images: fileURLToPath(new URL('./assets/images', import.meta.url)),
        models: fileURLToPath(new URL('./models', import.meta.url)),
        utils: fileURLToPath(new URL('./utils', import.meta.url)),
    },

    build: {
        transpile: ['vuetify'],
    },

    experimental: {
        reactivityTransform: false,
        inlineSSRStyles: false,
    },

    modules: [
        (_options, nuxt) => {
            nuxt.hooks.hook('vite:extendConfig', (config) => {
                config.plugins.push(vuetify({ autoImport: true }))
            })
        },
    ],

    vite: {
        vue: {
            template: {
                transformAssetUrls,
            },
        },
    },

    css: [
        '@mdi/font/css/materialdesignicons.css',
        'assets/scss/main.scss',
    ],

    srcDir: '.',

    ssr: false,
})