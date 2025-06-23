<template>
  <div class="invite-container">
    <h2>Войти в организацию</h2>
    <form @submit.prevent="submitInvite">
      <div class="form-group">
        <label for="invite-code">Код организации</label>
        <input
          id="invite-code"
          v-model="inviteCode"
          type="text"
          required
          placeholder="Введите код организации"
        >
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? 'Processing...' : 'Войти' }}
      </button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useOrganizationStore } from '@/stores/organization'

const organizationStore = useOrganizationStore()
const router = useRouter()
const inviteCode = ref('')
const loading = ref(false)
const error = ref(null)

const submitInvite = async () => {
  try {
    loading.value = true
    error.value = null
    await organizationStore.joinOrganization(inviteCode.value)
    router.push({ name: 'organization-detail', params: { slug: organizationStore.currentOrganization.slug } })
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to join organization'
  } finally {
    loading.value = false
  }
}
</script>