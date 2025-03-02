<template>
  <RouterView />
</template>


<!-- <script>
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
      if (!window.Telegram) {
        console.error('Telegram WebApp не найден');
        return;
      }
      
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
</script> -->

<script setup>
import { RouterView } from 'vue-router';

</script>