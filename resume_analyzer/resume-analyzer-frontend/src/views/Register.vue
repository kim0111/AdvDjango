<template>
  <div class="max-w-md mx-auto mt-16 bg-white p-6 rounded shadow">
    <h2 class="text-xl font-semibold mb-4">Register</h2>
    <form @submit.prevent="register">
      <input v-model="username" class="w-full p-2 mb-3 border rounded" placeholder="Username"/>
      <input v-model="email" class="w-full p-2 mb-3 border rounded" placeholder="Email"/>
      <input v-model="password" class="w-full p-2 mb-3 border rounded" type="password" placeholder="Password"/>
      <select v-model="role" class="w-full p-2 mb-3 border rounded">
        <option value="job_seeker">Job Seeker</option>
        <option value="recruiter">Recruiter</option>
        <option value="admin">Admin</option>
      </select>
      <button class="bg-green-600 text-white px-4 py-2 rounded w-full">Register</button>
    </form>
    <p v-if="message" class="text-green-600 mt-2">{{ message }}</p>
    <p v-if="error" class="text-red-500 mt-2">{{ error }}</p>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import axios from 'axios'

const username = ref('')
const email = ref('')
const password = ref('')
const role = ref('job_seeker')
const message = ref('')
const error = ref('')

const register = async () => {
  try {
    await axios.post('/api/auth/users/', {
      username: username.value,
      email: email.value,
      password: password.value,
      role: role.value,
    })
    message.value = '✅ Registration successful! Check your email to activate account.'
    error.value = ''
  } catch (err) {
    error.value = '❌ Registration failed. Check inputs.'
    message.value = ''
  }
}
</script>