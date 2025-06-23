<template>
  <div
    class="task-card"
    :class="{
      'high-priority': task.priority === 'high',
      'medium-priority': task.priority === 'medium',
      'low-priority': task.priority === 'low'
    }"
    draggable="true"
    @dragstart="onDragStart"
    @dragend="onDragEnd"
  >
    <div class="task-header">
      <h3>{{ task.title }}</h3>
      <span class="task-status">{{ task.status }}</span>
    </div>
    <div class="task-body">
      <p>{{ task.description }}</p>
      <div class="task-meta">
        <span>Deadline: {{ formatDate(task.end_date) }}</span>
        <span>Assigned to: {{ task.assignees.join(', ') }}</span>
      </div>
    </div>
    <div class="task-actions">
      <button @click="openTaskDetails">Details</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { formatDate } from '@/utils/date'

const props = defineProps({
  task: {
    type: Object,
    required: true
  }
})

const router = useRouter()
const isDragging = ref(false)

const onDragStart = (e) => {
  isDragging.value = true
  e.dataTransfer.setData('task/id', props.task.id)
  e.dataTransfer.effectAllowed = 'move'
}

const onDragEnd = () => {
  isDragging.value = false
}

const openTaskDetails = () => {
  router.push({
    name: 'task-detail',
    params: {
      orgSlug: props.task.organization_slug,
      projectSlug: props.task.project_slug,
      taskId: props.task.id
    }
  })
}
</script>

<style scoped>
.task-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 16px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
  cursor: grab;
}

.task-card:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  transform: translateY(-2px);
}

.task-card.high-priority {
  border-left: 4px solid #ff5252;
}

.task-card.medium-priority {
  border-left: 4px solid #ffc107;
}

.task-card.low-priority {
  border-left: 4px solid #4caf50;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.task-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
}

.task-body {
  margin-bottom: 12px;
}

.task-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #666;
}

.task-actions {
  display: flex;
  justify-content: flex-end;
}
</style>