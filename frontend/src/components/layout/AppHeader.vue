<template>
  <header class="app-header">
    <div class="header-left">
      <el-button class="menu-btn" :icon="Fold" @click="$emit('toggle-sidebar')" text />
      <h1 class="app-title">家庭记账</h1>
    </div>
    <div class="header-right">
      <span class="user-name">{{ auth.user?.username }}</span>
      <el-dropdown @command="handleCommand">
        <el-avatar :size="32" class="user-avatar">
          {{ auth.user?.username?.charAt(0) }}
        </el-avatar>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="settings">设置</el-dropdown-item>
            <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Fold } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

defineEmits(['toggle-sidebar'])

const router = useRouter()
const auth = useAuthStore()

function handleCommand(cmd: string) {
  if (cmd === 'logout') {
    auth.logout()
    router.push('/login')
  } else if (cmd === 'settings') {
    router.push('/settings')
  }
}
</script>

<style scoped>
.app-header {
  height: 56px;
  background: white;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  flex-shrink: 0;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}
.menu-btn {
  display: none;
}
.app-title {
  font-size: 18px;
  color: #303133;
  font-weight: 600;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.user-name {
  color: #606266;
  font-size: 14px;
}
.user-avatar {
  cursor: pointer;
  background: #409eff;
  color: white;
}
@media (max-width: 768px) {
  .menu-btn { display: inline-flex; }
  .app-title { font-size: 16px; }
  .user-name { display: none; }
}
</style>
