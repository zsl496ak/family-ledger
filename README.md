# 家庭记账 (Family Ledger)

一个简洁实用的家庭共享记账 Web 应用，支持多成员协作记账、预算管理、统计报表等功能。

## 功能特性

- **交易管理** - 记录收入、支出、转账，支持分类、备注
- **账户管理** - 现金、银行卡、信用卡、电子钱包等多种账户类型
- **预算管理** - 按月按分类设置预算，实时追踪进度
- **统计报表** - 月度/年度收支汇总、分类饼图、趋势折线图
- **导入导出** - 支持 Excel/CSV 格式批量导入导出交易记录
- **家庭共享** - 邀请码加入家庭，多成员共享账本
- **响应式设计** - 同时适配电脑和手机浏览器

## 技术栈

- **后端**: Python FastAPI + SQLAlchemy + SQLite
- **前端**: Vue 3 + TypeScript + Element Plus + ECharts
- **部署**: Docker Compose + Nginx

## 快速开始

### Docker 部署（推荐）

```bash
# 克隆项目
git clone https://github.com/$(git config user.name)/family-ledger.git
cd family-ledger

# 修改密钥
echo "SECRET_KEY=$(openssl rand -hex 32)" > .env

# 启动服务
docker compose up -d --build
```

访问 http://localhost 即可使用。

### 本地开发

**后端:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**前端:**

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173，API 会代理到后端 8000 端口。

## 项目结构

```
family-ledger/
├── backend/           # FastAPI 后端
│   └── app/
│       ├── models/    # 数据模型
│       ├── schemas/   # 请求/响应 Schema
│       ├── routers/   # API 路由
│       └── services/  # 业务逻辑
├── frontend/          # Vue 3 前端
│   └── src/
│       ├── views/     # 页面组件
│       ├── components/# 通用组件
│       ├── stores/    # Pinia 状态
│       └── api/       # API 调用
├── nginx/             # Nginx 配置
└── docker-compose.yml
```

## API 文档

启动后端后，访问 http://localhost:8000/docs 查看 Swagger API 文档。

## License

MIT
