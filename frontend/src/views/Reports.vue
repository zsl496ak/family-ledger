<template>
  <div class="reports-page">
    <el-card shadow="hover">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
          <h2 style="margin:0">统计报表</h2>
          <el-date-picker v-model="monthPicker" type="month" value-format="YYYY-MM" placeholder="选择月份" @change="loadData" />
        </div>
      </template>

      <el-row :gutter="16">
        <el-col :xs="12" :sm="6" v-for="(item, key) in summaryCards" :key="key">
          <div class="summary-card" :style="{ borderLeft: `4px solid ${item.color}` }">
            <div class="summary-label">{{ item.label }}</div>
            <div class="summary-value" :style="{ color: item.color }">{{ item.value }}</div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :xs="24" :lg="14">
        <el-card shadow="hover">
          <template #header><span>年度趋势</span></template>
          <v-chart :option="trendOption" style="height: 320px" autoresize />
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="10" style="margin-top: 16px">
        <el-card shadow="hover">
          <template #header><span>支出分类</span></template>
          <v-chart :option="pieOption" style="height: 320px" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="24">
        <el-card shadow="hover">
          <template #header><span>账户余额</span></template>
          <v-chart :option="barOption" style="height: 280px" autoresize />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart, BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { reportApi } from '@/api/reports'

use([CanvasRenderer, LineChart, PieChart, BarChart, GridComponent, TooltipComponent, LegendComponent])

const monthPicker = ref(new Date().toISOString().slice(0, 7))
const monthlyData = ref<any>({ total_income: 0, total_expense: 0, net_amount: 0, transaction_count: 0 })
const trendData = ref<any[]>([])
const categoryData = ref<any[]>([])
const accountData = ref<any[]>([])

const summaryCards = computed(() => ({
  income: { label: '收入', value: `¥${Number(monthlyData.value.total_income || 0).toFixed(2)}`, color: '#67C23A' },
  expense: { label: '支出', value: `¥${Number(monthlyData.value.total_expense || 0).toFixed(2)}`, color: '#F56C6C' },
  net: { label: '结余', value: `¥${Number(monthlyData.value.net_amount || 0).toFixed(2)}`, color: '#409EFF' },
  count: { label: '笔数', value: monthlyData.value.transaction_count || 0, color: '#E6A23C' },
}))

const trendOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { data: ['收入', '支出'] },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: { type: 'category', data: trendData.value.map(d => d.month) },
  yAxis: { type: 'value' },
  series: [
    { name: '收入', type: 'line', smooth: true, data: trendData.value.map(d => d.income), itemStyle: { color: '#67C23A' }, areaStyle: { opacity: 0.1 } },
    { name: '支出', type: 'line', smooth: true, data: trendData.value.map(d => d.expense), itemStyle: { color: '#F56C6C' }, areaStyle: { opacity: 0.1 } },
  ],
}))

const pieOption = computed(() => ({
  tooltip: { trigger: 'item', formatter: '{b}: ¥{c} ({d}%)' },
  legend: { orient: 'vertical', left: 'left', type: 'scroll' },
  series: [{
    type: 'pie', radius: ['35%', '65%'],
    center: ['55%', '50%'],
    data: categoryData.value.map(d => ({ name: d.category_name, value: d.amount, itemStyle: { color: d.color } })),
    emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.5)' } },
  }],
}))

const barOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: { type: 'category', data: accountData.value.map(d => d.account_name) },
  yAxis: { type: 'value' },
  series: [{
    type: 'bar', data: accountData.value.map(d => ({
      value: d.balance,
      itemStyle: { color: d.color || '#409EFF' },
    })),
    barMaxWidth: 50,
  }],
}))

async function loadData() {
  if (!monthPicker.value) return
  const [y, m] = monthPicker.value.split('-').map(Number)
  const [monthly, trend, cat, accounts] = await Promise.all([
    reportApi.monthly(y, m),
    reportApi.trend(y),
    reportApi.categoryBreakdown(y, m, 'expense'),
    reportApi.accountBalances(),
  ])
  monthlyData.value = monthly.data
  trendData.value = trend.data
  categoryData.value = cat.data
  accountData.value = accounts.data
}

onMounted(loadData)
</script>

<style scoped>
.summary-card {
  background: #f5f7fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}
.summary-label { color: #909399; font-size: 13px; margin-bottom: 4px; }
.summary-value { font-size: 20px; font-weight: 600; }
</style>
