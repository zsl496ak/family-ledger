<template>
  <nav class="mobile-nav">
    <router-link to="/" class="nav-item" :class="{ active: route.path === '/' }">
      <el-icon><DataAnalysis /></el-icon>
      <span>首页</span>
    </router-link>
    <router-link to="/transactions" class="nav-item" :class="{ active: route.path === '/transactions' }">
      <el-icon><List /></el-icon>
      <span>账单</span>
    </router-link>
    <router-link to="/accounts" class="nav-item" :class="{ active: route.path === '/accounts' }">
      <el-icon><Wallet /></el-icon>
      <span>账户</span>
    </router-link>
    <router-link to="/reports" class="nav-item" :class="{ active: route.path === '/reports' }">
      <el-icon><TrendCharts /></el-icon>
      <span>报表</span>
    </router-link>
    <router-link to="/settings" class="nav-item" :class="{ active: route.path === '/settings' }">
      <el-icon><Setting /></el-icon>
      <span>更多</span>
    </router-link>
  </nav>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { DataAnalysis, List, Wallet, TrendCharts, Setting } from '@element-plus/icons-vue'

const route = useRoute()
</script>

<style scoped>
.mobile-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 56px;
  background: white;
  border-top: 1px solid #e4e7ed;
  z-index: 100;
  justify-content: space-around;
  align-items: center;
}
.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  color: #909399;
  text-decoration: none;
  font-size: 11px;
  padding: 4px 0;
}
.nav-item .el-icon {
  font-size: 20px;
}
.nav-item.active {
  color: #409eff;
}
@media (max-width: 768px) {
  .mobile-nav {
    display: flex;
  }
}
</style>
