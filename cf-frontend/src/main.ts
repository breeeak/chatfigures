import { createApp } from 'vue'
import App from './App.vue'
import router from '@/router'
import store from "@/store";
// cookie settings
import CookieConsent from 'vue-cookieconsent'
import '../node_modules/vue-cookieconsent/vendor/cookieconsent.css'
import {consentOptions} from '@/core/plugins/cookieconsent/cookieconsent-init'


/* import bootstrap */
// import 'bootstrap/scss/bootstrap.scss'
import "bootstrap";
/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import InlineSvg from 'vue-inline-svg';

const app = createApp(App)
app.use(CookieConsent, consentOptions)
app.use(store);
app.use(router);


app.component('font-awesome-icon', FontAwesomeIcon)
app.component("inline-svg",InlineSvg)
app.mount('#app')
