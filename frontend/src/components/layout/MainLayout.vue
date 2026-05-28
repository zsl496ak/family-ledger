<template>
  <div class="main-layout" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
    <AppHeader @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed" />
    <div class="layout-body">
      <AppSidebar :collapsed="sidebarCollapsed" />
      <main class="main-content">
        <router-view />
      </main>
    </div>
    <MobileNav />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'
import MobileNav from './MobileNav.vue'

const sidebarCollapsed = ref(false)
</script>

<style scoped>
.main-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.layout-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f5f7fa;
}
@media (max-width: 768px) {
  .main-content {
    padding: 12px;
    padding-bottom: 70px;
  }
}
</style>
