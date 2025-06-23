<template>
  <div class="comment-section">
    <h3>Comments</h3>

    <div class="comment-form">
      <textarea
        v-model="newComment"
        placeholder="Write a comment..."
        rows="3"
      ></textarea>
      <div class="form-actions">
        <input
          type="file"
          ref="fileInput"
          multiple
          @change="handleFileUpload"
          style="display: none"
        >
        <button @click="$refs.fileInput.click()" class="attach-btn">
          Attach Files
        </button>
        <button
          @click="submitComment"
          :disabled="!newComment.trim() && !attachments.length"
          class="submit-btn"
        >
          Post Comment
        </button>
      </div>

      <div v-if="attachments.length" class="attachments-preview">
        <div v-for="(file, index) in attachments" :key="index" class="attachment">
          {{ file.name }}
          <button @click="removeAttachment(index)" class="remove-btn">×</button>
        </div>
      </div>
    </div>

    <div class="comments-list">
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <div class="comment-header">
          <span class="user">{{ comment.user.full_name }}</span>
          <span class="date">{{ formatDate(comment.created_at) }}</span>
          <span v-if="comment.subtask" class="subtask-ref">
            (re: subtask "{{ comment.subtask.title }}")
          </span>
        </div>
        <div class="comment-content">
          {{ comment.content }}
        </div>
        <div v-if="comment.attachments.length" class="comment-attachments">
          <div
            v-for="attachment in comment.attachments"
            :key="attachment.id"
            class="attachment"
          >
            <a
              :href="attachment.file"
              target="_blank"
              class="attachment-link"
            >
              {{ attachment.file.split('/').pop() }}
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { formatDate } from '@/utils/date'

const props = defineProps({
  comments: {
    type: Array,
    default: () => []
  },
  entityType: {
    type: String,
    required: true,
    validator: value => ['task', 'subtask'].includes(value)
  },
  entityId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['create'])

const newComment = ref('')
const attachments = ref([])
const fileInput = ref(null)

const handleFileUpload = (event) => {
  const files = Array.from(event.target.files)
  attachments.value = [...attachments.value, ...files]
  fileInput.value.value = '' // Сбрасываем input
}

const removeAttachment = (index) => {
  attachments.value.splice(index, 1)
}

const submitComment = async () => {
  if (!newComment.value.trim() && !attachments.value.length) return

  const formData = new FormData()
  formData.append('content', newComment.value)
  formData.append(props.entityType, props.entityId)

  attachments.value.forEach(file => {
    formData.append('attachments', file)
  })

  try {
    await emit('create', formData)
    newComment.value = ''
    attachments.value = []
  } catch (error) {
    console.error('Error posting comment:', error)
  }
}
</script>

<style scoped>
.comment-section {
  margin-top: 30px;
  padding: 20px;
  border-top: 1px solid #eee;
}

.comment-form {
  margin-bottom: 20px;
}

.comment-form textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.attach-btn, .submit-btn {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.attach-btn {
  background: #f0f0f0;
}

.attach-btn:hover {
  background: #e0e0e0;
}

.submit-btn {
  background: #2196f3;
  color: white;
}

.submit-btn:hover {
  background: #1976d2;
}

.submit-btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.attachments-preview {
  margin-top: 10px;
}

.attachment {
  display: inline-flex;
  align-items: center;
  background: #f5f5f5;
  padding: 5px 10px;
  border-radius: 4px;
  margin-right: 10px;
  margin-bottom: 10px;
}

.remove-btn {
  margin-left: 8px;
  background: none;
  border: none;
  color: #ff5252;
  cursor: pointer;
  padding: 0;
}

.comments-list {
  margin-top: 20px;
}

.comment {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.comment-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.user {
  font-weight: bold;
  margin-right: 10px;
}

.date {
  margin-right: 10px;
}

.subtask-ref {
  font-style: italic;
  color: #888;
}

.comment-content {
  margin-bottom: 10px;
  white-space: pre-wrap;
}

.comment-attachments {
  margin-top: 10px;
}

.attachment-link {
  color: #2196f3;
  text-decoration: none;
}

.attachment-link:hover {
  text-decoration: underline;
}
</style>