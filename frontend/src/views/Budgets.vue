<template>
  <div class="budgets-page">
    <el-card shadow="hover">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
          <h2 style="margin:0">预算管理</h2>
          <div style="display:flex;gap:8px;align-items:center">
            <el-date-picker v-model="monthPicker" type="month" value-format="YYYY-MM" placeholder="选择月份" @change="loadData" />
            <el-button type="primary" :icon="Plus" @click="openForm()">新增预算</el-button>
          </div>
        </div>
      </template>

      <div v-if="overview" class="budget-overview">
        <el-row :gutter="16">
          <el-col :span="8">
            <div class="overview-item">
              <div class="overview-label">总预算</div>
              <div class="overview-value">¥{{ overview.total_budget?.toFixed(2) }}</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="overview-item">
              <div class="overview-label">已支出</div>
              <div class="overview-value" style="color: #F56C6C">¥{{ overview.total_spent?.toFixed(2) }}</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="overview-item">
              <div class="overview-label">剩余</div>
              <div class="overview-value" :style="{ color: (overview.total_remaining || 0) >= 0 ? '#67C23A' : '#F56C6C' }">¥{{ overview.total_remaining?.toFixed(2) }}</div>
            </div>
          </el-col>
        </el-row>
      </div>

      <div v-for="budget in budgets" :key="budget.id" class="budget-item">
        <div class="budget-header">
          <span class="budget-category">{{ budget.category_name }}</span>
          <div class="budget-amounts">
            <span>¥{{ budget.spent?.toFixed(2) }} / ¥{{ budget.amount?.toFixed(2) }}</span>
            <el-button text type="primary" size="small" @click="openForm(budget)">编辑</el-button>
            <el-popconfirm title="确定删除?" @confirm="handleDelete(budget.id)">
              <template #reference>
                <el-button text type="danger" size="small">删除</el-button>
              </template>
            </el-popconfirm>
          </div>
        </div>
        <el-progress :percentage="Math.min(budget.percentage || 0, 100)" :color="budget.percentage > 80 ? '#F56C6C' : budget.percentage > 50 ? '#E6A23C' : '#67C23A'" :stroke-width="12" />
      </div>

      <el-empty v-if="budgets.length === 0" description="暂无预算，点击新增" />
    </el-card>

    <el-dialog v-model="showForm" :title="editingBudget ? '编辑预算' : '新增预算'" width="440px" destroy-on-close>
      <el-form :model="form" label-width="80px">
        <el-form-item label="分类" required>
          <el-select v-model="form.category_id" placeholder="选择分类" style="width: 100%">
            <el-option v-for="cat in expenseCategories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="预算金额" required>
          <el-input-number v-model="form.amount" :min="1" :precision="2" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showForm = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { budgetApi } from '@/api/budgets'
import { useCategoryStore } from '@/stores/category'

const categoryStore = useCategoryStore()
const budgets = ref<any[]>([])
const overview = ref<any>(null)
const showForm = ref(false)
const editingBudget = ref<any>(null)
const saving = ref(false)
const monthPicker = ref(new Date().toISOString().slice(0, 7))

const form = reactive({ category_id: null as number | null, amount: null as number | null })

const expenseCategories = computed(() => categoryStore.categories.filter(c => c.category_type === 'expense'))

const [year, month] = computed(() => {
  const parts = monthPicker.value.split('-')
  return [parseInt(parts[0]), parseInt(parts[1])]
}).value

async function loadData() {
  if (!monthPicker.value) return
  const [y, m] = monthPicker.value.split('-').map(Number)
  const [b, o] = await Promise.all([
    budgetApi.list(y, m),
    budgetApi.overview(y, m),
  ])
  budgets.value = b.data
  overview.value = o.data
}

function openForm(budget?: any) {
  if (budget) {
    editingBudget.value = budget
    Object.assign(form, { category_id: budget.category_id, amount: budget.amount })
  } else {
    editingBudget.value = null
    Object.assign(form, { category_id: null, amount: null })
  }
  showForm.value = true
}

async function handleSave() {
  saving.value = true
  try {
    const [y, m] = monthPicker.value.split('-').map(Number)
    if (editingBudget.value) {
      await budgetApi.update(editingBudget.value.id, { amount: form.amount })
    } else {
      await budgetApi.create({ category_id: form.category_id, year: y, month: m, amount: form.amount })
    }
    ElMessage.success('保存成功')
    showForm.value = false
    loadData()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

async function handleDelete(id: number) {
  await budgetApi.delete(id)
  loadData()
}

onMounted(() => {
  categoryStore.fetchCategories()
  loadData()
})
</script>

<style scoped>
.budget-overview {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}
.overview-item { text-align: center; }
.overview-label { color: #909399; font-size: 13px; margin-bottom: 8px; }
.overview-value { font-size: 22px; font-weight: 600; color: #303133; }
.budget-item {
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}
.budget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.budget-category { font-weight: 500; }
.budget-amounts {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
  font-size: 13px;
}
@media (max-width: 768px) {
  .overview-value { font-size: 18px; }
}
</style>
