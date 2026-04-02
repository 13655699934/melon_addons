# mln Drag Drop Gallery (Odoo 18)

**模块名 · Technical name:** `mln_drag_drop`  
**挂件名 · Widget:** `drag_drop_images`

## 概述 · Overview

**中文：** 在后台表单的 **one2many** 子表上提供图集挂件：**批量上传**（拖入或多选文件）、**点击缩略图放大预览**（灯箱）、**单张下载**与**已保存行的 ZIP 打包下载**。

**English:** Backend **one2many** image gallery widget: **batch upload** (drag-and-drop or multi-select files), **click thumbnail for lightbox preview**, **per-image download**, and **ZIP download** for lines already saved in the database.

---

## 功能概要 · Features

| 中文 | English |
|------|---------|
| 批量上传：拖多个文件到虚线区域，或一次多选；每图一行子记录。 | **Batch upload:** drop many files or multi-select; one child row per image. |
| 放大预览：点击缩略图打开遮罩大图；Esc / 遮罩 / 关闭钮退出。 | **Preview:** click thumbnail → overlay; Esc, backdrop, or close control. |
| 下载：左下单张；工具栏 ZIP 仅含已保存子行（先保存主表）。 | **Download:** per-tile control; *Download all (ZIP)* only for persisted rows (save parent first). |
| 文件名：子表若有 `name`（Char），上传时写入原始文件名。 | **Captions:** if the child model has Char `name`, the original file name is stored. |
| 演示：菜单 **mln Drag Drop → Demo**。 | **Demo:** menu **mln Drag Drop → Demo**. |

---

## 安装 · Installation

**中文**

1. 将 `mln_drag_drop` 加入插件路径。  
2. 更新应用列表。  
3. 安装 **mln Drag Drop Gallery**。

**English**

1. Add `mln_drag_drop` to your addons path.  
2. Update the Apps list.  
3. Install **mln Drag Drop Gallery**.

---

## 内置演示 · Built-in demo

| 中文 | English |
|------|---------|
| 菜单：**mln Drag Drop → Demo**（`base.group_user`） | Menu: **mln Drag Drop → Demo** (`base.group_user`) |
| 模型：`mln_drag_drop.demo`、`mln_drag_drop.demo.line` | Models: `mln_drag_drop.demo`, `mln_drag_drop.demo.line` |
| 示例数据：`data/mln_drag_drop_demo_data.xml` | Sample data: `data/mln_drag_drop_demo_data.xml` |

---

## 在视图中使用 · View usage

子表需图片字段（常用 `image_1920`），建议有 `name`。  
The child model needs an image field (often `image_1920`); a `name` field is recommended.

```xml
<field name="media_ids"
       widget="drag_drop_images"
       options="{
           'childImageField': 'image_1920',
           'acceptedFileExtensions': 'image/*',
           'extraData': {
               'enable_zoom': true,
               'previewImage': 'image_128',
               'cssStyles': 'width:150px;height:200px;border-radius:15px;object-fit:cover;'
           }
       }"/>
```

### `options` 说明 · Options

**中文**

- `childImageField`：子表存图字段，默认 `image_1920`。  
- `acceptedFileExtensions`：默认 `image/*`。  
- `extraData`：新建子行的默认值。`previewImage`、`cssStyles`、`enable_zoom` / `enableZoom` **仅界面**，不写库；其余键传入子表字段默认值。  
- 灯箱与单张下载内置；ZIP 需子行已落库。

**English**

- `childImageField`: child image field (default `image_1920`).  
- `acceptedFileExtensions`: default `image/*`.  
- `extraData`: defaults for new lines. `previewImage`, `cssStyles`, `enable_zoom` / `enableZoom` are **UI-only**; other keys are passed as field defaults.  
- Lightbox and single download are always available; ZIP requires saved child rows.

---

## 集成注意 · Integration notes

**中文**

1. 挂件为子表图片字段在 `relatedFields` 中设 `readonly: false`，否则保存可能丢二进制。  
2. 子表若有 `name`，亦需可写，创建时才会提交文件名。  
3. 若同时使用 list/kanban 子视图，建议配置含 `name` 与图片，便于切换模式编辑。

**English**

1. The widget sets `readonly: false` on the child image field in `relatedFields` so binary data is not dropped on save.  
2. If the child has `name`, it must be writable so the file name is sent on create.  
3. If you also use list/kanban subviews, configure them with `name` and image for easier editing.

---

**协议 · License:** LGPL-3 · **作者 · Author:** mln
