<template>
  <div class="min-h-screen bg-gray-50">
    <main class="pb-16">
      <RouterView />
    </main>

    <!-- Bottom Navigation -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200">
      <div class="flex justify-around">
        <RouterLink 
          v-for="item in navigation" 
          :key="item.name"
          :to="item.to"
          class="flex flex-col items-center py-2 px-4"
          :class="route.path === item.to ? 'text-green-500' : 'text-gray-400'"
        >
          <component :is="item.icon" class="w-6 h-6" />
          <span class="text-xs mt-1">{{ item.name }}</span>
        </RouterLink>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { Home, Trophy, ShoppingCart, ClipboardList, Settings } from 'lucide-vue-next'

const route = useRoute()

const navigation = [
  { name: 'Главная', to: '/', icon: Home },
  // { name: 'Лидеры', to: '/leaderboard', icon: Trophy },
  { name: 'Магазин', to: '/market', icon: ShoppingCart },
  { name: 'Задачи', to: '/tasks', icon: ClipboardList },
  { name: 'Админ', to: '/admin/tasks', icon: Settings }
]
</script>