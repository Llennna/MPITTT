<template>
  <div class="continer">
    <div class="zag">Таски</div>

    <!-- Tabs -->
    <div class="tabs-menu w-tab-menu">
      <a v-for="tab in tabs" :key="tab.id" @click="currentTab = tab.id" data-w-tab="Tab 1"
        class="tabbb11c w-inline-block w-tab-link" :class="currentTab === tab.id ? 'w--current' : ''">
        <img src="../../b8stify.webflow.io/67bf26ad9cb30c9bdf27f087/67bf3d842cd0e8c51e6e431b_trophy.svg" width="24"
          height="24">
        <div class="text-20">{{ tab.name }}</div>
      </a>
    </div>

    <!-- Активные задачи -->
    <div v-if="currentTab === 'tasks'" class="space-y-4">
      <div v-for="task in activeTasks" :key="task.id" class="frame-44727">
        <!-- Статус задачи -->
        <div :class="{
          'componentstatus': task.status === 'В процессе',
          'componentstatus-4': task.status === 'На проверке'
        }">
          <div :class="{
            'pending': task.status === 'В процессе',
            'pending-4': task.status === 'На проверке'
          }">{{ task.status }}</div>
        </div>

        <div class="text-21">{{ task.title }}</div>
        <div class="text-22">{{ task.description }}</div>
        <div class="frame-2178">
          <div class="frame-2175">
            <div class="text-23">Награда:</div>
            <div class="frame-2179">
              <div class="text-24">⚡ {{ task.rewards.points }} Баллов</div>
              <div class="text-25">|</div>
              <img
                src="../../b8stify.webflow.io/67bf26ad9cb30c9bdf27f087/67bf3e32c809cc85f7d64c2a_Frame-1114.svg"
                loading="lazy" width="18" height="18" alt="" class="frame-44728">
              <div class="text-24">{{ task.rewards.boost }} BOOST</div>
            </div>
          </div>
          <div class="frame-2175">
            <div class="text-23">Сроки:</div>
            <div class="text-22">{{ task.deadline }}</div>
          </div>
        </div>
        <div class="frame-44729" @click="updateTaskStatus(task)">
          <div class="frame-65">
            <div class="component-9 elements">
              <img
                src="../../b8stify.webflow.io/67bf26ad9cb30c9bdf27f087/67bf3e338898d8365b6f0858_file-filled.svg"
                loading="lazy" width="24" height="24" alt="" class="file-filled">
              <div class="label-style">
                {{ getActionButtonText(task.status) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Уведомления о выполненных и проваленных задачах -->
    <div v-if="currentTab === 'notifications'" class="space-y-4">
      <div v-for="task in completedTasks" :key="task.id" class="frame-44727">
        <!-- Статус задачи -->
        <div :class="{
          'componentstatus-3': task.status === 'Сделано',
          'componentstatus-2': task.status === 'Провалено'
        }">
          <div :class="{
            'pending-3': task.status === 'Сделано',
            'pending-2': task.status === 'Провалено'
          }">{{ task.status }}</div>
        </div>

        <div class="text-21">{{ task.title }}</div>
        <div class="text-22">{{ task.description }}</div>
        <div class="frame-2178">
          <div class="frame-2175">
            <div class="text-23">Награда:</div>
            <div class="frame-2179">
              <div class="text-24">⚡ {{ task.rewards.points }} Баллов</div>
              <div class="text-25">|</div>
              <img
                src="../../b8stify.webflow.io/67bf26ad9cb30c9bdf27f087/67bf3e32c809cc85f7d64c2a_Frame-1114.svg"
                loading="lazy" width="18" height="18" alt="" class="frame-44728">
              <div class="text-24">{{ task.rewards.boost }} BOOST</div>
            </div>
          </div>
          <div class="frame-2175">
            <div class="text-23">Сроки:</div>
            <div class="text-22">{{ task.deadline }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const currentTab = ref('tasks');
const tasks = ref([]);

const tabs = [
  { id: 'tasks', name: 'Задачи' },
  { id: 'notifications', name: 'Уведомления' }
];

// Фильтрация активных задач (В процессе и На проверке)
const activeTasks = computed(() => {
  return tasks.value.filter(task => 
    task.status === 'В процессе' || task.status === 'На проверке'
  );
});

// Фильтрация выполненных и проваленных задач
const completedTasks = computed(() => {
  return tasks.value.filter(task => 
    task.status === 'Сделано' || task.status === 'Провалено'
  );
});

// Функция для получения текста кнопки действия в зависимости от статуса
const getActionButtonText = (status) => {
  switch (status) {
    case 'В процессе':
      return 'Отправить на проверку';
    case 'На проверке':
      return 'На проверке';
    default:
      return 'Отправить на проверку';
  }
};

// Функция для обновления статуса задачи
const updateTaskStatus = async (task) => {
  if (task.status === 'В процессе') {
    try {
      await axios.put(`http://127.0.0.1:8000/tasks/${task.id}/status`, {
        status: 'На проверке'
      });
      task.status = 'На проверке';
    } catch (error) {
      console.error('Ошибка при обновлении статуса:', error);
    }
  }
};

// Функция для загрузки задач из БД
const fetchTasks = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/tasks');
    tasks.value = response.data.map(task => ({
      id: task.id,
      status: task.status,
      title: task.description,
      description: task.description,
      rewards: {
        points: task.points,
        boost: task.coins
      },
      deadline: new Date(task.deadline).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    }));
  } catch (error) {
    console.error('Ошибка при загрузке задач:', error);
  }
};

// Загружаем задачи при монтировании компонента
onMounted(() => {
  fetchTasks();
});
</script>

<style>
.componentstatus {
  background-color: #FFF7E6;
  padding: 4px 8px;
  border-radius: 4px;
}

.componentstatus-2 {
  background-color: #FFE6E6;
  padding: 4px 8px;
  border-radius: 4px;
}

.componentstatus-3 {
  background-color: #E6FFE6;
  padding: 4px 8px;
  border-radius: 4px;
}

.componentstatus-4 {
  background-color: #E6F0FF;
  padding: 4px 8px;
  border-radius: 4px;
}

.pending {
  color: #FF9900;
}

.pending-2 {
  color: #FF0000;
}

.pending-3 {
  color: #00CC00;
}

.pending-4 {
  color: #0066FF;
}
</style>