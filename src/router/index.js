import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../components/MainLayout.vue'
import HomeView from '../components/HomeView.vue'
import ProfileView from '../components/ProfileView.vue'
import LeaderboardView from '../components/LeaderboardView.vue'
import MarketView from '../components/MarketView.vue'
import TasksView from '../components/TasksView.vue'
import AdminMainLayout from '../components/AdminMainLayout.vue'
import AdminTasksView from '../components/AdminTasksView.vue'
import AdminPanelView from '../components/AdminPanelView.vue'
import AdminCreateTaskView from '../components/AdminCreateTaskView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: MainLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: HomeView
        },
        {
          path: 'profile',
          name: 'profile',
          component: ProfileView
        },
        {
          path: 'leaderboard',
          name: 'leaderboard',
          component: LeaderboardView
        },
        {
          path: 'market',
          name: 'market',
          component: MarketView
        },
        {
          path: 'tasks',
          name: 'tasks',
          component: TasksView
        }
      ]
    },
    {
      path: '/admin',
      component: AdminMainLayout,
      children: [
        {
          path: 'tasks',
          name: 'admin-tasks',
          component: AdminTasksView
        },
        {
          path: 'panel',
          name: 'admin-panel',
          component: AdminPanelView
        },
        {
          path: 'create-task',
          name: 'admin-create-task',
          component: AdminCreateTaskView
        }
      ]
    }
  ]
})

export default router