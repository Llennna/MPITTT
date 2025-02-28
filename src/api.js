import axios from 'axios';

// Базовый URL API (можно вынести в .env)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

// Создаем экземпляр axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Метод для получения задач с преобразованием данных
export const fetchTasks = async () => {
  try {
    console.log('Начинаем загрузку задач...');
    console.log('Запрос к:', `${API_BASE_URL}/tasks`);
    
    const response = await api.get('/tasks');
    console.log('Получен ответ:', response);
    
    const tasks = response.data;
    console.log('Данные задач:', tasks);
    
    // Преобразуем данные для фронтенда
    const transformedTasks = tasks.map(task => ({
      id: task.id,
      title: task.description, // Используем description как title
      description: task.description,
      status: 'В процессе', // Статичное значение, можно доработать
      rewards: {
        points: task.points,
        boost: task.coins, // coins как boost
      },
      deadline: new Date(task.deadline).toLocaleString(), // Форматируем дату
    }));
    
    console.log('Преобразованные задачи:', transformedTasks);
    return transformedTasks;
  } catch (error) {
    console.error('Детали ошибки:', {
      message: error.message,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      config: error.config
    });
    throw error;
  }
};

// Метод для добавления задачи
export const createTask = async (taskData) => {
  try {
    const response = await api.post('/create-task', taskData);
    return response.data;
  } catch (error) {
    console.error('Ошибка при создании задачи:', error.response?.data || error.message);
    throw error;
  }
};

// Метод для получения продуктов
export const fetchProducts = async () => {
  try {
    const response = await api.get('/products');
    return response.data;
  } catch (error) {
    console.error('Ошибка при загрузке продуктов:', error.response?.data || error.message);
    throw error;
  }
};

// Метод для добавления продукта
export const createProduct = async (productData) => {
  try {
    const response = await api.post('/products', productData);
    return response.data;
  } catch (error) {
    console.error('Ошибка при создании продукта:', error.response?.data || error.message);
    throw error;
  }
};

// Метод для получения конкретного продукта по ID
export const getProduct = async (id) => {
  try {
    const response = await api.get(`/products/${id}`);
    return response.data;
  } catch (error) {
    console.error('Ошибка при загрузке продукта:', error.response?.data || error.message);
    throw error;
  }
};

// Метод для покупки продукта
export const purchaseProduct = async (data) => {
  try {
    const response = await api.post('/purchase-product', data);
    return response.data;
  } catch (error) {
    console.error('Ошибка при покупке продукта:', error.response?.data || error.message);
    throw error;
  }
};