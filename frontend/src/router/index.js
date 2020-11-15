import Vue from 'vue'
import Router from 'vue-router'
import LlistatMotos from '@/components/LlistatMotos'
// import Login from '@/components/Login'
import 'bootstrap'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'LlistatMotos',
      component: LlistatMotos
    },
    {
      path: '/home',
      name: 'LlistatMotos',
      component: LlistatMotos
    }
  ]
})
