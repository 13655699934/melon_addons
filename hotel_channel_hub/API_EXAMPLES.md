# API接口调用示例

## 目录
1. [接口概述](#接口概述)
2. [认证流程](#认证流程)
3. [接口详细说明](#接口详细说明)
4. [错误处理](#错误处理)
5. [Postman集合](#postman集合)

---

## 接口概述

### 基础信息
- **协议**: HTTP/HTTPS
- **格式**: JSON-RPC 2.0
- **编码**: UTF-8
- **认证**: Enterprise Key + Token

### 统一响应格式

```json
{
  "code": 0,
  "msg": "成功",
  "data": {...},
  "timestamp": 1699430400
}
```

**字段说明:**
- `code`: 状态码，0=成功，-1=失败
- `msg`: 消息说明
- `data`: 返回的数据对象
- `timestamp`: Unix时间戳

---

## 认证流程

### 1. 获取企业标识（Enterprise Key）

在Odoo后台创建渠道时，系统会自动生成`enterprise_key`。

路径：**酒店管理 → 渠道管理 → 渠道**

### 2. 获取Token

**接口**: `POST /api/channel/token`

**请求示例**:
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

**响应示例**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "code": 0,
    "msg": "Token获取成功",
    "data": {
      "enterprise_key": "CTRIP_ENTERPRISE_001",
      "token": "xB7kF3mP9qN2wR5tY8vC1dG4hJ6lZ0aS",
      "expiry": "2026-11-08 12:00:00"
    },
    "timestamp": 1699430400
  }
}
```

### 3. 使用Token调用接口

后续所有接口调用都需要在`params`中传入`enterprise_key`和`token`。

---

## 接口详细说明

### 1. 获取酒店房间列表

**接口**: `POST /api/hotel/rooms`

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| enterprise_key | string | 是 | 企业唯一标识 |
| token | string | 是 | 访问Token |
| hotel_id | integer | 否 | 酒店ID，不传则返回所有 |
| page | integer | 否 | 页码，默认1 |
| page_size | integer | 否 | 每页数量，默认20 |

**请求示例**:
```bash
curl -X POST http://localhost:8069/api/hotel/rooms \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "enterprise_key": "CTRIP_ENTERPRISE_001",
      "token": "xB7kF3mP9qN2wR5tY8vC1dG4hJ6lZ0aS",
      "hotel_id": 1,
      "page": 1,
      "page_size": 20
    },
    "id": 1
  }'
```

**响应示例**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "code": 0,
    "msg": "查询成功",
    "data": {
      "total": 5,
      "page": 1,
      "page_size": 20,
      "rooms": [
        {
          "id": 1,
          "number": "301",
          "hotel_id": 1,
          "hotel_name": "天悦大酒店",
          "room_type_id": 1,
          "room_type_name": "豪华大床房",
          "floor": 3,
          "status": "vacant",
          "sale_type": "both",
          "price": 588.0,
          "bed_type": "king",
          "max_occupancy": 2,
          "has_breakfast": true
        }
      ]
    },
    "timestamp": 1699430400
  }
}
```

---

### 2. 创建订单

**接口**: `POST /api/order/create`

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| enterprise_key | string | 是 | 企业唯一标识 |
| token | string | 是 | 访问Token |
| hotel_id | integer | 是 | 酒店ID |
| room_id | integer | 否 | 房间ID |
| room_type_id | integer | 否 | 房型ID（room_id和room_type_id至少填一个） |
| check_in | string | 是 | 入住日期，格式：YYYY-MM-DD |
| check_out | string | 是 | 离店日期，格式：YYYY-MM-DD |
| quantity | integer | 否 | 房间数量，默认1 |
| guest_name | string | 是 | 预订人姓名 |
| guest_phone | string | 是 | 预订人手机号 |
| guest_email | string | 否 | 预订人邮箱 |
| guest_id_number | string | 否 | 身份证号 |
| channel_order_no | string | 否 | 渠道订单号 |
| unit_price | float | 否 | 单价（不传则使用房间价格） |
| note | string | 否 | 备注 |
| auto_confirm | boolean | 否 | 是否自动确认，默认true |

**请求示例**:
```bash
curl -X POST http://localhost:8069/api/order/create \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "enterprise_key": "CTRIP_ENTERPRISE_001",
      "token": "xB7kF3mP9qN2wR5tY8vC1dG4hJ6lZ0aS",
      "hotel_id": 1,
      "room_id": 1,
      "check_in": "2025-11-15",
      "check_out": "2025-11-17",
      "quantity": 1,
      "guest_name": "张三",
      "guest_phone": "13800138000",
      "guest_email": "zhangsan@example.com",
      "channel_order_no": "CH202511080001",
      "note": "无烟房"
    },
    "id": 1
  }'
```

**响应示例**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "code": 0,
    "msg": "订单创建成功",
    "data": {
      "order_id": 123,
      "order_no": "HO000123",
      "state": "confirmed",
      "total_price": 1176.0,
      "nights": 2
    },
    "timestamp": 1699430400
  }
}
```

---

### 3. 批量更新房间价格与库存

**接口**: `POST /api/room/update`

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| enterprise_key | string | 是 | 企业唯一标识 |
| token | string | 是 | 访问Token |
| updates | array | 是 | 更新数据数组 |

**updates数组元素**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| hotel_id | integer | 是 | 酒店ID |
| room_id | integer | 否 | 房间ID |
| room_type_id | integer | 否 | 房型ID（room_id和room_type_id至少填一个） |
| date | string | 是 | 日期，格式：YYYY-MM-DD |
| price | float | 否 | 价格 |
| quota | integer | 否 | 库存 |
| is_open | boolean | 否 | 是否开放售卖 |

**请求示例**:
```bash
curl -X POST http://localhost:8069/api/room/update \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "enterprise_key": "CTRIP_ENTERPRISE_001",
      "token": "xB7kF3mP9qN2wR5tY8vC1dG4hJ6lZ0aS",
      "updates": [
        {
          "hotel_id": 1,
          "room_id": 1,
          "date": "2025-11-15",
          "price": 688.0,
          "quota": 5
        },
        {
          "hotel_id": 1,
          "room_id": 1,
          "date": "2025-11-16",
          "price": 688.0,
          "quota": 5
        }
      ]
    },
    "id": 1
  }'
```

**响应示例**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "code": 0,
    "msg": "更新完成",
    "data": {
      "results": [
        {
          "success": true,
          "id": 45,
          "date": "2025-11-15"
        },
        {
          "success": true,
          "id": 46,
          "date": "2025-11-16"
        }
      ]
    },
    "timestamp": 1699430400
  }
}
```

---

### 4. 更新订单

**接口**: `POST /api/order/update`

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| enterprise_key | string | 是 | 企业唯一标识 |
| token | string | 是 | 访问Token |
| order_id | integer | 否 | 订单ID |
| order_no | string | 否 | 订单号（order_id和order_no至少填一个） |
| action | string | 是 | 操作类型：cancel（取消）、update_dates（改期） |
| cancel_reason | string | 否 | 取消原因（action=cancel时） |
| check_in | string | 否 | 新入住日期（action=update_dates时） |
| check_out | string | 否 | 新离店日期（action=update_dates时） |

**请求示例（取消订单）**:
```bash
curl -X POST http://localhost:8069/api/order/update \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "enterprise_key": "CTRIP_ENTERPRISE_001",
      "token": "xB7kF3mP9qN2wR5tY8vC1dG4hJ6lZ0aS",
      "order_no": "HO000123",
      "action": "cancel",
      "cancel_reason": "客户取消"
    },
    "id": 1
  }'
```

**响应示例**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "code": 0,
    "msg": "订单已取消",
    "data": {
      "order_id": 123,
      "order_no": "HO000123",
      "state": "cancelled"
    },
    "timestamp": 1699430400
  }
}
```

---

### 5. 查询订单详情

**接口**: `POST /api/order/detail`

**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| enterprise_key | string | 是 | 企业唯一标识 |
| token | string | 是 | 访问Token |
| order_id | integer | 否 | 订单ID |
| order_no | string | 否 | 订单号（order_id和order_no至少填一个） |

**请求示例**:
```bash
curl -X POST http://localhost:8069/api/order/detail \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
      "enterprise_key": "CTRIP_ENTERPRISE_001",
      "token": "xB7kF3mP9qN2wR5tY8vC1dG4hJ6lZ0aS",
      "order_no": "HO000123"
    },
    "id": 1
  }'
```

**响应示例**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "code": 0,
    "msg": "查询成功",
    "data": {
      "order_id": 123,
      "order_no": "HO000123",
      "channel_order_no": "CH202511080001",
      "hotel_id": 1,
      "hotel_name": "天悦大酒店",
      "room_id": 1,
      "room_number": "301",
      "room_type_id": 1,
      "room_type_name": "豪华大床房",
      "guest_name": "张三",
      "guest_phone": "13800138000",
      "guest_email": "zhangsan@example.com",
      "check_in": "2025-11-15",
      "check_out": "2025-11-17",
      "nights": 2,
      "quantity": 1,
      "unit_price": 588.0,
      "total_price": 1176.0,
      "state": "confirmed",
      "confirmed_date": "2025-11-08 10:30:00",
      "checkin_date": null,
      "checkout_date": null,
      "note": "无烟房"
    },
    "timestamp": 1699430400
  }
}
```

---

## 错误处理

### 常见错误码

| Code | 说明 | 处理方式 |
|------|------|----------|
| -1 | Token验证失败 | 检查Token是否正确或过期，重新获取Token |
| -1 | 缺少必填参数 | 检查请求参数 |
| -1 | 订单创建失败 | 检查日期、房间可用性等 |
| -1 | 无权操作此订单 | 检查订单是否属于该渠道 |

### 错误响应示例

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "code": -1,
    "msg": "Token验证失败",
    "data": {},
    "timestamp": 1699430400
  }
}
```

---

## Postman集合

### 导入Postman

1. 打开Postman
2. 点击"Import"
3. 选择下面的JSON内容并导入

### Postman Collection JSON

```json
{
  "info": {
    "name": "Hotel Channel Hub API",
    "description": "酒店管理与渠道聚合系统API接口集合",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8069",
      "type": "string"
    },
    {
      "key": "enterprise_key",
      "value": "CTRIP_ENTERPRISE_001",
      "type": "string"
    },
    {
      "key": "token",
      "value": "",
      "type": "string"
    }
  ],
  "item": [
    {
      "name": "1. 获取Token",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": {
          "raw": "{{base_url}}/api/channel/token",
          "host": ["{{base_url}}"],
          "path": ["api", "channel", "token"]
        },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"jsonrpc\": \"2.0\",\n  \"method\": \"call\",\n  \"params\": {\n    \"enterprise_key\": \"{{enterprise_key}}\"\n  },\n  \"id\": 1\n}"
        }
      }
    },
    {
      "name": "2. 获取酒店房间列表",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": {
          "raw": "{{base_url}}/api/hotel/rooms",
          "host": ["{{base_url}}"],
          "path": ["api", "hotel", "rooms"]
        },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"jsonrpc\": \"2.0\",\n  \"method\": \"call\",\n  \"params\": {\n    \"enterprise_key\": \"{{enterprise_key}}\",\n    \"token\": \"{{token}}\",\n    \"hotel_id\": 1,\n    \"page\": 1,\n    \"page_size\": 20\n  },\n  \"id\": 1\n}"
        }
      }
    },
    {
      "name": "3. 创建订单",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": {
          "raw": "{{base_url}}/api/order/create",
          "host": ["{{base_url}}"],
          "path": ["api", "order", "create"]
        },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"jsonrpc\": \"2.0\",\n  \"method\": \"call\",\n  \"params\": {\n    \"enterprise_key\": \"{{enterprise_key}}\",\n    \"token\": \"{{token}}\",\n    \"hotel_id\": 1,\n    \"room_id\": 1,\n    \"check_in\": \"2025-11-15\",\n    \"check_out\": \"2025-11-17\",\n    \"quantity\": 1,\n    \"guest_name\": \"张三\",\n    \"guest_phone\": \"13800138000\"\n  },\n  \"id\": 1\n}"
        }
      }
    },
    {
      "name": "4. 批量更新价格库存",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": {
          "raw": "{{base_url}}/api/room/update",
          "host": ["{{base_url}}"],
          "path": ["api", "room", "update"]
        },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"jsonrpc\": \"2.0\",\n  \"method\": \"call\",\n  \"params\": {\n    \"enterprise_key\": \"{{enterprise_key}}\",\n    \"token\": \"{{token}}\",\n    \"updates\": [\n      {\n        \"hotel_id\": 1,\n        \"room_id\": 1,\n        \"date\": \"2025-11-15\",\n        \"price\": 688.0,\n        \"quota\": 5\n      }\n    ]\n  },\n  \"id\": 1\n}"
        }
      }
    },
    {
      "name": "5. 取消订单",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": {
          "raw": "{{base_url}}/api/order/update",
          "host": ["{{base_url}}"],
          "path": ["api", "order", "update"]
        },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"jsonrpc\": \"2.0\",\n  \"method\": \"call\",\n  \"params\": {\n    \"enterprise_key\": \"{{enterprise_key}}\",\n    \"token\": \"{{token}}\",\n    \"order_no\": \"HO000001\",\n    \"action\": \"cancel\",\n    \"cancel_reason\": \"客户取消\"\n  },\n  \"id\": 1\n}"
        }
      }
    },
    {
      "name": "6. 查询订单详情",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "url": {
          "raw": "{{base_url}}/api/order/detail",
          "host": ["{{base_url}}"],
          "path": ["api", "order", "detail"]
        },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"jsonrpc\": \"2.0\",\n  \"method\": \"call\",\n  \"params\": {\n    \"enterprise_key\": \"{{enterprise_key}}\",\n    \"token\": \"{{token}}\",\n    \"order_no\": \"HO000001\"\n  },\n  \"id\": 1\n}"
        }
      }
    }
  ]
}
```

---

## 最佳实践

1. **Token管理**
   - Token有效期1年，建议定期轮换
   - Token泄露时立即重新生成
   - 不要在前端暴露Token

2. **错误重试**
   - 网络错误时使用指数退避重试
   - 业务错误不应重试
   - 最多重试3次

3. **日志记录**
   - 所有API调用会自动记录到"同步日志"
   - 可通过日志追踪问题
   - 生产环境定期清理过期日志

4. **性能优化**
   - 批量操作使用批量接口
   - 避免频繁调用
   - 使用分页避免大量数据

5. **安全建议**
   - 使用HTTPS加密传输
   - 定期更新Token
   - 限制API调用频率
   - 记录并监控异常调用

---

**技术支持**: support@yourcompany.com

