import DashboardView from '@/views/DashboardView.vue';
import ManagementView from '@/views/ManagementView.vue';
import RepositoryView from '@/views/RepositoryView.vue';
import { createRouter, createWebHistory } from 'vue-router'
import ElementView from '@/views/ElementView.vue';
import LoginView from '@/views/LoginView.vue';
import ManagerView from '@/views/ManagerView.vue';
import AdminView from '@/views/AdminView.vue';
import SettingsView from '@/views/SettingsView.vue';
import { useLoaderStore } from '@/stores/loader';
import { i18n } from '@/utils/localization';



const routes = [
  {
    path: '/',
    redirect: 'manager/dashboard'
  },
  {
    path: '/login',
    component: LoginView,
    name: 'Login',
    meta: { title: 'Login - ONYKS Bloodstone' }
  },
  {
    path: '/manager',
    component: ManagerView,
    children: 
    [
      {
        path: 'dashboard',
        component: DashboardView,
        meta: { title: i18n.global.t('views.DashboardView.title') + ' - ONYKS Bloodstone' }
      },
      {
        path: 'management',
        component: ManagementView,
        meta: { title: i18n.global.t('views.ManagementView.title') + ' - ONYKS Bloodstone' }
      },
      {
        path: 'repository',
        component: RepositoryView,
        meta: { title: i18n.global.t('views.RepositoryView.title') + ' - ONYKS Bloodstone' }
      },
      {
        path: 'admin',
        component: AdminView,
        meta: { title: i18n.global.t('views.AdminView.title') + ' - ONYKS Bloodstone' }
      },
      {
        path: 'settings',
        component: SettingsView,
        meta: { title: i18n.global.t('views.SettingsView.title') + ' - ONYKS Bloodstone' }
      },
      {
        path: 'elements/create',
        name: 'element-create',
        component: ElementView,
        meta: { title: i18n.global.t('views.ElementView.titles.create') + ' - ONYKS Bloodstone' }
      },
      {
        path: 'elements/details/:uuid',
        name: 'element-details',
        component: ElementView,
        meta: { title: i18n.global.t('views.ElementView.titles.details') + ' - ONYKS Bloodstone' }
      },
      {
        path: 'elements/edit/:uuid',
        name: 'element-edit',
        component: ElementView,
        meta: { title: i18n.global.t('views.ElementView.titles.edit') + ' - ONYKS Bloodstone' }
      },
      {
        path: 'elements/duplicate/:uuid',
        name: 'element-duplicate',
        component: ElementView,
        meta: { title: i18n.global.t('views.ElementView.titles.duplicate') + ' - ONYKS Bloodstone' },
        props: { schema: 'duplicate' }
      },
    ]
  }
]

const router = createRouter(
{
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => 
{
  document.title = to.meta.title || 'ONYKS Bloodstone';
  const loaderStore = useLoaderStore()

  if(from.path == '/')
  {
    loaderStore.globalIsLoading = true
  }

  loaderStore.isLoading = true 
  next();
});

export default router