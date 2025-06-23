<template>
  <div class="task-create">
    <h2>Create New Task</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="title">Title</label>
        <input id="title" v-model="form.title" required>
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea id="description" v-model="form.description"></textarea>
      </div>

      <div class="form-group">
        <label for="type">Type</label>
        <select id="type" v-model="form.type">
          <option value="task">Task</option>
          <option value="development">Development</option>
          <option value="idea">Idea</option>
          <option value="research">Research</option>
        </select>
      </div>

      <div class="form-group">
        <label for="priority">Priority</label>
        <select id="priority" v-model="form.priority">
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
      </div>

      <div class="form-group">
        <label for="start_date">Start Date</label>
        <input id="start_date" v-model="form.start_date" type="datetime-local">
      </div>

      <div class="form-group">
        <label for="end_date">End Date</label>
        <input id="end_date" v-model="form.end_date" type="datetime-local">
      </div>

      <div class="form-group">
        <label>Assign Roles</label>
        <div class="assignments">
          <div v-for="user in availableUsers" :key="user.id" class="user-assignment">
            <label>
              <input
                type="checkbox"
                v-model="form.assignments[user.id].assigned"
                @change="handleAssignmentChange(user.id)"
              >
              {{ user.full_name }}
            </label>
            <select
              v-model="form.assignments[user.id].role"
              :disabled="!form.assignments[user.id].assigned"
            >
              <option value="executor">Executor</option>
              <option value="responsible">Responsible</option>
            </select>
          </div>
        </div>
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Creating...' : 'Create Task' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const taskStore = useTaskStore()
const userStore = useUserStore()

const form = ref({
  title: '',
  description: '',
  type: 'task',
  priority: 'medium',
  start_date: null,
  end_date: null,
  assignments: {}
})

const availableUsers = ref([])
const loading = ref(false)

onMounted(async () => {
  // Загружаем пользователей проекта
  availableUsers.value = await userStore.fetchProjectUsers(
    route.params.orgSlug,
    route.params.projectSlug
  )

  // Инициализируем assignments
  availableUsers.value.forEach(user => {
    form.value.assignments[user.id] = {
      assigned: false,
      role: 'executor'
    }
  })
})

const handleAssignmentChange = (userId) => {
  if (!form.value.assignments[userId].assigned) {
    form.value.assignments[userId].role = 'executor'
  }
}

const submitForm = async () => {
  try {
    loading.value = true

    // Формируем данные для отправки
    const taskData = {
      ...form.value,
      assignments: Object.entries(form.value.assignments)
        .filter(([_, assignment]) => assignment.assigned)
        .map(([userId, assignment]) => ({
          user_id: userId,
          role: assignment.role
        }))
    }

    const task = await taskStore.createTask(
      route.params.orgSlug,
      route.params.projectSlug,
      taskData
    )

    router.push({
      name: 'task-detail',
      params: {
        orgSlug: route.params.orgSlug,
        projectSlug: route.params.projectSlug,
        taskId: task.id
      }
    })
  } finally {
    loading.value = false
  }
}
</script>