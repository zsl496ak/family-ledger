<template>
  <div class="dashboard">
    <div class="stat-cards">
      <el-row :gutter="16">
        <el-col :xs="12" :sm="6">
          <el-card shadow="hover" class="stat-card income">
            <div class="stat-label">本月收入</div>
            <div class="stat-value">{{ formatMoney(monthly.total_income) }}</div>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="6">
          <el-card shadow="hover" class="stat-card expense">
            <div class="stat-label">本月支出</div>
            <div class="stat-value">{{ formatMoney(monthly.total_expense) }}</div>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="6">
          <el-card shadow="hover" class="stat-card net">
            <div class="stat-label">本月结余</div>
            <div class="stat-value">{{ formatMoney(monthly.net_amount) }}</div>
          </el-card>
        </el-col>
        <el-col :xs="12" :sm="6">
          <el-card shadow="hover" class="stat-card count">
            <div class="stat-label">交易笔数</div>
            <div class="stat-value">{{ monthly.transaction_count }}</div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :xs="24" :lg="14">
        <el-card shadow="hover">
          <template #header>
            <span>收支趋势</span>
          </template>
          <v-chart :option="trendOption" style="height: 300px" autoresize />
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="10" style="margin-top: 16px">
        <el-card shadow="hover">
          <template #header>
            <span>支出分类</span>
          </template>
          <v-chart :option="pieOption" style="height: 300px" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-top: 16px">
      <el-col :span="24">
        <el-card shadow="hover">
          <template #header>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span>最近交易</span>
              <el-button text type="primary" @click="$router.push('/transactions')">查看全部</el-button>
            </div>
          </template>
          <el-table :data="recentTransactions" stripe style="width: 100%">
            <el-table-column prop="transaction_date" label="日期" width="110" />
            <el-table-column label="类型" width="70">
              <template #default="{ row }">
                <el-tag :type="row.transaction_type === 'income' ? 'success' : row.transaction_type === 'expense' ? 'danger' : 'warning'" size="small">
                  {{ typeMap[row.transaction_type] }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="category_name" label="分类" width="90" />
            <el-table-column label="金额">
              <template #default="{ row }">
                <span :style="{ color: row.transaction_type === 'income' ? '#67C23A' : '#F56C6C' }">
                  {{ row.transaction_type === 'income' ? '+' : '-' }}{{ row.amount }}
                </span>
              </template>
            </el-table-column>
            <el-table-column prop="note" label="备注" show-overflow-tooltip />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-button class="fab" type="primary" :icon="Plus" circle size="large" @click="showAddDialog = true" />

    <TransactionForm v-model:visible="showAddDialog" @saved="loadData" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart, BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { reportApi } from '@/api/reports'
import { transactionApi } from '@/api/transactions'
import TransactionForm from '@/components/transaction/TransactionForm.vue'

use([CanvasRenderer, LineChart, PieChart, BarChart, GridComponent, TooltipComponent, LegendComponent])

const now = new Date()
const year = now.getFullYear()
const month = now.getMonth() + 1

const monthly = ref<any>({ total_income: 0, total_expense: 0, net_amount: 0, transaction_count: 0 })
const trendData = ref<any[]>([])
const pieData = ref<any[]>([])
const recentTransactions = ref<any[]>([])
const showAddDialog = ref(false)

const typeMap: Record<string, string> = { income: '收入', expense: '支出', transfer: '转账' }

function formatMoney(v: number) {
  return '¥' + (v || 0).toFixed(2)
}

const trendOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { data: ['收入', '支出'] },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: { type: 'category', data: trendData.value.map(d => d.month) },
  yAxis: { type: 'value' },
  series: [
    { name: '收入', type: 'bar', data: trendData.value.map(d => d.income), itemStyle: { color: '#67C23A' } },
    { name: '支出', type: 'bar', data: trendData.value.map(d => d.expense), itemStyle: { color: '#F56C6C' } },
  ],
}))

const pieOption = computed(() => ({
  tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
  series: [{
    type: 'pie', radius: ['40%', '70%'],
    data: pieData.value.map(d => ({ name: d.category_name, value: d.amount, itemStyle: { color: d.color } })),
    emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.5)' } },
  }],
}))

async function loadData() {
  const [m, t, p, r] = await Promise.all([
    reportApi.monthly(year, month),
    reportApi.trend(year),
    reportApi.categoryBreakdown(year, month, 'expense'),
    transactionApi.list({ page: 1, page_size: 10 }),
  ])
  monthly.value = m.data
  trendData.value = t.data
  pieData.value = p.data
  recentTransactions.value = r.data.items
}

onMounted(loadData)
</script>

<style scoped>
.stat-card {
  text-align: center;
  padding: 8px 0;
  margin-bottom: 16px;
}
.stat-label {
  color: #909399;
  font-size: 13px;
  margin-bottom: 8px;
}
.stat-value {
  font-size: 22px;
  font-weight: 600;
}
.stat-card.income .stat-value { color: #67C23A; }
.stat-card.expense .stat-value { color: #F56C6C; }
.stat-card.net .stat-value { color: #409EFF; }
.stat-card.count .stat-value { color: #E6A23C; }

.fab {
  position: fixed;
  right: 24px;
  bottom: 24px;
  width: 56px;
  height: 56px;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
  z-index: 99;
}
@media (max-width: 768px) {
  .fab { bottom: 72px; right: 16px; }
  .stat-value { font-size: 18px; }
}
</style>
