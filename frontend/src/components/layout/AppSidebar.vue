<template>
  <aside class="app-sidebar" :class="{ collapsed }">
    <el-menu :default-active="route.path" router :collapse="collapsed">
      <el-menu-item index="/">
        <el-icon><DataAnalysis /></el-icon>
        <span>仪表盘</span>
      </el-menu-item>
      <el-menu-item index="/transactions">
        <el-icon><List /></el-icon>
        <span>交易记录</span>
      </el-menu-item>
      <el-menu-item index="/accounts">
        <el-icon><Wallet /></el-icon>
        <span>账户管理</span>
      </el-menu-item>
      <el-menu-item index="/budgets">
        <el-icon><PieChart /></el-icon>
        <span>预算管理</span>
      </el-menu-item>
      <el-menu-item index="/reports">
        <el-icon><TrendCharts /></el-icon>
        <span>统计报表</span>
      </el-menu-item>
      <el-menu-item index="/settings">
        <el-icon><Setting /></el-icon>
        <span>设置</span>
      </el-menu-item>
    </el-menu>
  </aside>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { DataAnalysis, List, Wallet, PieChart, TrendCharts, Setting } from '@element-plus/icons-vue'

defineProps<{ collapsed: boolean }>()
const route = useRoute()
</script>

<style scoped>
.app-sidebar {
  width: 200px;
  background: white;
  border-right: 1px solid #e4e7ed;
  overflow-y: auto;
  transition: width 0.3s;
  flex-shrink: 0;
}
.app-sidebar.collapsed {
  width: 64px;
}
.el-menu {
  border-right: none;
}
@media (max-width: 768px) {
  .app-sidebar {
    display: none;
  }
}
</style>
