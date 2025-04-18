import {defineStore} from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        access: localStorage.getItem('access') || null,
        refresh: localStorage.getItem('refresh') || null,
        user: null
    }),
    actions: {
        async login(username, password) {
            const {data} = await axios.post('/api/login/', {username, password})
            this.access = data.access
            this.refresh = data.refresh
            localStorage.setItem('access', data.access)
            localStorage.setItem('refresh', data.refresh)
            axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`
            this.user = username
        },
        logout() {
            this.access = this.refresh = null
            this.user = null
            localStorage.removeItem('access')
            localStorage.removeItem('refresh')
            delete axios.defaults.headers.common['Authorization']
        }
    }
})