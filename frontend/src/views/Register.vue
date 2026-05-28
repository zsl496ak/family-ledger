<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="title">注册账户</h1>
      <el-tabs v-model="tab">
        <el-tab-pane label="创建家庭" name="create">
          <el-form :model="createForm" :rules="rules" ref="createFormRef" @submit.prevent="handleCreate">
            <el-form-item prop="username">
              <el-input v-model="createForm.username" placeholder="用户名" prefix-icon="User" size="large" />
            </el-form-item>
            <el-form-item prop="email">
              <el-input v-model="createForm.email" placeholder="邮箱" prefix-icon="Message" size="large" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="createForm.password" type="password" placeholder="密码" prefix-icon="Lock" size="large" show-password />
            </el-form-item>
            <el-form-item prop="family_name">
              <el-input v-model="createForm.family_name" placeholder="家庭名称" prefix-icon="House" size="large" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="loading" native-type="submit" size="large" style="width: 100%">注册</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="加入家庭" name="join">
          <el-form :model="joinForm" :rules="rules" ref="joinFormRef" @submit.prevent="handleJoin">
            <el-form-item prop="username">
              <el-input v-model="joinForm.username" placeholder="用户名" prefix-icon="User" size="large" />
            </el-form-item>
            <el-form-item prop="email">
              <el-input v-model="joinForm.email" placeholder="邮箱" prefix-icon="Message" size="large" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="joinForm.password" type="password" placeholder="密码" prefix-icon="Lock" size="large" show-password />
            </el-form-item>
            <el-form-item prop="invite_code">
              <el-input v-model="joinForm.invite_code" placeholder="家庭邀请码" prefix-icon="Key" size="large" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="loading" native-type="submit" size="large" style="width: 100%">加入</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      <div class="links">
        已有账户？<router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const tab = ref('create')
const createFormRef = ref<FormInstance>()
const joinFormRef = ref<FormInstance>()
const loading = ref(false)

const createForm = reactive({ username: '', email: '', password: '', family_name: '我的家庭' })
const joinForm = reactive({ username: '', email: '', password: '', invite_code: '' })

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email' as const, message: '请输入有效的邮箱', trigger: 'blur' },
  ],
  password: [{ required: true, min: 6, message: '密码至少6位', trigger: 'blur' }],
  family_name: [{ required: true, message: '请输入家庭名称', trigger: 'blur' }],
  invite_code: [{ required: true, message: '请输入邀请码', trigger: 'blur' }],
}

async function handleCreate() {
  await createFormRef.value?.validate()
  loading.value = true
  try {
    await auth.register(createForm)
    ElMessage.success('注册成功')
    router.push('/')
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '注册失败')
  } finally {
    loading.value = false
  }
}

async function handleJoin() {
  await joinFormRef.value?.validate()
  loading.value = true
  try {
    await auth.registerJoin(joinForm)
    ElMessage.success('加入成功')
    router.push('/')
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '加入失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}
.login-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}
.title {
  text-align: center;
  font-size: 24px;
  color: #303133;
  margin-bottom: 16px;
}
.links {
  text-align: center;
  color: #909399;
  font-size: 14px;
  margin-top: 16px;
}
.links a {
  color: #409eff;
  text-decoration: none;
}
</style>
