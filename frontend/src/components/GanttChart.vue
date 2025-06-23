<template>
  <div class="gantt-container">
    <div class="gantt-header">
      <div class="gantt-title">Project Timeline</div>
      <div class="gantt-timeframe">
        {{ formatDate(timeframe.start) }} - {{ formatDate(timeframe.end) }}
      </div>
    </div>

    <div class="gantt-chart" ref="ganttChart">
      <div class="gantt-grid">
        <div
          v-for="day in days"
          :key="day.date"
          class="gantt-day"
          :class="{ 'weekend': day.isWeekend }"
        >
          <div class="day-label">{{ day.label }}</div>
        </div>
      </div>

      <div
        v-for="task in tasks"
        :key="task.id"
        class="gantt-task"
        :style="taskStyle(task)"
        :title="taskTooltip(task)"
      >
        <div class="task-bar"></div>
        <div class="task-label">{{ task.title }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { formatDate } from '@/utils/date'

const props = defineProps({
  tasks: {
    type: Array,
    required: true
  }
})

const ganttChart = ref(null)
const chartWidth = ref(0)

onMounted(() => {
  updateChartWidth()
  window.addEventListener('resize', updateChartWidth)
})

const updateChartWidth = () => {
  if (ganttChart.value) {
    chartWidth.value = ganttChart.value.offsetWidth
  }
}

const timeframe = computed(() => {
  if (!props.tasks.length) {
    return { start: new Date(), end: new Date() }
  }

  const startDates = props.tasks.map(t => new Date(t.start_date))
  const endDates = props.tasks.map(t => new Date(t.end_date))

  return {
    start: new Date(Math.min(...startDates)),
    end: new Date(Math.max(...endDates))
  }
})

const days = computed(() => {
  const daysArray = []
  const current = new Date(timeframe.value.start)
  const end = new Date(timeframe.value.end)

  while (current <= end) {
    daysArray.push({
      date: new Date(current),
      label: current.getDate(),
      isWeekend: current.getDay() === 0 || current.getDay() === 6
    })
    current.setDate(current.getDate() + 1)
  }

  return daysArray
})

const dayWidth = computed(() => {
  if (!days.value.length || !chartWidth.value) return 0
  return chartWidth.value / days.value.length
})

const taskStyle = (task) => {
  const startDate = new Date(task.start_date)
  const endDate = new Date(task.end_date)

  const daysFromStart = Math.floor(
    (startDate - timeframe.value.start) / (1000 * 60 * 60 * 24)
  )
  const durationDays = Math.ceil(
    (endDate - startDate) / (1000 * 60 * 60 * 24)
  ) + 1

  return {
    left: `${daysFromStart * dayWidth.value}px`,
    width: `${durationDays * dayWidth.value}px`,
    backgroundColor: getPriorityColor(task.priority)
  }
}

const taskTooltip = (task) => {
  return `
    ${task.title}
    Start: ${formatDate(task.start_date)}
    End: ${formatDate(task.end_date)}
    Status: ${task.status}
    Priority: ${task.priority}
  `
}

const getPriorityColor = (priority) => {
  const colors = {
    high: '#ff5252',
    medium: '#ffc107',
    low: '#4caf50',
    unknown: '#9e9e9e'
  }
  return colors[priority] || colors.unknown
}
</script>

<style scoped>
.gantt-container {
  margin-top: 30px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.gantt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
}

.gantt-title {
  font-weight: bold;
}

.gantt-timeframe {
  font-size: 0.9em;
  color: #666;
}

.gantt-chart {
  position: relative;
  height: 400px;
  overflow-x: auto;
  padding-top: 30px;
}

.gantt-grid {
  display: flex;
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
}

.gantt-day {
  flex-shrink: 0;
  width: 40px;
  height: 100%;
  border-right: 1px solid #f0f0f0;
  text-align: center;
}

.gantt-day.weekend {
  background-color: #f9f9f9;
}

.day-label {
  font-size: 0.8em;
  padding: 5px;
  border-bottom: 1px solid #e0e0e0;
}

.gantt-task {
  position: absolute;
  height: 30px;
  margin-top: 5px;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
}

.task-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0.2;
}

.task-label {
  position: relative;
  padding: 5px 8px;
  font-size: 0.85em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>