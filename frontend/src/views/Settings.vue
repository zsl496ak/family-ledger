<template>
  <div class="settings-page">
    <el-row :gutter="16">
      <el-col :xs="24" :md="12">
        <el-card shadow="hover" style="margin-bottom: 16px">
          <template #header><span>家庭信息</span></template>
          <el-form label-width="80px">
            <el-form-item label="家庭名称">
              <el-input v-model="familyForm.name" />
            </el-form-item>
            <el-form-item label="邀请码">
              <div style="display:flex;gap:8px;align-items:center">
                <el-input :model-value="family.invite_code" readonly style="flex:1" />
                <el-button @click="copyInvite" text type="primary">复制</el-button>
                <el-button @click="regenerateInvite" text type="warning">重新生成</el-button>
              </div>
              <div style="color:#909399;font-size:12px;margin-top:4px">分享邀请码给家庭成员，即可加入</div>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveFamily">保存</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card shadow="hover" style="margin-bottom: 16px">
          <template #header>
            <div style="display:flex;justify-content:space-between;align-items:center">
              <span>分类管理</span>
              <el-button type="primary" size="small" :icon="Plus" @click="openCategoryForm()">新增</el-button>
            </div>
          </template>
          <el-tabs v-model="catTab">
            <el-tab-pane label="支出分类" name="expense">
              <div v-for="cat in expenseCategories" :key="cat.id" class="category-item">
                <el-icon :style="{ color: cat.color }" style="font-size:18px"><component :is="cat.icon || 'Menu'" /></el-icon>
                <span>{{ cat.name }}</span>
                <div class="category-actions">
                  <el-button text type="primary" size="small" @click="openCategoryForm(cat)">编辑</el-button>
                  <el-popconfirm title="确定删除?" @confirm="deleteCategory(cat.id)">
                    <template #reference><el-button text type="danger" size="small">删除</el-button></template>
                  </el-popconfirm>
                </div>
              </div>
            </el-tab-pane>
            <el-tab-pane label="收入分类" name="income">
              <div v-for="cat in incomeCategories" :key="cat.id" class="category-item">
                <el-icon :style="{ color: cat.color }" style="font-size:18px"><component :is="cat.icon || 'Menu'" /></el-icon>
                <span>{{ cat.name }}</span>
                <div class="category-actions">
                  <el-button text type="primary" size="small" @click="openCategoryForm(cat)">编辑</el-button>
                  <el-popconfirm title="确定删除?" @confirm="deleteCategory(cat.id)">
                    <template #reference><el-button text type="danger" size="small">删除</el-button></template>
                  </el-popconfirm>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="12">
        <el-card shadow="hover" style="margin-bottom: 16px">
          <template #header><span>家庭成员</span></template>
          <div v-for="member in members" :key="member.id" class="member-item">
            <el-avatar :size="36" style="background:#409eff;color:white">{{ member.username?.charAt(0) }}</el-avatar>
            <div class="member-info">
              <div class="member-name">{{ member.username }}</div>
              <div class="member-email">{{ member.email }}</div>
            </div>
            <el-tag :type="member.role === 'admin' ? 'danger' : 'info'" size="small">{{ member.role === 'admin' ? '管理员' : '成员' }}</el-tag>
            <el-dropdown v-if="auth.user?.role === 'admin' && member.id !== auth.user.id" @command="(cmd: string) => handleMemberCmd(cmd, member.id)">
              <el-button text size="small">更多</el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item :command="member.role === 'admin' ? 'member' : 'admin'">
                    {{ member.role === 'admin' ? '设为成员' : '设为管理员' }}
                  </el-dropdown-item>
                  <el-dropdown-item command="remove" style="color:#F56C6C">移除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-card>

        <el-card shadow="hover" style="margin-bottom: 16px">
          <template #header><span>个人设置</span></template>
          <el-form label-width="80px">
            <el-form-item label="用户名">
              <el-input v-model="profileForm.username" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveProfile">保存</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card shadow="hover">
          <template #header><span>修改密码</span></template>
          <el-form label-width="80px">
            <el-form-item label="原密码">
              <el-input v-model="passwordForm.old_password" type="password" show-password />
            </el-form-item>
            <el-form-item label="新密码">
              <el-input v-model="passwordForm.new_password" type="password" show-password />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="changePassword">修改密码</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="showCatForm" :title="editingCategory ? '编辑分类' : '新增分类'" width="400px" destroy-on-close>
      <el-form :model="catForm" label-width="60px">
        <el-form-item label="名称">
          <el-input v-model="catForm.name" />
        </el-form-item>
        <el-form-item label="类型">
          <el-radio-group v-model="catForm.category_type">
            <el-radio value="expense">支出</el-radio>
            <el-radio value="income">收入</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="颜色">
          <el-color-picker v-model="catForm.color" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCatForm = false">取消</el-button>
        <el-button type="primary" @click="saveCategory">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { useCategoryStore } from '@/stores/category'
import { familyApi } from '@/api/family'
import { authApi } from '@/api/auth'

const auth = useAuthStore()
const categoryStore = useCategoryStore()
const family = ref<any>({})
const members = ref<any[]>([])
const catTab = ref('expense')
const showCatForm = ref(false)
const editingCategory = ref<any>(null)

const familyForm = reactive({ name: '' })
const profileForm = reactive({ username: '' })
const passwordForm = reactive({ old_password: '', new_password: '' })
const catForm = reactive({ name: '', category_type: 'expense', color: '#409EFF' })

const expenseCategories = computed(() => categoryStore.categories.filter(c => c.category_type === 'expense'))
const incomeCategories = computed(() => categoryStore.categories.filter(c => c.category_type === 'income'))

async function loadFamily() {
  const { data } = await familyApi.get()
  family.value = data
  familyForm.name = data.name
}

async function loadMembers() {
  const { data } = await familyApi.members()
  members.value = data
}

async function saveFamily() {
  await familyApi.update({ name: familyForm.name })
  ElMessage.success('保存成功')
  loadFamily()
}

function copyInvite() {
  navigator.clipboard.writeText(family.value.invite_code)
  ElMessage.success('已复制邀请码')
}

async function regenerateInvite() {
  const { data } = await familyApi.regenerateInvite()
  family.value.invite_code = data.invite_code
  ElMessage.success('已重新生成')
}

function openCategoryForm(cat?: any) {
  if (cat) {
    editingCategory.value = cat
    Object.assign(catForm, { name: cat.name, category_type: cat.category_type, color: cat.color || '#409EFF' })
  } else {
    editingCategory.value = null
    Object.assign(catForm, { name: '', category_type: catTab.value, color: '#409EFF' })
  }
  showCatForm.value = true
}

async function saveCategory() {
  if (editingCategory.value) {
    await categoryStore.updateCategory(editingCategory.value.id, catForm)
  } else {
    await categoryStore.createCategory(catForm)
  }
  ElMessage.success('保存成功')
  showCatForm.value = false
}

async function deleteCategory(id: number) {
  await categoryStore.deleteCategory(id)
  ElMessage.success('删除成功')
}

async function saveProfile() {
  await authApi.updateMe({ username: profileForm.username })
  auth.fetchUser()
  ElMessage.success('保存成功')
}

async function changePassword() {
  try {
    await authApi.changePassword(passwordForm)
    ElMessage.success('密码修改成功')
    passwordForm.old_password = ''
    passwordForm.new_password = ''
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '修改失败')
  }
}

async function handleMemberCmd(cmd: string, userId: number) {
  if (cmd === 'remove') {
    await familyApi.removeMember(userId)
    ElMessage.success('已移除')
  } else {
    await familyApi.updateRole(userId, cmd)
    ElMessage.success('已更新')
  }
  loadMembers()
}

onMounted(() => {
  loadFamily()
  loadMembers()
  categoryStore.fetchCategories()
  if (auth.user) {
    profileForm.username = auth.user.username
  }
})
</script>

<style scoped>
.category-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}
.category-actions { margin-left: auto; }
.member-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}
.member-info { flex: 1; }
.member-name { font-weight: 500; }
.member-email { color: #909399; font-size: 12px; }
</style>
