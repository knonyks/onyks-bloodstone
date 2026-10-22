import 'onyks-web-ui-system'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import { i18n } from './utils/localization'

import App from './App.vue'
import router from './router'

const pinia = createPinia()
const app = createApp(App)


app.use(router)
app.use(pinia)
app.use(i18n)
app.mount('#app')