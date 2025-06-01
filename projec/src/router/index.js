import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/home',
    name: 'home',
    component: ()=>import('../views/Home.vue'),
    meta: {title: '全国地图动态展示'}
  },
  {
    path:'/baidu',
    name:'baidu',
    component:()=>import('../views/Baidu.vue')
  },
  {
    path:'/',
    name:'screen',
    component:()=>import('../views/index.vue'),
    meta:{title: '道路交通数据可视化'}
  },
  {
    path:'/details',
    name:'details',
    component: ()=>import('../views/Details.vue'),
    meta:{title: '省份详细数据'}
  },
  {
    path:'/test',
    name:'test',
    component:()=>import('../components/test.vue'),
    meta:{title: '地图测试'}
  },
   {
     path:'/loading',
     name:'loading',
     component:()=>import('../components/loading.vue')
   }
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  window.document.title = to.meta.title
  next()
})


export default router
