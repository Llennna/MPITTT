<template>
  <div id="app">
    <div v-if="!isAuthenticated">
      <h2>Авторизация через Telegram</h2>
      <p>Загрузка...</p>
    </div>
    <div v-else>
      <h2>Профиль пользователя</h2>
      <img :src="profile.photo_url" alt="Avatar" class="avatar" />
      <p><strong>Имя:</strong> {{ profile.first_name }}</p>
      <p><strong>Фамилия:</strong> {{ profile.last_name }}</p>
      <p><strong>Username:</strong> {{ profile.username }}</p>
      <p><strong>Очки:</strong> {{ profile.points }}</p>
      <p><strong>Монеты:</strong> {{ profile.coins }}</p>
      <p><strong>Роль:</strong> {{ profile.role }}</p>
    </div>
  </div>
  <RouterView />
</template>


<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      isAuthenticated: false,
      profile: {
        first_name: '',
        last_name: '',
        username: '',
        photo_url: '',
        points: 0,
        coins: 0,
        role: ''
      }
    };
  },
  mounted() {
    this.initTelegram();
  },
  methods: {
    async initTelegram() {
      const Telegram = window.Telegram.WebApp;
      Telegram.ready();

      const initData = Telegram.initData;

      if (initData) {
        try {
          const response = await axios.post('https://b8stify.ru/auth/telegram', {
            initData: initData
          });
          
          this.profile = response.data.profile;
          this.isAuthenticated = true;
          Telegram.expand(); // Разворачиваем приложение
        } catch (error) {
          console.error('Ошибка авторизации:', error);
          alert('Не удалось авторизоваться');
        }
      } else {
        alert('Запустите приложение через Telegram');
      }
    }
  }
};
</script>

<script setup>
import { RouterView } from 'vue-router';

</script>