# mln Drag Drop Gallery (Odoo 18)

**Technical name:** `mln_drag_drop`  
**Widget:** `drag_drop_images`

## Overview

Backend **one2many** image gallery widget: **batch upload** (drag-and-drop or multi-select files), **click thumbnail for lightbox preview**, **per-image download**, and **ZIP download** for lines already saved in the database.

---

## Features

| Feature | Description |
|---------|-------------|
| Batch upload | Drop many files or multi-select; one child row per image. |
| Preview | Click thumbnail → overlay; Esc, backdrop, or close control. |
| Download | Per-tile control; *Download all (ZIP)* only for persisted rows (save parent first). |
| Captions | If the child model has Char `name`, the original file name is stored. |
| Demo | Menu **mln Drag Drop → Demo**. |

---

## Installation

1. Add `mln_drag_drop` to your addons path.  
2. Update the Apps list.  
3. Install **mln Drag Drop Gallery**.

---

## Built-in demo

| Item | Value |
|------|--------|
| Menu | **mln Drag Drop → Demo** (`base.group_user`) |
| Models | `mln_drag_drop.demo`, `mln_drag_drop.demo.line` |
| Sample data | `data/mln_drag_drop_demo_data.xml` |

---

## View usage

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

### Options

- `childImageField`: child image field (default `image_1920`).  
- `acceptedFileExtensions`: default `image/*`.  
- `extraData`: defaults for new lines. `previewImage`, `cssStyles`, `enable_zoom` / `enableZoom` are **UI-only**; other keys are passed as field defaults.  
- Lightbox and single download are always available; ZIP requires saved child rows.

---

## Integration notes

1. The widget sets `readonly: false` on the child image field in `relatedFields` so binary data is not dropped on save.  
2. If the child has `name`, it must be writable so the file name is sent on create.  
3. If you also use list/kanban subviews, configure them with `name` and image for easier editing.

---

**License:** LGPL-3 · **Author:** mln
