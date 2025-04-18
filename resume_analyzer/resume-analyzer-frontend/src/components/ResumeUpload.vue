<template>
  <div class="p-6">
    <h2 class="text-xl font-semibold mb-4">Upload your resume</h2>
    <input type="file" @change="upload"/>
    <p v-if="response">✅ {{ response.original_file_name }} uploaded</p>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import axios from 'axios'

const response = ref(null)

const upload = async (e) => {
  const file = e.target.files[0]
  const formData = new FormData()
  formData.append('original_file', file)
  const {data} = await axios.post('/api/resumes/', formData)
  response.value = data
}
</script>