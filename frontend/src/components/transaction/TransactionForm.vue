<template>
  <el-dialog :model-value="visible" @update:model-value="$emit('update:visible', $event)" :title="form.id ? '编辑交易' : '新增交易'" width="500px" destroy-on-close>
    <el-form :model="form" label-width="80px">
      <el-form-item label="类型" required>
        <el-radio-group v-model="form.transaction_type">
          <el-radio-button value="expense">支出</el-radio-button>
          <el-radio-button value="income">收入</el-radio-button>
          <el-radio-button value="transfer">转账</el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="金额" required>
        <el-input-number v-model="form.amount" :min="0.01" :precision="2" style="width: 100%" />
      </el-form-item>
      <el-form-item v-if="form.transaction_type !== 'transfer'" label="分类">
        <el-select v-model="form.category_id" placeholder="选择分类" clearable style="width: 100%">
          <el-option v-for="cat in filteredCategories" :key="cat.id" :label="cat.name" :value="cat.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="账户" required>
        <el-select v-model="form.account_id" placeholder="选择账户" style="width: 100%">
          <el-option v-for="acc in accountStore.accounts" :key="acc.id" :label="acc.name" :value="acc.id" />
        </el-select>
      </el-form-item>
      <el-form-item v-if="form.transaction_type === 'transfer'" label="转入账户" required>
        <el-select v-model="form.transfer_to_account_id" placeholder="选择转入账户" style="width: 100%">
          <el-option v-for="acc in accountStore.accounts" :key="acc.id" :label="acc.name" :value="acc.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="日期" required>
        <el-date-picker v-model="form.transaction_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="form.note" type="textarea" :rows="2" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="$emit('update:visible', false)">取消</el-button>
      <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useAccountStore } from '@/stores/account'
import { useCategoryStore } from '@/stores/category'
import { transactionApi } from '@/api/transactions'

const props = defineProps<{ visible: boolean; transaction?: any }>()
const emit = defineEmits(['update:visible', 'saved'])

const accountStore = useAccountStore()
const categoryStore = useCategoryStore()
const saving = ref(false)

const defaultForm = () => ({
  id: null as number | null,
  transaction_type: 'expense',
  amount: null as number | null,
  category_id: null as number | null,
  account_id: null as number | null,
  transfer_to_account_id: null as number | null,
  transaction_date: new Date().toISOString().split('T')[0],
  note: '',
})

const form = ref<any>(defaultForm())

watch(() => props.visible, (val) => {
  if (val) {
    accountStore.fetchAccounts()
    categoryStore.fetchCategories()
    if (props.transaction) {
      form.value = { ...props.transaction }
    } else {
      form.value = defaultForm()
    }
  }
})

const filteredCategories = computed(() => {
  const type = form.value.transaction_type === 'income' ? 'income' : 'expense'
  return categoryStore.categories.filter(c => c.category_type === type)
})

async function handleSave() {
  saving.value = true
  try {
    if (form.value.id) {
      await transactionApi.update(form.value.id, form.value)
    } else {
      await transactionApi.create(form.value)
    }
    ElMessage.success('保存成功')
    emit('update:visible', false)
    emit('saved')
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}
</script>
