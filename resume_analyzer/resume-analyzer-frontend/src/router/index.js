import {createRouter, createWebHistory} from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import ResumeUpload from '../components/ResumeUpload.vue'
import JobMatches from '../components/JobMatches.vue'
import Home from '../views/HomeView.vue'

const routes = [
    {path: '/', component: Home},
    {path: '/login', component: Login},
    {path: '/register', component: Register},
    {path: '/upload', component: ResumeUpload},
    {path: '/jobs', component: JobMatches},
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router