// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import BootstrapVue from 'bootstrap-vue'
import '@/../bootstrap/css/bootstrap.css'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
// import x5GMaps from 'x5-gmaps'

Vue.use(BootstrapVue)
Vue.config.productionTip = false
// Vue.use(x5GMaps, { key: 'AIzaSyD_8CnauFmnvQZ1zuOhY4SGIdwc3MoBbO4', libraries: ['visualization'] })

new Vue({
  router,
  render: (h) => h(App)
}).$mount('#app')
