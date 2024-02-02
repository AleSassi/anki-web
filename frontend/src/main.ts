import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import 'vuetify/styles'
import { createVuetify, type ThemeDefinition } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import Toast from "vue-toastification";
import { type PluginOptions, POSITION } from 'vue-toastification';
// Import the CSS or use your own!
import "vue-toastification/dist/index.css";

// Import our custom CSS
import './assets/styles.scss'

// Import all of Bootstrap's JS
import * as bootstrap from 'bootstrap'

const darkTheme: ThemeDefinition = {
    dark: true,
}

const vuetify = createVuetify({
    components,
    directives,
    theme: {
        defaultTheme: 'darkTheme',
        themes: {
            darkTheme
        }
    }
})

const toast_options: PluginOptions = {
    // You can set your default options here
    position: POSITION.TOP_RIGHT,
};

const app = createApp(App)

app.use(createPinia())
app.use(vuetify)
app.use(router)
app.use(Toast, toast_options);

app.mount('#app')
