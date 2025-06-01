import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import "./style.css"
import axios from 'axios'
import ElementPlus from 'element-plus'



const app = createApp(App)

app.use(router)

app.mount('#app')

app.use(axios)
app.use(ElementPlus)

// axios.defaults.withCredentials = true

