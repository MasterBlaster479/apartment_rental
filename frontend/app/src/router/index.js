import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Calendars from '../views/Calendars.vue'
import { isLoggedIn } from '../utils/auth'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
    meta: {
        allowAnonymous: true
    }
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: {
        allowAnonymous: true
    }
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: {
        allowAnonymous: true
    }
  },
  {
    path: '/calendars',
    name: 'calendars',
    component: Calendars,
    meta: {
        allowAnonymous: false
    }
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (!to.meta.allowAnonymous && !isLoggedIn()) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  }
  else {
    next()
  }
})

export default router
