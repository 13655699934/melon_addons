# Field Masking Widget (web_field_mask)

字段脱敏显示挂件 - Odoo 18.0

## 功能特性

### 支持的脱敏类型
- **手机号**: 138****1234
- **身份证**: 340***********1234
- **银行卡**: 6222 **** **** 1234
- **邮箱**: abc***@gmail.com
- **姓名**: 张*、李**
- **自定义**: 自由设置保留位数

### 交互功能
- 🖱️ 鼠标悬停显示完整内容
- 📋 双击复制到剪贴板
- 🎨 优雅的视觉效果

## 安装

```bash
# 解压到addons目录
unzip web_field_mask_v18.0.1.0.0.zip -d /opt/odoo/addons/

# 重启Odoo
sudo systemctl restart odoo

# 安装模块
./odoo-bin -i web_field_mask -d your_database
```

## 使用方法

### 基础用法
```xml
         <field name="name"  widget="masked_field" options="{'mask_type': 'name'}"/>
        <field name="id_card" widget="masked_field" options="{'mask_type': 'id_card'}"/>
        <field name="mobile" widget="masked_field" options="{'mask_type': 'mobile'}"/>
```

### 指定脱敏类型

```xml
         <field name="name"  widget="masked_field" options="{'mask_type': 'name'}"/>
        <field name="id_card" widget="masked_field" options="{'mask_type': 'id_card'}"/>
        <field name="mobile" widget="masked_field" options="{'mask_type': 'mobile'}"/>
```


### 自定义脱敏
```xml
<field name="custom" widget="masked_field" mask_type="custom" mask_start="3" mask_end="4"/>
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| mask_type | String | "phone" | 脱敏类型 |
| mask_char | String | "*" | 脱敏字符 |
| mask_start | Integer | 3 | 保留前N位 |
| mask_end | Integer | 4 | 保留后N位 |
| show_on_hover | Boolean | True | 鼠标悬停显示 |

## 许可

LGPL-3.0
