# 工业物联网时钟同步设备管理平台

## 项目定位

本项目是一次**工业级项目主题的概念验证（Proof of Concept）**，对**最小可行产品（MVP）**的模拟实现。

- **概念验证**：验证“时钟同步设备监控与管理”这一工业场景在技术栈选型、前后端分工、多协议扩展上的可行性，不追求生产级完备性。
- **MVP 模拟**：实现设备登记、列表展示、状态看板、多协议连接扩展与用户入口预留等最小功能集，为后续迭代预留接口。

适用于演示、教学与需求探索，不作为直接投产的工业系统使用。

---

## 功能概览

| 模块 | 说明 |
|------|------|
| 设备管理 | 设备注册（序列号、型号、IP、固件版本）、设备列表展示 |
| 监控看板 | 设备数量与在线统计、同步状态统计、时间偏差折线图（ECharts） |
| 多协议连接 | 工厂模式封装 NTP/PTP 连接创建，可扩展新协议而不影响调用方 |
| 用户入口 | 前端预留登录/注册入口（仅展示、待扩展） |
---

## 技术栈

- **前端**：Vue 3、TypeScript、Vite、Element Plus、ECharts、Axios  
- **后端**：FastAPI、SQLAlchemy、MySQL（生产）/ SQLite（演示）、Redis、MQTT（Paho）  
- **设计**：前后端分离、分层架构（API → Service → DB）、连接层工厂模式  

---

## 项目结构

```clock_sync_platform/
├── app/                    # 后端
│   ├── api/                # 接口层
│   ├── connections/        # 多协议连接（ConnectionFactory、NTP/PTP）
│   ├── core/               # 配置、数据库、Redis
│   ├── models/             # 设备、设备状态
│   ├── mqtt/               # MQTT 订阅与状态上报
│   ├── schemas/            # 请求/响应模型
│   └── services/           # 业务逻辑
├── clock-sync-frontend/     # 前端 SPA
│   └── src/
│       ├── api/            # 设备、状态接口
│       ├── views/          # 仪表盘、设备列表、设备注册
│       ├── components/     # 设备表、状态图表
│       └── router/
├── run_demo.py             # 演示用后端（SQLite，无需 MySQL/Redis/MQTT）
└── requirements.txt
```

---

## 快速运行

**演示模式**

```bash
# 后端（SQLite，端口 8000）
pip install fastapi uvicorn sqlalchemy
python run_demo.py

# 前端（端口 5173）
cd clock-sync-frontend && npm install && npm run dev
```

浏览器访问 http://localhost:5173 。

**生产配置**：使用 MySQL、Redis、MQTT 时，配置 `.env` 并启动 `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`。

---

## 说明与限制

- 时钟同步**执行**由设备或时间源完成，本平台负责**状态上报的接收与展示**。
- 当前无按设备 IP 主动拉取状态、告警、权限与审计等工业级能力，可作为后续迭代方向。

---

## 许可证

按项目实际需求添加。
