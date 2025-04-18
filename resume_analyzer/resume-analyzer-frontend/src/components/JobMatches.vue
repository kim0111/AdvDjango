<template>
  <div class="p-6">
    <h2 class="text-xl font-semibold mb-4">Job Matches</h2>
    <ul>
      <li v-for="job in jobs" :key="job.id" class="mb-3">
        <strong>{{ job.title }}</strong> at {{ job.company }}<br/>
        Score: {{ job.compatibility_score }}%
      </li>
    </ul>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import axios from 'axios'

const jobs = ref([])

onMounted(async () => {
  const {data} = await axios.get('/api/jobs/?resume_text=Senior+Python+developer')
  jobs.value = data
})
</script>