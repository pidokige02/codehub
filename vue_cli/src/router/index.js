import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BibleView from '../views/BibleView.vue'
import BibleUpload from '../views/BibleUpload.vue'
import KakaoSearch from '../views/KakaoSearchView.vue'
import YouTubeSearch from '../views/YouTubeSearch.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/kakao/search/book',
    component: KakaoSearch
  },
  {
    path: '/YouTube/search',
    component: YouTubeSearch
  },
  {
    path: '/bible/view/:book/:chapter',
    name: 'BibleView',
    component: BibleView,
    props: true
  },
  {
    path: '/bible/upload',
    name: 'BibleUpload',
    component: BibleUpload
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
