import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '@/views/Dashboard.vue';
import DeviceList from '@/views/DeviceList.vue';
import DeviceRegister from '@/views/DeviceRegister.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/dashboard', name: 'Dashboard', component: Dashboard },
    { path: '/devices', name: 'DeviceList', component: DeviceList },
    { path: '/register', name: 'DeviceRegister', component: DeviceRegister }
  ]
});
export default router;
