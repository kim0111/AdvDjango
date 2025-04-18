<template>
  <div class="max-w-md mx-auto mt-16 bg-white p-6 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">Login</h2>
    <form @submit.prevent="login">
      <input v-model="username" class="w-full p-2 mb-3 border rounded" placeholder="Username"/>
      <input v-model="password" class="w-full p-2 mb-3 border rounded" type="password" placeholder="Password"/>
      <button class="bg-blue-600 text-white px-4 py-2 rounded w-full">Login</button>
    </form>
    <p v-if="error" class="text-red-500 mt-2">{{ error }}</p>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import axios from 'axios'
import {useRouter} from 'vue-router'
import {useAuthStore} from '../stores/auth'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()
const auth = useAuthStore()

const login = async () => {
  try {
    await auth.login(username.value, password.value)
    router.push('/upload')
  } catch (err) {
    error.value = 'Invalid credentials'
  }
}
</script>