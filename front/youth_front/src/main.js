import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import './assets/css/global.css';  // 글로벌 스타일 파일 임포트

import VCalendar from 'v-calendar';
import 'v-calendar/style.css';

// Font Awesome CSS import
import '@fortawesome/fontawesome-free/css/all.css'

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(VCalendar, {});

app.mount("#app");

