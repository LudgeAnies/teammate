<template>
  <div class="checklist">
    <h3>Checklist</h3>
    <div class="checklist-items">
      <div
        v-for="(item, index) in items"
        :key="item.id || index"
        class="checklist-item"
        :class="{ completed: item.is_completed }"
      >
        <input
          type="checkbox"
          v-model="item.is_completed"
          @change="updateItem(item)"
        >
        <input
          type="text"
          v-model="item.title"
          @blur="updateItem(item)"
          placeholder="Checklist item"
        >
        <button @click="deleteItem(item)" class="delete-btn">×</button>
      </div>
    </div>
    <button @click="addItem" class="add-btn">+ Add Item</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  entityType: {
    type: String,
    required: true,
    validator: value => ['project', 'task', 'subtask'].includes(value)
  },
  entityId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update', 'create', 'delete'])

const addItem = () => {
  const newItem = {
    title: '',
    is_completed: false,
    [props.entityType]: props.entityId
  }
  emit('create', newItem)
}

const updateItem = (item) => {
  if (item.id) {
    emit('update', item)
  } else if (item.title.trim()) {
    emit('create', item)
  }
}

const deleteItem = (item) => {
  if (item.id) {
    emit('delete', item.id)
  } else {
    // Удаляем из локального массива, если элемент не сохранен
    const index = props.items.findIndex(i => i === item)
    if (index !== -1) {
      emit('update-items', props.items.filter((_, i) => i !== index))
    }
  }
}
</script>

<style scoped>
.checklist {
  margin-top: 20px;
  padding: 15px;
  background: #f5f5f5;
  border-radius: 8px;
}

.checklist h3 {
  margin-top: 0;
  margin-bottom: 10px;
}

.checklist-items {
  margin-bottom: 10px;
}

.checklist-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  padding: 8px;
  background: white;
  border-radius: 4px;
}

.checklist-item.completed {
  opacity: 0.7;
}

.checklist-item input[type="text"] {
  flex-grow: 1;
  margin: 0 10px;
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.checklist-item input[type="checkbox"] {
  margin-right: 10px;
}

.delete-btn {
  background: none;
  border: none;
  color: #ff5252;
  font-size: 20px;
  cursor: pointer;
  padding: 0 5px;
}

.add-btn {
  background: #4caf50;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
}

.add-btn:hover {
  background: #388e3c;
}
</style>