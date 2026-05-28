<template>
  <div class="transactions-page">
    <el-card shadow="hover">
      <template #header>
        <div class="page-header">
          <h2>交易记录</h2>
          <div class="header-actions">
            <el-button type="primary" :icon="Plus" @click="openForm()">新增</el-button>
            <el-button :icon="Download" @click="handleExport">导出</el-button>
            <el-button :icon="Upload" @click="showImport = true">导入</el-button>
            <el-button text @click="downloadTemplate">下载导入模板</el-button>
          </div>
        </div>
      </template>

      <div class="filters">
        <el-date-picker v-model="filters.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" value-format="YYYY-MM-DD" size="default" style="max-width: 280px" />
        <el-select v-model="filters.type" placeholder="类型" clearable style="width: 100px">
          <el-option label="收入" value="income" />
          <el-option label="支出" value="expense" />
          <el-option label="转账" value="transfer" />
        </el-select>
        <el-select v-model="filters.account_id" placeholder="账户" clearable style="width: 140px">
          <el-option v-for="acc in accountStore.accounts" :key="acc.id" :label="acc.name" :value="acc.id" />
        </el-select>
        <el-input v-model="filters.search" placeholder="搜索备注" clearable style="width: 180px" />
        <el-button type="primary" @click="loadData">查询</el-button>
      </div>

      <el-table :data="store.transactions" stripe v-loading="store.loading" style="width: 100%">
        <el-table-column prop="transaction_date" label="日期" width="110" />
        <el-table-column label="类型" width="70">
          <template #default="{ row }">
            <el-tag :type="row.transaction_type === 'income' ? 'success' : row.transaction_type === 'expense' ? 'danger' : 'warning'" size="small">
              {{ typeMap[row.transaction_type] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="category_name" label="分类" width="90" />
        <el-table-column prop="account_name" label="账户" width="100" />
        <el-table-column label="金额">
          <template #default="{ row }">
            <span :style="{ color: row.transaction_type === 'income' ? '#67C23A' : '#F56C6C', fontWeight: 600 }">
              {{ row.transaction_type === 'income' ? '+' : '-' }}{{ row.amount }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="note" label="备注" show-overflow-tooltip />
        <el-table-column prop="creator_name" label="记账人" width="80" />
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button text type="primary" size="small" @click="openForm(row)">编辑</el-button>
            <el-popconfirm title="确定删除?" @confirm="handleDelete(row.id)">
              <template #reference>
                <el-button text type="danger" size="small">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination v-if="store.total > 0" :current-page="page" :page-size="pageSize" :total="store.total" layout="total, prev, pager, next" @current-change="onPageChange" style="margin-top: 16px; justify-content: center" />
    </el-card>

    <TransactionForm v-model:visible="showForm" :transaction="editingTransaction" @saved="loadData" />

    <el-dialog v-model="showImport" title="导入交易" width="500px">
      <el-upload drag :auto-upload="false" :limit="1" accept=".xlsx,.csv" :on-change="onFileChange">
        <el-icon style="font-size: 48px; color: #c0c4cc"><Upload /></el-icon>
        <div>将文件拖到此处，或点击上传</div>
        <template #tip>
          <div class="el-upload__tip">支持 .xlsx / .csv 文件</div>
        </template>
      </el-upload>
      <div v-if="importResult" style="margin-top: 16px">
        <el-result :icon="importResult.errors.length > 0 ? 'warning' : 'success'" :title="`导入完成`">
          <template #sub-title>
            <p>成功: {{ importResult.success }} 条 | 重复跳过: {{ importResult.skipped }} 条 | 失败: {{ importResult.errors.length }} 条</p>
            <div v-if="importResult.errors.length > 0" style="text-align: left; max-height: 200px; overflow-y: auto">
              <p v-for="(err, i) in importResult.errors" :key="i" style="color: #F56C6C; font-size: 12px">
                第{{ err.row }}行: {{ err.error }}
              </p>
            </div>
          </template>
        </el-result>
      </div>
      <template #footer>
        <el-button @click="showImport = false">关闭</el-button>
        <el-button type="primary" :loading="importing" :disabled="!importFile" @click="handleImport">开始导入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Plus, Download, Upload } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useTransactionStore } from '@/stores/transaction'
import { useAccountStore } from '@/stores/account'
import { transactionApi } from '@/api/transactions'
import TransactionForm from '@/components/transaction/TransactionForm.vue'

const store = useTransactionStore()
const accountStore = useAccountStore()
const typeMap: Record<string, string> = { income: '收入', expense: '支出', transfer: '转账' }

const page = ref(1)
const pageSize = ref(20)
const showForm = ref(false)
const editingTransaction = ref<any>(null)
const showImport = ref(false)
const importFile = ref<File | null>(null)
const importing = ref(false)
const importResult = ref<any>(null)

const filters = reactive({
  dateRange: null as any,
  type: '',
  account_id: null as number | null,
  search: '',
})

function loadData() {
  const params: any = { page: page.value, page_size: pageSize.value }
  if (filters.dateRange?.length === 2) {
    params.date_from = filters.dateRange[0]
    params.date_to = filters.dateRange[1]
  }
  if (filters.type) params.transaction_type = filters.type
  if (filters.account_id) params.account_id = filters.account_id
  if (filters.search) params.search = filters.search
  store.fetchTransactions(params)
}

function onPageChange(p: number) {
  page.value = p
  loadData()
}

function openForm(txn?: any) {
  editingTransaction.value = txn || null
  showForm.value = true
}

async function handleDelete(id: number) {
  await store.deleteTransaction(id)
  loadData()
}

async function handleExport() {
  const params: any = { format: 'xlsx' }
  if (filters.dateRange?.length === 2) {
    params.date_from = filters.dateRange[0]
    params.date_to = filters.dateRange[1]
  }
  if (filters.type) params.transaction_type = filters.type
  const res = await transactionApi.export(params)
  const url = URL.createObjectURL(new Blob([res.data]))
  const a = document.createElement('a')
  a.href = url
  a.download = 'transactions.xlsx'
  a.click()
  URL.revokeObjectURL(url)
}

function onFileChange(file: any) {
  importFile.value = file.raw
  importResult.value = null
}

async function handleImport() {
  if (!importFile.value) return
  importing.value = true
  try {
    const { data } = await transactionApi.import(importFile.value)
    importResult.value = data
    loadData()
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '导入失败')
  } finally {
    importing.value = false
  }
}

async function downloadTemplate() {
  const res = await transactionApi.downloadTemplate()
  const url = URL.createObjectURL(new Blob([res.data]))
  const a = document.createElement('a')
  a.href = url
  a.download = 'import_template.xlsx'
  a.click()
  URL.revokeObjectURL(url)
}

onMounted(() => {
  loadData()
  accountStore.fetchAccounts()
})
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}
.page-header h2 { font-size: 18px; margin: 0; }
.header-actions { display: flex; gap: 8px; flex-wrap: wrap; }
.filters {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
@media (max-width: 768px) {
  .header-actions .el-button:not(.el-button--primary) { display: none; }
  .filters { gap: 6px; }
  .filters .el-date-picker { width: 100%; max-width: 100%; }
}
</style>
