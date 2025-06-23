<template>
  <div class="yandex-calendar">
    <iframe
      :src="calendarUrl"
      frameborder="0"
      scrolling="no"
      class="calendar-iframe"
    ></iframe>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  tasks: {
    type: Array,
    default: () => []
  }
})

const calendarUrl = computed(() => {
  const events = props.tasks.map(task => {
    const start = new Date(task.start_date).toISOString().split('T')[0]
    const end = new Date(task.end_date).toISOString().split('T')[0]
    return `&event[${task.id}]=${encodeURIComponent(task.title)}&event_dates[${task.id}]=${start}/${end}`
  }).join('')

  return `https://calendar.yandex.ru/embed/?layerNames=work&${events}`
})
</script>

<style scoped>
.yandex-calendar {
  margin-top: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.calendar-iframe {
  width: 100%;
  height: 600px;
  border: none;
}
</style>