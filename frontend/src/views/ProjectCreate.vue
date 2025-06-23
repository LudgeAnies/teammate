<template>
  <div class="project-create">
    <h2>Create New Project</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="name">Project Name</label>
        <input id="name" v-model="form.name" required>
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea id="description" v-model="form.description"></textarea>
      </div>

      <div class="form-group">
        <label for="deadline">Deadline</label>
        <input id="deadline" v-model="form.deadline" type="datetime-local">
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Creating...' : 'Create Project' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProjectStore } from '@/stores/project'

const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()

const form = ref({
  name: '',
  description: '',
  deadline: null
})

const loading = ref(false)

const submitForm = async () => {
  try {
    loading.value = true
    const project = await projectStore.createProject(route.params.orgSlug, form.value)
    router.push({
      name: 'project-detail',
      params: {
        orgSlug: route.params.orgSlug,
        projectSlug: project.slug
      }
    })
  } finally {
    loading.value = false
  }
}
</script>