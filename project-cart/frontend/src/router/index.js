import { createRouter, createWebHistory } from 'vue-router'
import register_user from '../components/register_user.vue'
import login_manager from '../components/login_manager.vue'
import login_user from '../components/login_user.vue'
import welcome from '../components/welcome.vue'
import user_after_login from '../components/user_after_login.vue'
import manager_after_login from '../components/manager_after_login.vue'
import view_product from '../components/view_product.vue'
import add_product from '../components/add_product.vue'
import view_section from '../components/view_section.vue'
import add_section from '../components/add_section.vue'
import cart from '../components/cart.vue'
import user_after_login_products from '../components/user_after_login_products.vue'
import update_cart from '../components/update_cart.vue'
import checkout from '../components/checkout.vue'
import storemanager_after_login from '../components/storemanager_after_login.vue'
import storemanager_login from '../components/storemanager_login.vue'
import storemanager_signup from '../components/storemanager_signup.vue'
import error from '../components/error.vue'

import { ref } from 'vue';
export const isAuthenticated = ref(false);

const routes = [
  {path: '/login_manager',name: 'Login_Manager',component: login_manager},
  {path: '/signup',name: 'Signup',component: register_user},
  {path: '/login',name: 'Login',component: login_user},
  {path: '/',name: 'Welcome',component: welcome},
  {path: '/user_after_login',name: 'User_After_Login',component: user_after_login,meta: { requiresAuth: true }},
  {path: '/section/:sectionId/:username/products',name: 'User_After_Login_Products',component: user_after_login_products,meta: { requiresAuth: true }},
  {path: '/manager_after_login',name: 'Manager_After_Login',component: manager_after_login, meta: { requiresAuth: true }},
  {path: '/add_product',name: 'Add_Product',component: add_product},
  {path: '/view_product',name: 'View_Product',component: view_product,meta: { requiresAuth: true }},
  {path: '/add_section',name: 'Add_Section',component: add_section, meta: { requiresAuth: true }},
  {path: '/view_section',name: 'View_Section',component: view_section, meta: { requiresAuth: true }},
  {path: '/cart',name: 'Cart',component: cart, meta: { requiresAuth: true }},
  {path:'/update/:uname/:item_id',name:'Update_Cart',component:update_cart, meta: { requiresAuth: true }},
  {path:'/checkout/:username',name:'Checkout',component:checkout, meta: { requiresAuth: true }},
  {path:'/storemanager_signup',name:'Storemanager_Signup',component:storemanager_signup},
  {path:'/storemanager_login',name:'Storemanager_Login',component:storemanager_login},
  {path:'/storemanager_after_login',name:'Storemanager_After_Login',component:storemanager_after_login, meta: { requiresAuth: true }},
  {path:'/error',name:'Error',component:error},
]



const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated.value) {
      next('/error');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router
