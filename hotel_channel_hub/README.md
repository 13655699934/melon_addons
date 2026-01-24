# 酒店管理与渠道聚合系统

## 概述

这是一套完整的酒店管理与渠道聚合解决方案，专为 **Odoo 18 社区版** 设计开发。系统支持酒店、房型、房间的全面管理，提供线上线下订单处理，集成多渠道API接口，实现酒店与第三方OTA平台的无缝对接。

## 主要功能

### 🏢 酒店基础管理
- 多酒店、多公司支持
- 酒店信息管理（地址、联系方式、星级）
- 房型定义（床型、价格、设施、取消规则）
- 房间管理（房态、价格、售卖类型）
- 实时房态更新（空闲、预订、入住、维修）

### 📝 订单全流程管理
- 线上线下订单统一管理
- 订单流程：草稿 → 确认 → 入住 → 退房
- 支持订单取消与退款
- **一键复刻**功能：快速复制订单重新下单
- 订单日历与看板视图
- 订单确认单打印（含二维码）

### 🌐 渠道聚合与API
- 多渠道接入（携程、美团、飞猪等）
- 企业唯一标识 + Token 认证机制
- Token自动生成与轮换
- RESTful JSON API接口
- 渠道映射与定价策略
- 接口调用日志与审计

### 📊 库存与价格管理
- 按日期管理房间库存
- 总库存、已售、可售自动计算
- 批量更新价格与库存
- 库存预警机制

### 🔐 权限与安全
- 四级权限：酒店经理、渠道经理、前台用户、API客户端
- 多公司数据隔离
- 记录级权限控制
- 价格修改权限保护

## 安装

### 环境要求
- Odoo 18 Community Edition
- Python 3.11+
- PostgreSQL 14+

### 安装步骤

1. **复制模块到addons目录**
   ```bash
   cp -r hotel_channel_hub /path/to/odoo/addons/
   ```

2. **重启Odoo服务**
   ```bash
   sudo systemctl restart odoo
   ```

3. **更新应用列表**
   - 进入Odoo后台
   - 应用 → 更新应用列表

4. **安装模块**
   - 搜索"酒店管理"
   - 点击"安装"

## 使用Docker快速部署

### docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: odoo
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  odoo:
    image: odoo:18.0
    depends_on:
      - postgres
    ports:
      - "8069:8069"
    volumes:
      - ./hotel_channel_hub:/mnt/extra-addons/hotel_channel_hub
      - odoo_data:/var/lib/odoo
    environment:
      - HOST=postgres
      - USER=odoo
      - PASSWORD=odoo
    command: --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons

volumes:
  postgres_data:
  odoo_data:
```

### 启动服务

```bash
docker-compose up -d
```

访问 http://localhost:8069 开始使用

## 演示场景

安装完成后，系统会自动创建演示数据：

### 1. 查看酒店信息
- **酒店管理 → 酒店信息 → 酒店**
- 查看"天悦大酒店"和"云端商务酒店"

### 2. 查看房型和房间
- **酒店管理 → 酒店信息 → 房型**
- **酒店管理 → 酒店信息 → 房间**

### 3. 查看订单
- **酒店管理 → 订单管理 → 订单**
- 查看5个样例订单

### 4. 测试API接口

#### 获取Token
```bash
curl -X POST http://localhost:8069/api/channel/token \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "enterprise_key": "CTRIP_ENTERPRISE_001"
    },
    "id": 1
  }'
```

#### 查询房间
```bash
curl -X POST http://localhost:8069/api/hotel/rooms \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "enterprise_key": "CTRIP_ENTERPRISE_001",
      "token": "YOUR_TOKEN",
      "hotel_id": 1,
      "page": 1,
      "page_size": 20
    },
    "id": 1
  }'
```

#### 创建订单
```bash
curl -X POST http://localhost:8069/api/order/create \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "enterprise_key": "CTRIP_ENTERPRISE_001",
      "token": "YOUR_TOKEN",
      "hotel_id": 1,
      "room_id": 1,
      "check_in": "2025-11-15",
      "check_out": "2025-11-17",
      "quantity": 1,
      "guest_name": "张三",
      "guest_phone": "13800138000",
      "channel_order_no": "CH202511080001"
    },
    "id": 1
  }'
```

### 5. 使用一键复刻功能
- 打开任意订单
- 点击"一键复刻"按钮
- 系统自动创建新订单（草稿状态）
- 修改必要信息后确认

### 6. 查看数据看板
- **酒店管理 → 数据看板**
- 查看订单统计、收入分析等

### 7. 查看同步日志
- **酒店管理 → 消息与日志 → 同步日志**
- 查看API调用记录

## API接口说明

### 接口列表

| 接口 | 方法 | 说明 |
|------|------|------|
| /api/channel/token | POST | 获取企业接入Token |
| /api/hotel/rooms | POST | 获取酒店房间列表 |
| /api/order/create | POST | 创建订单 |
| /api/room/update | POST | 更新房间价格与库存 |
| /api/order/update | POST | 更新订单 |
| /api/order/detail | POST | 查询订单详情 |

### 统一响应格式

```json
{
  "code": 0,
  "msg": "成功",
  "data": {...},
  "timestamp": 1699430400
}
```

- `code`: 0=成功, -1=失败
- `msg`: 消息说明
- `data`: 返回数据
- `timestamp`: 时间戳

## 测试

### 运行单元测试

```bash
# 方法1：使用odoo-bin
odoo-bin -c odoo.conf -d your_db -i hotel_channel_hub --test-enable --stop-after-init

# 方法2：使用pytest（需要安装pytest-odoo）
pytest /path/to/hotel_channel_hub/tests/
```

### 测试覆盖
- ✓ 模型创建与约束验证
- ✓ 订单流程与状态转换
- ✓ 库存扣减与释放
- ✓ Token生成与验证
- ✓ 渠道价格计算
- ✓ 权限边界测试

## 配置文件

### odoo.conf 示例

```ini
[options]
addons_path = /path/to/odoo/addons,/path/to/hotel_channel_hub
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
http_port = 8069
logfile = /var/log/odoo/odoo.log
log_level = info
```

### requirements.txt

```
odoo==18.0
psycopg2-binary
```

## 权限组说明

| 权限组 | 说明 | 权限范围 |
|--------|------|----------|
| 酒店经理 | 完整管理权限 | 所有功能的增删改查 |
| 渠道经理 | 渠道管理权限 | 管理渠道、映射和订单 |
| 前台用户 | 前台操作权限 | 查看订单、办理入住退房 |
| API客户端 | 仅API访问 | 通过API访问，不能登录后台 |

## 常见问题

### 1. Token如何获取？
- 创建渠道记录时自动生成
- 可手动点击"重新生成Token"按钮轮换
- Token有效期1年

### 2. 如何批量更新价格？
- 使用"库存与价格"菜单直接编辑
- 或调用 `/api/room/update` 接口批量更新

### 3. 订单状态流转规则？
- draft（草稿）→ confirmed（已确认）→ checked_in（已入住）→ checked_out（已退房）
- draft/confirmed 可取消
- 状态不可逆转

### 4. 如何设置渠道定价？
- 在"渠道映射"中关联渠道和房型
- 设置定价策略：基础价、加价、减价、固定价
- 支持金额和百分比两种方式

## 技术架构

- **后端**: Python 3.11 + Odoo 18 Framework
- **数据库**: PostgreSQL 14+
- **前端**: Odoo Web Client (OWL Framework)
- **API**: JSON-RPC over HTTP

## 数据库表结构

主要模型：
- `hotel.hotel` - 酒店
- `hotel.room.type` - 房型
- `hotel.room` - 房间
- `hotel.channel` - 渠道
- `hotel.channel.mapping` - 渠道映射
- `hotel.order` - 订单
- `hotel.room.availability` - 库存/价格
- `hotel.sync.log` - 同步日志

## 注意事项

⚠️ **生产环境使用前请：**
1. 进行完整的功能测试
2. 根据实际业务需求调整代码
3. 配置好备份与监控
4. 评估性能与安全性
5. 定期清理过期日志

## 许可证

LGPL-3

## 作者

Your Company

## 更新日志

### v18.0.1.0.0 (2025-11-08)
- 首次发布
- 完整的酒店管理功能
- 多渠道API接口
- 订单全流程管理
- 数据看板与报表

## 支持

如有问题或建议，请联系：
- Email: support@yourcompany.com
- 网站: https://www.yourcompany.com

