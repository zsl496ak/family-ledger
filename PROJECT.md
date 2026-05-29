# Family Ledger - 家庭记账系统

> 最后更新：2026-05-29

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3.5 + TypeScript + Vite 6 + Element Plus 2.9 + ECharts 5 |
| 状态管理 | Pinia 2.3 (Composition API 风格) |
| HTTP 客户端 | Axios 1.7 |
| 后端 | Python 3.12 + FastAPI 0.115 + Pydantic 2.10 |
| ORM | SQLAlchemy 2.0 (Mapped/mapped_column 声明式) |
| 数据库 | SQLite (WAL 模式, 外键约束开启) |
| 认证 | JWT (python-jose) + bcrypt 密码哈希 |
| 部署 | Docker Compose (3 容器: backend + frontend + nginx) |

---

## 项目结构

```
family-ledger/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py                 # FastAPI 应用入口, 挂载所有路由, CORS, lifespan 建表
│       ├── config.py               # Pydantic Settings (DB URL, JWT 密钥等)
│       ├── database.py             # SQLAlchemy engine, SessionLocal, Base, SQLite PRAGMA
│       ├── models/                 # ORM 模型
│       │   ├── __init__.py         # 导出所有模型
│       │   ├── family.py           # Family (name, invite_code, currency)
│       │   ├── user.py             # User (family_id FK, username, email, hashed_password, role)
│       │   ├── account.py          # Account (family_id FK, name, type, icon, color, initial_balance, is_active)
│       │   ├── category.py         # Category (family_id FK, name, type, icon, color, parent_id 自引用)
│       │   ├── transaction.py      # Transaction (family_id, account_id, category_id, type, amount, date, creator_id, transfer_to_account_id)
│       │   └── budget.py           # Budget (family_id, category_id, year, month, amount, 唯一约束)
│       ├── schemas/                # Pydantic 请求/响应模型
│       │   ├── auth.py             # LoginRequest, RegisterRequest, TokenResponse, RefreshRequest
│       │   ├── user.py             # UserOut, UserUpdate, PasswordChange
│       │   ├── account.py          # AccountCreate, AccountUpdate, AccountOut (输出用 float)
│       │   ├── category.py         # CategoryCreate, CategoryUpdate, CategoryOut
│       │   ├── transaction.py      # TransactionCreate/Update/Out/Filter/Summary (输出用 float)
│       │   ├── budget.py           # BudgetCreate/Update/Out (输出用 float)
│       │   └── report.py           # MonthlySummary, CategoryBreakdown, TrendData, AccountBalance (全 float)
│       ├── services/               # 业务逻辑层
│       │   ├── auth_service.py     # 注册/登录/Token/默认分类创建/邀请码
│       │   ├── account_service.py  # 账户 CRUD + 余额计算 (sum transactions)
│       │   ├── category_service.py # 分类 CRUD (软删除)
│       │   ├── transaction_service.py # 交易 CRUD + 分页 + 汇总 + 关联名称填充
│       │   └── budget_service.py   # 预算 CRUD + upsert + 动态计算已支出/剩余/百分比
│       ├── routers/                # API 路由
│       │   ├── deps.py             # get_current_user 依赖 (JWT 解码 + 用户查询)
│       │   ├── auth.py             # /auth/* (注册/登录/刷新/用户信息/改密码)
│       │   ├── accounts.py         # /accounts/* (CRUD + 余额计算)
│       │   ├── categories.py       # /categories/* (CRUD + 软删除)
│       │   ├── transactions.py     # /transactions/* (CRUD + 分页 + 导入导出 + 汇总)
│       │   ├── budgets.py          # /budgets/* (CRUD + 概览聚合)
│       │   ├── reports.py          # /reports/* (月度/年度/分类/趋势/账户余额, 无 service 层)
│       │   └── family.py           # /family/* (家庭信息/邀请码/成员管理)
│       └── config.py               # Settings (DATABASE_URL, SECRET_KEY, TOKEN过期时间)
├── frontend/
│   ├── Dockerfile                  # 多阶段构建: node build → nginx 静态服务
│   ├── nginx.conf                  # SPA fallback + /api/ 反代
│   ├── vite.config.ts              # Vite 配置 + /api 代理到 localhost:8000
│   ├── package.json
│   └── src/
│       ├── main.ts                 # Vue 入口 (Pinia + Router + Element Plus + 全局图标注册)
│       ├── App.vue                 # 根组件 (<router-view />)
│       ├── router/index.ts         # 路由 + beforeEach 鉴权守卫
│       ├── api/                    # Axios API 客户端
│       │   ├── http.ts             # Axios 实例 (baseURL /api/v1, 请求Token拦截, 401自动刷新)
│       │   ├── auth.ts             # 认证 API
│       │   ├── accounts.ts         # 账户 API
│       │   ├── categories.ts       # 分类 API
│       │   ├── transactions.ts     # 交易 API (含 blob 导入导出)
│       │   ├── budgets.ts          # 预算 API
│       │   └── reports.ts          # 报表 API
│       ├── stores/                 # Pinia 状态管理
│       │   ├── auth.ts             # token/refreshToken/user, login/register/logout/refresh
│       │   ├── account.ts          # accounts[], fetchAccounts/create/update/delete
│       │   ├── category.ts         # categories[], fetchCategories/create/update/delete
│       │   └── transaction.ts      # transactions[]/total/summary, fetch/create/update/delete
│       ├── views/                  # 页面组件
│       │   ├── Login.vue           # 登录页 (紫色渐变背景)
│       │   ├── Register.vue        # 注册页 (创建家庭/加入家庭 两个Tab)
│       │   ├── Dashboard.vue       # 首页仪表盘 (月度收支/趋势图/饼图/最近交易)
│       │   ├── Accounts.vue        # 账户管理 (卡片网格 + 新增/编辑/删除)
│       │   ├── Transactions.vue    # 交易列表 (筛选/分页/导入导出XLSX/CSV)
│       │   ├── Budgets.vue         # 预算管理 (月度预算 + 进度条)
│       │   ├── Reports.vue         # 报表 (月度/年度/分类/趋势)
│       │   └── Settings.vue        # 设置 (家庭信息/分类管理/成员管理/个人设置)
│       └── components/
│           ├── layout/
│           │   ├── MainLayout.vue  # 主布局 (Header + Sidebar + Content)
│           │   ├── AppSidebar.vue  # 侧边栏菜单 (6项导航, 可折叠)
│           │   └── AppHeader.vue   # 顶部栏
│           └── transaction/
│               └── TransactionForm.vue  # 交易表单弹窗 (支持收入/支出/转账三种类型)
├── nginx/
│   └── nginx.conf                  # 生产环境 Nginx (反代 backend + frontend)
└── docker-compose.yml              # backend:8000 + frontend:80 + nginx:8080
```

---

## API 路由一览

所有接口前缀 `/api/v1`，需 `Authorization: Bearer <access_token>`（auth 路由除外）。

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/auth/register` | 注册（创建家庭） |
| POST | `/auth/register/join` | 注册（加入家庭） |
| POST | `/auth/login` | 登录 |
| POST | `/auth/refresh` | 刷新 Token |
| GET | `/auth/me` | 当前用户信息 |
| PUT | `/auth/me` | 更新用户信息 |
| PUT | `/auth/password` | 修改密码 |
| GET | `/accounts` | 账户列表（含实时余额） |
| POST | `/accounts` | 新增账户 |
| GET | `/accounts/{id}` | 账户详情 |
| PUT | `/accounts/{id}` | 编辑账户 |
| DELETE | `/accounts/{id}` | 删除账户（软删除） |
| GET | `/categories` | 分类列表（可按 type 筛选） |
| POST | `/categories` | 新增分类 |
| PUT | `/categories/{id}` | 编辑分类 |
| DELETE | `/categories/{id}` | 删除分类（软删除） |
| GET | `/transactions` | 交易列表（分页+筛选） |
| POST | `/transactions` | 新增交易 |
| GET | `/transactions/summary` | 收支汇总 |
| GET | `/transactions/{id}` | 交易详情 |
| PUT | `/transactions/{id}` | 编辑交易 |
| DELETE | `/transactions/{id}` | 删除交易 |
| POST | `/transactions/export` | 导出 XLSX/CSV |
| POST | `/transactions/import` | 导入 XLSX |
| GET | `/transactions/import/template` | 下载导入模板 |
| GET | `/budgets` | 预算列表（按年月） |
| POST | `/budgets` | 新增/更新预算（upsert） |
| GET | `/budgets/overview` | 预算概览（总额/已支出/剩余） |
| GET | `/budgets/{id}` | 预算详情 |
| PUT | `/budgets/{id}` | 编辑预算 |
| DELETE | `/budgets/{id}` | 删除预算 |
| GET | `/reports/monthly` | 月度报表 |
| GET | `/reports/yearly` | 年度报表 |
| GET | `/reports/category-breakdown` | 分类支出占比 |
| GET | `/reports/trend` | 收支趋势 |
| GET | `/reports/account-balances` | 各账户余额 |
| GET | `/family` | 家庭信息 |
| PUT | `/family` | 更新家庭信息（管理员） |
| POST | `/family/regenerate-invite` | 重新生成邀请码（管理员） |
| GET | `/family/members` | 成员列表 |
| PUT | `/family/members/{id}/role` | 修改成员角色（管理员） |
| DELETE | `/family/members/{id}` | 移除成员（管理员） |

---

## 数据库模型关系

```
Family (1) ──< User (N)          家庭拥有多个用户
Family (1) ──< Account (N)       家庭拥有多个账户
Family (1) ──< Category (N)      家庭拥有多个分类
Family (1) ──< Transaction (N)   家庭拥有多笔交易
Family (1) ──< Budget (N)        家庭拥有多个预算

Account (1) ──< Transaction (N)         账户关联交易 (account_id)
Account (1) ──< Transaction (N)         转入目标 (transfer_to_account_id, nullable)
Category (1) ──< Transaction (N)        分类关联交易
Category (1) ──< Budget (N)             分类关联预算
Category (1) ──< Category (N)           自引用父子分类 (parent_id)
User (1) ──< Transaction (N)            用户创建的交易 (creator_id)

Budget 唯一约束: (family_id, category_id, year, month)
```

### 关键字段类型

| 字段 | 类型 | 说明 |
|------|------|------|
| `amount` / `initial_balance` | `Numeric(15, 2)` | 数据库存储 Decimal，**输出 Schema 使用 float 序列化为 JSON 数字** |
| `is_active` | `Boolean` | 软删除标记（Account, Category, User） |
| `transaction_type` | `String(10)` | "income" / "expense" / "transfer" |
| `account_type` | `String(30)` | "cash" / "bank_card" / "credit_card" / "e_wallet" / "other" |
| `role` | `String(20)` | "admin" / "member" |
| `invite_code` | `String(8)` | 家庭邀请码，随机8位大写字母+数字 |

---

## 认证流程

```
注册 → POST /auth/register → 返回 access_token + refresh_token
登录 → POST /auth/login    → 返回 access_token + refresh_token

请求 → Authorization: Bearer <access_token>
       ↓ 401 (过期)
       ← 自动 POST /auth/refresh { refresh_token }
       → 获取新 token，重试原请求
       ↓ 刷新也失败
       → 清除 token，跳转 /login
```

- Access Token 有效期: 30 分钟
- Refresh Token 有效期: 7 天
- JWT payload: `{ sub: user_id, family_id, role, exp, type: "access"|"refresh" }`
- Token 存储在 `localStorage` (`token`, `refreshToken`)

---

## 前端数据流

```
View (Accounts.vue)
  └─ onMounted → accountStore.fetchAccounts()
       └─ accountApi.list() → http.get('/accounts')
            └─ Axios → GET /api/v1/accounts
                 └─ Backend → account_service.get_accounts() → 查询 DB
                      └─ 返回 list[AccountOut]
                           └─ { data: [...] } → accounts.value = data
                                └─ Vue 响应式更新模板
```

---

## 关键设计决策与注意事项

### 1. Decimal 序列化（已修复的 Bug）
- **问题**: Pydantic v2 的 `Decimal` 类型 JSON 序列化为字符串 `"1000.00"`，前端 `.toFixed()` 报 TypeError 导致页面崩溃
- **修复**: 输出 Schema 使用 `float` 类型，Router 中 `compute_balance` 返回值用 `float()` 转换
- **前端防御**: 模板中所有 `.toFixed()` 前加 `Number()` 包裹
- **原则**: 输入 Schema 保留 `Decimal`（精度），输出 Schema 用 `float`（兼容 JSON/JS）

### 2. 数据隔离
- 所有查询均以 `current_user.family_id` 过滤，确保家庭间数据隔离
- `get_current_user` 依赖从 JWT 解码 `sub`(user_id)，再查数据库获取最新 `family_id`

### 3. 软删除
- Account、Category、User 均使用 `is_active = False` 软删除
- 查询时默认过滤 `is_active == True`

### 4. 预算 Upsert
- `create_budget` 检查 `(family_id, category_id, year, month)` 唯一约束
- 已存在则更新 `amount`，避免重复预算

### 5. 余额实时计算
- 账户余额不在数据库存储，每次查询时通过 `compute_balance` 实时计算
- 公式: `initial_balance + income - expense - transfer_out + transfer_in`
- 对每个账户执行 4 次 SQL 聚合查询（N+1 问题，小规模可接受）

### 6. 注册自动初始化
- 注册创建家庭时自动生成默认分类（9 个支出分类 + 7 个收入分类）
- 邀请码自动生成（8 位随机大写字母+数字）

---

## 部署

### Docker Compose（生产）
```bash
docker-compose up -d --build
# 访问 http://localhost:8080
```

三个容器:
- `backend`: Gunicorn + Uvicorn workers, 端口 8000
- `frontend`: Nginx 静态文件 + `/api/` 反代到 backend
- `nginx`: 入口网关, 端口 8080, 反代到 frontend 和 backend

数据卷: `app_data` → 持久化 SQLite 数据库 (`/app/data/family_ledger.db`)

### 本地开发
```bash
# 后端
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 前端
cd frontend && npm install
npm run dev   # Vite dev server on :5173, 自动代理 /api → localhost:8000
```

---

## 前端路由

| 路径 | 组件 | 说明 |
|------|------|------|
| `/login` | Login.vue | 登录 |
| `/register` | Register.vue | 注册 |
| `/` | Dashboard.vue | 首页仪表盘 |
| `/transactions` | Transactions.vue | 交易管理 |
| `/accounts` | Accounts.vue | 账户管理 |
| `/budgets` | Budgets.vue | 预算管理 |
| `/reports` | Reports.vue | 报表统计 |
| `/settings` | Settings.vue | 系统设置 |

所有 `/` 子路由需登录（`beforeEach` 守卫检查 `auth.token`）。
