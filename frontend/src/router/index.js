import { createRouter, createWebHistory } from 'vue-router'
import { useLoaderStore } from '../stores/loader';
import { i18n } from '../utils/localization';
import { useAuthStore } from '../stores/auth';

const routes = [
  {
    path: '/',
    redirect: 'manager/dashboard'
  },
  {
    path: '/login',
    component: () => import('../views/LoginView.vue'),
    name: 'login',
    meta: { title: 'Login - ONYKS Bloodstone', guestOnly: true }
  },
  {
    path: '/error',
    name: 'error',
    component: () => import('../views/ErrorView.vue'),
    meta: { title: 'Error - ONYKS Bloodstone' },
    beforeEnter: (to, from) => {
      if (!from.name) {
        return { name: 'dashboard', replace: true }
      }
    }
  },
  {
    path: '/manager',
    redirect: '/manager/dashboard',
    component: () => import('../views/ManagerView.vue'),
    meta: { requiresAuth: true },
    children:
    [
      {
        path: 'dashboard',
        component: () => import('../views/DashboardView.vue'),
        name: 'dashboard',
        meta: { title: i18n.global.t('common.dashboard') + ' - ONYKS Bloodstone', requiresAuth: true }
      },
      {
        path: 'management',
        name: 'management',
        component: () => import('../views/ManagementView.vue'),
        meta: { title: i18n.global.t('common.management') + ' - ONYKS Bloodstone', requiresAuth: true }
      },
      {
        path: 'repository',
        component: () => import('../views/RepositoryView.vue'),
        meta: { title: i18n.global.t('common.repository') + ' - ONYKS Bloodstone', requiresAuth: true }
      },
      {
        path: 'admin',
        component: () => import('../views/AdminView.vue'),
        meta: { title: i18n.global.t('common.admin_panel') + ' - ONYKS Bloodstone', requiresAuth: true, ranks: ['admin'] }
      },
      { 
        path: 'settings',
        component: () => import('../views/SettingsView.vue'),
        meta: { title: i18n.global.t('common.settings') + ' - ONYKS Bloodstone', requiresAuth: true }
      },
      {
        path: 'elements/create',
        name: 'element-create',
        component: () => import('../views/ElementView.vue'),
        meta: { title: i18n.global.t('elements.create') + ' - ONYKS Bloodstone', requiresAuth: true }
      },
      {
        path: 'elements/details/:uuid',
        name: 'element-details',
        component: () => import('../views/ElementView.vue'),
        meta: { title: i18n.global.t('elements.details') + ' - ONYKS Bloodstone', requiresAuth: true }
      },
      {
        path: 'elements/edit/:uuid',
        name: 'element-edit',
        component: () => import('../views/ElementView.vue'),
        meta: { title: i18n.global.t('elements.edit') + ' - ONYKS Bloodstone', requiresAuth: true }
      },
      {
        path: 'elements/duplicate/:uuid',
        name: 'element-duplicate',
        component: () => import('../views/ElementView.vue'),
        meta: { title: i18n.global.t('elements.duplicate') + ' - ONYKS Bloodstone', requiresAuth: true },
      },
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    redirect: { name: 'error', replace: true }
  }
]

const router = createRouter(
{
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from) => 
{
  document.title = to.meta.title || 'ONYKS Bloodstone';
  const auth = useAuthStore()
  await auth.init()
  const loaderStore = useLoaderStore()

  if (from.path == '/')
  {
    loaderStore.globalIsLoading = true
  }

  loaderStore.isLoading = true

  if (to.meta.requiresAuth && !auth.isLoggedIn) 
  {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.ranks && !auth.hasRank(...to.meta.ranks)) 
  {
    return { name: 'dashboard', replace: true }
  }
  if (to.meta.guestOnly && auth.isLoggedIn) 
  {
    return { name: 'dashboard', query: { redirect: to.fullPath } }
  }
  return true;
});

export default router