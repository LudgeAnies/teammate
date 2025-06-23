<template>
  <div class="deadline-info">
    <div v-if="workingDays !== null">
      Working days: {{ workingDays }} ({{ workingHours }} hours)
    </div>
    <div v-if="isDeadlineWarning" class="warning">
      Warning: Deadline is on a non-working day!
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { CalendarAPI } from '@/api/calendar'

const props = defineProps({
  startDate: String,
  endDate: String
})

const workingDays = ref(null)
const workingHours = ref(null)
const isDeadlineWarning = ref(false)

const updateWorkingDays = async () => {
  if (!props.startDate || !props.endDate) {
    workingDays.value = null
    workingHours.value = null
    return
  }

  workingDays.value = await CalendarAPI.getWorkingDaysCount(props.startDate, props.endDate)
  workingHours.value = workingDays.value * 8

  // Проверяем, является ли дедлайн рабочим днем
  isDeadlineWarning.value = !(await CalendarAPI.isWorkingDay(props.endDate))
}

onMounted(updateWorkingDays)
watch(() => [props.startDate, props.endDate], updateWorkingDays)
</script>

<style scoped>
.deadline-info {
  font-size: 0.9em;
  color: #666;
  margin-top: 10px;
}

.warning {
  color: #ff5252;
  font-weight: bold;
  margin-top: 5px;
}
</style>