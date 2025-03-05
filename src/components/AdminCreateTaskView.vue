<template>
  <div class="min-h-screen bg-white">
    <div class="px-4 py-4">
      <h1 class="text-xl font-bold mb-6">Создать таск</h1>
      
      <div class="text-sm text-gray-500 mb-4">Отправили на проверку</div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Title -->
        <div>
          <input
            type="text"
            v-model="form.title"
            placeholder="Заголовок"
            class="w-full px-4 py-3 rounded-lg border border-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
          />
        </div>

        <!-- Description -->
        <div>
          <textarea
            v-model="form.description"
            placeholder="Описание"
            rows="4"
            class="w-full px-4 py-3 rounded-lg border border-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
          ></textarea>
        </div>

        <!-- Deadline -->
        <div>
          <h3 class="font-medium mb-3">Дедлайн</h3>
          <input
            type="datetime-local"
            v-model="form.deadline"
            class="w-full px-4 py-3 rounded-lg border border-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
          />
        </div>

        <!-- Rewards -->
        <div>
          <h3 class="font-medium mb-3">Награда</h3>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <div class="flex items-center gap-1 mb-2">
                <Star class="w-4 h-4 text-yellow-500" />
                <span class="text-sm">Баллов</span>
              </div>
              <input
                type="number"
                v-model="form.points"
                placeholder="Баллов"
                class="w-full px-4 py-3 rounded-lg border border-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
            <div>
              <div class="flex items-center gap-1 mb-2">
                <CircleDollarSign class="w-4 h-4" />
                <span class="text-sm">BOOST</span>
              </div>
              <input
                type="number"
                v-model="form.boost"
                placeholder="Boost"
                class="w-full px-4 py-3 rounded-lg border border-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
          </div>
        </div>

        <!-- Submit -->
        <button
          type="submit"
          class="w-full py-3 bg-gray-100 rounded-lg text-gray-600 font-medium flex items-center justify-center gap-2"
        >
          <FileText class="w-5 h-5" />
          Добавить таск
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Star, CircleDollarSign, FileText } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const form = ref({
  title: '',
  description: '',
  points: '',
  boost: '',
  deadline: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().slice(0, 16) // Дефолтное значение - неделя от текущей даты
})

const handleSubmit = async () => {
  try {
    // Проверяем, что все поля заполнены
    if (!form.value.title || !form.value.description || !form.value.points || !form.value.boost || !form.value.deadline) {
      alert('Пожалуйста, заполните все поля')
      return
    }

    // Подготавливаем данные в соответствии с TaskCreate схемой
    const taskData = {
      description: `${form.value.title}\n${form.value.description}`,
      points: parseInt(form.value.points) || 0,
      coins: parseInt(form.value.boost) || 0,
      deadline: new Date(form.value.deadline).toISOString(), // Используем выбранный дедлайн
      status: "В процессе",
      user_id: null
    }

    console.log('Отправляемые данные:', JSON.stringify(taskData, null, 2))

    const response = await axios.post('http://localhost:8000/create-task', taskData)
    console.log('Ответ сервера:', response.data)

    // Очищаем форму после успешного создания
    form.value = {
      title: '',
      description: '',
      points: '',
      boost: '',
      deadline: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().slice(0, 16)
    }

    alert('Задача успешно создана!')
    router.push('/admin/tasks')

  } catch (error) {
    console.error('Полная ошибка:', error)
    console.error('Данные ошибки:', error.response?.data)
    
    let errorMessage = 'Ошибка при создании задачи: '
    if (error.response?.data?.detail) {
      errorMessage += JSON.stringify(error.response.data.detail)
    } else if (error.response?.data) {
      errorMessage += JSON.stringify(error.response.data)
    } else {
      errorMessage += error.message
    }
    
    alert(errorMessage)
  }
}
</script>