# 安装与部署指南

## 目录
1. [环境要求](#环境要求)
2. [Docker部署（推荐）](#docker部署推荐)
3. [手动安装](#手动安装)
4. [初始化配置](#初始化配置)
5. [验证安装](#验证安装)
6. [API测试](#api测试)

---

## 环境要求

### 必需软件
- **Odoo**: 18.0 Community Edition
- **Python**: 3.11 或更高
- **PostgreSQL**: 14 或更高
- **Docker** (可选): 20.10+ 和 Docker Compose 2.0+

### 系统要求
- **CPU**: 2核心或以上
- **内存**: 4GB 或以上
- **磁盘**: 20GB 可用空间

---

## Docker部署（推荐）

### 1. 准备工作

```bash
# 克隆或复制模块到本地
cd /path/to/your/workspace
cp -r hotel_channel_hub ./

# 进入模块目录
cd hotel_channel_hub
```

### 2. 启动服务

```bash
# 启动 PostgreSQL + Odoo
docker-compose up -d

# 查看日志
docker-compose logs -f odoo

# 等待服务启动完成（约1-2分钟）
```

### 3. 访问系统

打开浏览器访问：http://localhost:8069

- **首次访问**：需要创建数据库
  - 数据库名称：`hotel_db`（自定义）
  - 邮箱：`admin@example.com`
  - 密码：`admin`（建议修改）
  - 语言：`简体中文`
  - 加载演示数据：`勾选`

### 4. 安装模块

1. 登录后台
2. 进入 **应用 → 更新应用列表**
3. 搜索 `酒店管理`
4. 点击 **安装**

### 5. 停止服务

```bash
# 停止服务
docker-compose down

# 停止并删除数据
docker-compose down -v
```

---

## 手动安装

### 1. 安装Odoo

#### 方法A：使用官方脚本（Ubuntu/Debian）

```bash
# 下载安装脚本
wget https://raw.githubusercontent.com/odoo/odoo/18.0/setup/odoo -O odoo-install.sh

# 添加执行权限
chmod +x odoo-install.sh

# 执行安装
sudo ./odoo-install.sh
```

#### 方法B：从源码安装

```bash
# 安装依赖
sudo apt update
sudo apt install -y python3-pip python3-dev libxml2-dev libxslt1-dev \
    libldap2-dev libsasl2-dev libtiff5-dev libjpeg8-dev libopenjp2-7-dev \
    zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev \
    libfribidi-dev libxcb1-dev libpq-dev git postgresql nodejs npm

# 克隆Odoo源码
git clone https://github.com/odoo/odoo.git --depth 1 --branch 18.0 /opt/odoo

# 安装Python依赖
cd /opt/odoo
pip3 install -r requirements.txt

# 安装wkhtmltopdf（用于PDF报表）
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb
sudo dpkg -i wkhtmltox_0.12.6.1-2.jammy_amd64.deb
sudo apt-get install -f
```

### 2. 配置PostgreSQL

```bash
# 创建Odoo数据库用户
sudo -u postgres createuser -s odoo

# 设置密码
sudo -u postgres psql
postgres=# ALTER USER odoo WITH PASSWORD 'odoo';
postgres=# \q
```

### 3. 部署模块

```bash
# 创建addons目录
sudo mkdir -p /opt/odoo/custom-addons

# 复制模块
sudo cp -r hotel_channel_hub /opt/odoo/custom-addons/

# 设置权限
sudo chown -R odoo:odoo /opt/odoo/custom-addons
```

### 4. 配置Odoo

创建配置文件 `/etc/odoo.conf`：

```ini
[options]
addons_path = /opt/odoo/addons,/opt/odoo/custom-addons
admin_passwd = admin_password_change_me
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
http_port = 8069
logfile = /var/log/odoo/odoo.log
```

创建日志目录：

```bash
sudo mkdir -p /var/log/odoo
sudo chown odoo:odoo /var/log/odoo
```

### 5. 创建系统服务

创建 `/etc/systemd/system/odoo.service`：

```ini
[Unit]
Description=Odoo 18
After=network.target postgresql.service

[Service]
Type=simple
User=odoo
Group=odoo
ExecStart=/usr/bin/python3 /opt/odoo/odoo-bin -c /etc/odoo.conf
StandardOutput=journal+console

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
# 重载systemd
sudo systemctl daemon-reload

# 启动Odoo
sudo systemctl start odoo

# 设置开机自启
sudo systemctl enable odoo

# 查看状态
sudo systemctl status odoo
```

---

## 初始化配置

### 1. 创建数据库

访问 http://localhost:8069，填写：
- 数据库名称：`hotel_db`
- 邮箱：`admin@example.com`
- 密码：`admin`
- 语言：简体中文
- 加载演示数据：勾选

### 2. 安装模块

1. 登录系统
2. 应用 → 更新应用列表
3. 搜索"酒店管理"
4. 点击"安装"

### 3. 配置用户权限

**创建酒店经理用户：**
1. 设置 → 用户与公司 → 用户
2. 创建新用户
3. 分配"酒店管理 / 酒店经理"权限组

**创建前台用户：**
1. 创建新用户
2. 分配"酒店管理 / 前台用户"权限组

---

## 验证安装

### 1. 检查演示数据

- **酒店管理 → 酒店信息 → 酒店**：应有2家酒店
- **酒店管理 → 酒店信息 → 房型**：应有3种房型
- **酒店管理 → 酒店信息 → 房间**：应有5个房间
- **酒店管理 → 渠道管理 → 渠道**：应有2个渠道
- **酒店管理 → 订单管理 → 订单**：应有5个订单

### 2. 测试订单流程

1. 创建新订单
2. 确认订单（检查房间状态变为"已预订"）
3. 办理入住（检查房间状态变为"已入住"）
4. 办理退房（检查房间状态变为"空闲"）

### 3. 测试一键复刻

1. 打开任意已确认订单
2. 点击"一键复刻"按钮
3. 验证新订单已创建为草稿状态

---

## API测试

### 1. 获取Token

在"渠道管理 → 渠道"中，找到渠道的`enterprise_key`和`token`。

或通过API获取：

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

### 2. 查询房间

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

### 3. 创建订单

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
      "guest_name": "测试客人",
      "guest_phone": "13800138000"
    },
    "id": 1
  }'
```

### 4. 查看日志

访问 **酒店管理 → 消息与日志 → 同步日志**，查看API调用记录。

---

## 使用Postman测试API

### 1. 导入Postman集合

创建 `hotel_api.postman_collection.json`：

```json
{
  "info": {
    "name": "Hotel Channel Hub API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8069"
    },
    {
      "key": "enterprise_key",
      "value": "CTRIP_ENTERPRISE_001"
    },
    {
      "key": "token",
      "value": ""
    }
  ],
  "item": [
    {
      "name": "1. Get Token",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/channel/token",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"jsonrpc\": \"2.0\",\n  \"method\": \"call\",\n  \"params\": {\n    \"enterprise_key\": \"{{enterprise_key}}\"\n  },\n  \"id\": 1\n}"
        }
      }
    },
    {
      "name": "2. Get Hotel Rooms",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/hotel/rooms",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"jsonrpc\": \"2.0\",\n  \"method\": \"call\",\n  \"params\": {\n    \"enterprise_key\": \"{{enterprise_key}}\",\n    \"token\": \"{{token}}\",\n    \"hotel_id\": 1,\n    \"page\": 1,\n    \"page_size\": 20\n  },\n  \"id\": 1\n}"
        }
      }
    },
    {
      "name": "3. Create Order",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/order/create",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"jsonrpc\": \"2.0\",\n  \"method\": \"call\",\n  \"params\": {\n    \"enterprise_key\": \"{{enterprise_key}}\",\n    \"token\": \"{{token}}\",\n    \"hotel_id\": 1,\n    \"room_id\": 1,\n    \"check_in\": \"2025-11-15\",\n    \"check_out\": \"2025-11-17\",\n    \"quantity\": 1,\n    \"guest_name\": \"测试客人\",\n    \"guest_phone\": \"13800138000\"\n  },\n  \"id\": 1\n}"
        }
      }
    }
  ]
}
```

---

## 运行测试

```bash
# 使用odoo-bin运行测试
odoo-bin -c /etc/odoo.conf -d hotel_db -i hotel_channel_hub --test-enable --stop-after-init

# 或使用Docker
docker exec -it hotel_odoo odoo -d hotel_db -i hotel_channel_hub --test-enable --stop-after-init
```

---

## 常见问题

### 1. 端口已被占用

如果8069端口已被占用，修改`docker-compose.yml`或`odoo.conf`中的端口号。

### 2. 模块未显示

- 检查模块路径是否正确
- 更新应用列表
- 查看日志是否有错误

### 3. Token验证失败

- 检查Token是否正确
- 检查Token是否过期
- 重新生成Token

### 4. 数据库连接失败

- 检查PostgreSQL是否运行
- 检查数据库用户名和密码
- 检查防火墙设置

---

## 生产环境建议

1. **修改默认密码**
2. **配置SSL证书**（使用Nginx反向代理）
3. **配置定时备份**
4. **优化Worker数量**
5. **配置日志轮转**
6. **使用Redis缓存**（可选）
7. **配置监控告警**

---

## 技术支持

如有问题，请联系：
- Email: support@yourcompany.com
- 文档: 查看 README.md

