<template>
  <div class="accounts-page">
    <el-card shadow="hover">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <h2 style="margin:0">账户管理</h2>
          <el-button type="primary" :icon="Plus" @click="openForm()">新增账户</el-button>
        </div>
      </template>

      <el-row :gutter="16">
        <el-col :xs="12" :sm="8" :md="6" v-for="acc in accountStore.accounts" :key="acc.id">
          <el-card shadow="hover" class="account-card" :body-style="{ padding: '20px' }">
            <div class="account-icon" :style="{ background: acc.color || '#409EFF' }">
              <el-icon :size="24"><Wallet /></el-icon>
            </div>
            <div class="account-info">
              <div class="account-name">{{ acc.name }}</div>
              <div class="account-type">{{ typeMap[acc.account_type] }}</div>
              <div class="account-balance" :style="{ color: (acc.balance || 0) >= 0 ? '#303133' : '#F56C6C' }">
                ¥{{ (acc.balance || 0).toFixed(2) }}
              </div>
            </div>
            <div class="account-actions">
              <el-button text type="primary" size="small" @click="openForm(acc)">编辑</el-button>
              <el-popconfirm title="确定删除?" @confirm="handleDelete(acc.id)">
                <template #reference>
                  <el-button text type="danger" size="small">删除</el-button>
                </template>
              </el-popconfirm>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>

    <el-dialog v-model="showForm" :title="editingAccount ? '编辑账户' : '新增账户'" width="440px" destroy-on-close>
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称" required>
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="类型" required>
          <el-select v-model="form.account_type" style="width: 100%">
            <el-option label="现金" value="cash" />
            <el-option label="银行卡" value="bank_card" />
            <el-option label="信用卡" value="credit_card" />
            <el-option label="电子钱包" value="e_wallet" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="初始余额">
          <el-input-number v-model="form.initial_balance" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="颜色">
          <el-color-picker v-model="form.color" />
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
import { ref, reactive, onMounted } from 'vue'
import { Plus, Wallet } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useAccountStore } from '@/stores/account'

const accountStore = useAccountStore()
const showForm = ref(false)
const editingAccount = ref<any>(null)
const saving = ref(false)

const typeMap: Record<string, string> = { cash: '现金', bank_card: '银行卡', credit_card: '信用卡', e_wallet: '电子钱包', other: '其他' }

const form = reactive({
  name: '',
  account_type: 'cash',
  initial_balance: 0,
  color: '#409EFF',
})

function openForm(acc?: any) {
  if (acc) {
    editingAccount.value = acc
    Object.assign(form, { name: acc.name, account_type: acc.account_type, initial_balance: acc.initial_balance, color: acc.color || '#409EFF' })
  } else {
    editingAccount.value = null
    Object.assign(form, { name: '', account_type: 'cash', initial_balance: 0, color: '#409EFF' })
  }
  showForm.value = true
}

async function handleSave() {
  saving.value = true
  try {
    if (editingAccount.value) {
      await accountStore.updateAccount(editingAccount.value.id, form)
    } else {
      await accountStore.createAccount(form)
    }
    ElMessage.success('保存成功')
    showForm.value = false
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

async function handleDelete(id: number) {
  await accountStore.deleteAccount(id)
  ElMessage.success('删除成功')
}

onMounted(() => accountStore.fetchAccounts())
</script>

<style scoped>
.account-card {
  margin-bottom: 16px;
  text-align: center;
}
.account-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 12px;
}
.account-name { font-weight: 600; font-size: 15px; }
.account-type { color: #909399; font-size: 12px; margin: 4px 0; }
.account-balance { font-size: 20px; font-weight: 700; margin-top: 8px; }
.account-actions { margin-top: 12px; }
</style>
