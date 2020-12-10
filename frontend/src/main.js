// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import BootstrapVue from 'bootstrap-vue'
import '@/../bootstrap/css/bootstrap.css'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
// import x5GMaps from 'x5-gmaps'
import * as VueGoogleMaps from 'vue2-google-maps'

Vue.use(BootstrapVue)
Vue.config.productionTip = false

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyC7g__qRA71WBebAoQPdKSbzfoUheEj_HQ',
    libraries: 'places' // If you need to use place input
  }
})

new Vue({
  router,
  render: (h) => h(App)
}).$mount('#app')
