<template>


        <div class="continer">
            <div class="zag">Главная</div>

            <div class="text">Проекты</div>
            <div class="div-block-4">
                <div class="frame-44742">
                    <div class="frame-2201">
                        <a href="#" target="_blank" class="button-style-5 icon">
                            <div class="flash">
                                <div class="flash"></div><img src="" loading="lazy" width="14" height="14" alt=""
                                    class="flash-1">
                            </div>
                        </a>
                        <div class="text-37">Хакатон MPIT 2025</div>
                    </div>
                    <div class="frame-2202">
                        <div class="frame-44743">
                            <div class="frame-44744">
                                <div class="text-38">Команда</div>
                                <div class="frame-44745">
                                    <div class="frame-2197"></div>
                                    <div class="frame-2197"></div>
                                    <div class="frame-2197"></div>
                                    <div class="frame-2197"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <a href="#" class="frame-44746 w-inline-block">
                        <div class="text-39">Посмотреть проект</div>
                    </a>
                </div>
                <div class="frame-44742">
                    <div class="frame-2201">
                        <a href="#" target="_blank" class="button-style-5 icon">
                            <div class="flash">
                                <div class="flash"></div><img src="" loading="lazy" width="14" height="14" alt=""
                                    class="flash-1">
                            </div>
                        </a>
                        <div class="text-37">Хакатон MPIT 2025</div>
                    </div>
                    <div class="frame-2202">
                        <div class="frame-44743">
                            <div class="frame-44744">
                                <div class="text-38">Команда</div>
                                <div class="frame-44745">
                                    <div class="frame-2197"></div>
                                    <div class="frame-2197"></div>
                                    <div class="frame-2197"></div>
                                    <div class="frame-2197"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <a href="#" class="frame-44746 w-inline-block">
                        <div class="text-39">Посмотреть проект</div>
                    </a>
                </div>
            </div>


            <!-- Tabs -->
            <div class="tabs-menu w-tab-menu">
                <a v-for="tab in tabs" :key="tab.id" @click="currentTab = tab.id" data-w-tab="Tab 1"
                    class="tabbb11c w-inline-block w-tab-link" :class="currentTab === tab.id ? 'w--current' : ''">
                    <img src=""
                        width="24" height="24">
                    <div class="text-20">{{ tab.name }}</div>
                </a>
            </div>




            <div v-if="currentTab === 'tasks'" class="space-y-4">
                <div class="text">Задачи</div>
                <div v-for="task in tasks" :key="task.id" class="frame-44727">
                    <!-- <div class="componentstatus">
                <div class="pending">В процессе</div>
            </div>
            <div class="componentstatus-4">
                <div class="pending-4">На проверке</div>
            </div>
            <div class="componentstatus-3">
                <div class="pending-3">Сделано</div>
            </div>
            <div class="componentstatus-2">
                <div class="pending-2">Провалено</div>
            </div> -->

                    <div class="componentstatus-3">
                        <div class="pending-3"> {{ task.status }}</div>
                    </div>
                    <div class="text-21">{{ task.title }}</div>
                    <div class="text-22">{{ task.description }}</div>
                    <div class="frame-2178">
                        <div class="frame-2175">
                            <div class="text-23">Награда:</div>
                            <div class="frame-2179">
                                <div class="text-24">⚡ {{ task.rewards.points }} Баллов</div>
                                <div class="text-25">|</div><img
                                    src=""
                                    loading="lazy" width="18" height="18" alt="" class="frame-44728">
                                <div class="text-24">{{ task.rewards.boost }} BOOST</div>
                            </div>
                        </div>
                        <div class="frame-2175">
                            <div class="text-23">Сроки:</div>
                            <div class="text-22">{{ task.deadline }}</div>
                        </div>
                    </div>
                    <a href="" class="frame-44729">
                        <div class="frame-65">
                            <div class="component-9 elements"><img
                                    src=""
                                    loading="lazy" width="24" height="24" alt="" class="file-filled">
                                <div class="label-style"> {{ task.status === 'В процессе' ? 'Отправить на проверку' :
                                    'На проверке' }}
                                </div>
                            </div>
                        </div>
                    </a>
                </div>
            </div>


            <div v-if="currentTab === 'lider'" class="lider">
                <!-- Топ-1 пользователь -->
                <div class="text">Лидер</div>
                <div class="frame-447" v-if="sortedUsers[0]">
                    <div class="frame-68">
                        <div class="imgprof">
                            <img src="https://www.gravatar.com/avatar" loading="lazy" alt="">
                        </div>
                        <div class="content-style">
                            <div class="component-copy elements-copy">
                                <div class="text">{{ sortedUsers[0].name }}</div>
                                <div class="frame-1114">
                                    <div class="text-3">Ур. {{ sortedUsers[0].level }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="component-2 elements">
                        <div class="text">⚡ {{ sortedUsers[0].points }} баллов</div>
                    </div>
                </div>

                <div class="div-block">
                    <div class="text21">Сотрудники</div>
                    <div class="texttt12">Топ 10</div>
                </div>

                <!-- Список всех пользователей -->
                <div class="div-block-3">
                    <div v-for="(user, index) in sortedUsers" :key="user.id" class="frame-44723">
                        <div class="frame-68">
                            <div class="imgprof">
                                <img src="https://www.gravatar.com/avatar" loading="lazy" alt="">
                            </div>
                            <div class="content-style">
                                <div class="component-copy elements-copy">
                                    <div class="text">{{ user.name }}</div>
                                    <div class="frame-1114">
                                        <div class="text-3">Ур. {{ user.level }}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="component-2 elements">
                            <div class="text">#{{ index + 1 }} | ⚡ {{ user.points }} баллов</div>
                        </div>
                    </div>
                </div>
            </div>




        </div>



</template>


<style>
.lider {
    grid-column-gap: 12px;
    grid-row-gap: 12px;
    flex-flow: column;
    display: flex;
    overflow: hidden;
}

.mt-4 {
    margin-top: 1rem;
}
</style>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Star, CircleDollarSign, FileText } from 'lucide-vue-next'
import axios from 'axios'

const currentTab = ref('tasks')
const tasks = ref([])
const users = ref([])

const tabs = [
    { id: 'tasks', name: 'Задачи' },
    { id: 'lider', name: 'Лидерборд' }
]

// Сортированный список пользователей по баллам
const sortedUsers = computed(() => {
    return [...users.value].sort((a, b) => (b.points || 0) - (a.points || 0))
})

// Функция для загрузки задач из БД
const fetchTasks = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/tasks')
        tasks.value = response.data.map(task => ({
            id: task.id,
            status: task.status || 'В процессе',
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
        }))
    } catch (error) {
        console.error('Ошибка при загрузке задач:', error)
    }
}

// Функция для загрузки лидерборда
const fetchLeaderboard = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/leaderboard')
        users.value = response.data
        console.log('Полученные данные:', response.data) // Для отладки
    } catch (error) {
        console.error('Ошибка при загрузке лидерборда:', error)
        users.value = []
    }
}

// Загружаем данные при монтировании компонента
onMounted(() => {
    fetchTasks()
    fetchLeaderboard()
})
</script>