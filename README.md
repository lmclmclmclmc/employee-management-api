# Employee Management API

一个使用 Python、FastAPI 和 SQLite 开发的员工管理后端项目。

项目支持用户注册、JWT 登录认证、员工 CRUD、分页查询、请求日志、健康检查和自动化测试。

## 技术栈

- Python 3.11
- FastAPI
- SQLite
- Pydantic
- PyJWT
- Argon2
- unittest

## 主要功能

- 用户注册
- 密码哈希存储
- JWT Bearer Token 登录认证
- 查询当前登录用户
- 新增、查询、修改和删除员工
- 员工列表分页
- 请求参数校验
- CORS 配置
- 请求日志和耗时统计
- 数据库健康检查
- 自动化测试
- 环境变量配置
- 按姓名模糊搜索员工
- Ruff 代码检查和格式化
- 测试覆盖率检查
- GitHub Actions 持续集成

## 项目结构

```text
.
├── main_db.py          # FastAPI 应用入口
├── auth_router.py      # 注册、登录和当前用户接口
├── employee_router.py  # 员工 CRUD 接口
├── health_router.py    # 健康检查接口
├── database.py         # SQLite 数据访问
├── security.py         # 密码哈希和 JWT
├── dependencies.py     # 登录认证依赖
├── schemas.py          # Pydantic 数据模型
├── config.py           # 环境配置
├── test_auth.py        # 认证测试
├── test_main_db.py     # 员工 API 测试
├── test_health.py      # 健康检查测试
└── requirements.txt    # Python 依赖
```

## 安装

创建虚拟环境：

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

安装依赖：

```bash
python -m pip install -r requirements.txt
```

## 配置

复制环境变量模板：

```bash
cp .env.example .env
```

生成随机 JWT 密钥：

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

把生成结果写入 `.env` 的 `JWT_SECRET_KEY`。

不要将真实 `.env` 文件提交到 Git。

## 启动服务

```bash
uvicorn main_db:app --reload
```

接口文档：

```text
http://127.0.0.1:8000/docs
```

健康检查：

```text
http://127.0.0.1:8000/health
```

## API 接口

| 方法 | 路径 | 是否需要登录 | 说明 |
|---|---|---:|---|
| POST | `/register` | 否 | 注册用户 |
| POST | `/login` | 否 | 登录并获取 Token |
| GET | `/me` | 是 | 查询当前用户 |
| GET | `/employees` | 否 | 查询员工列表 |
| GET | `/employees/{employee_id}` | 否 | 查询单个员工 |
| POST | `/employees` | 是 | 新增员工 |
| PUT | `/employees/{employee_id}` | 是 | 完整修改员工 |
| PATCH | `/employees/{employee_id}` | 是 | 部分修改员工 |
| DELETE | `/employees/{employee_id}` | 是 | 删除员工 |
| GET | `/health` | 否 | 健康检查 |

员工列表支持分页和姓名搜索：

```text
GET /employees?limit=10&offset=0&name=wang
```

## 运行测试

```bash
python -m unittest -v
```

当前项目包含 30 个自动化测试，业务代码覆盖率为 93%，覆盖注册、登录、Token 验证、员工 CRUD、搜索、数据校验和健康检查。

运行代码质量检查：

```bash
ruff check .
ruff format --check .
```

运行带覆盖率的测试：

```bash
python -m coverage run -m unittest
python -m coverage report
```