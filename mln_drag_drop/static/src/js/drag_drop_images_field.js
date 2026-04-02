/** @odoo-module **/

import { Component, useEffect, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { x2ManyCommands } from "@web/core/orm_service";
import { getDataURLFromFile, imageUrl, url } from "@web/core/utils/urls";
import { isBinarySize } from "@web/core/utils/binary";
import { download } from "@web/core/network/download";
import { useService } from "@web/core/utils/hooks";

const fileTypeMagicWordMap = {
    "/": "jpg",
    R: "gif",
    i: "png",
    P: "svg+xml",
    U: "webp",
};

/** Keys under options.extraData that are widget-only and must not be sent on create/write. */
const EXTRA_DATA_UI_KEYS = new Set([
    "previewImage",
    "cssStyles",
    "enable_zoom",
    "enableZoom",
]);

export class DragAndDropImagesField extends Component {
    static template = "mln_drag_drop.DragAndDropImagesField";
    static props = {
        ...standardFieldProps,
        childImageField: { type: String, optional: true },
        acceptedFileExtensions: { type: String, optional: true },
        previewImage: { type: String, optional: true },
        enableZoom: { type: Boolean, optional: true },
        cssStyles: { type: String, optional: true },
        extraData: { type: Object, optional: true },
    };
    static defaultProps = {
        childImageField: "image_1920",
        acceptedFileExtensions: "image/*",
        previewImage: undefined,
        enableZoom: false,
        cssStyles: "",
        extraData: {},
    };

    setup() {
        this.state = useState({ dragging: false, lightbox: null });
        this.notification = useService("notification");
        useEffect(
            () => {
                if (!this.state.lightbox) {
                    return () => {};
                }
                const onKey = (ev) => {
                    if (ev.key === "Escape") {
                        this.closeLightbox();
                    }
                };
                window.addEventListener("keydown", onKey);
                return () => window.removeEventListener("keydown", onKey);
            },
            () => [this.state.lightbox]
        );
    }

    get records() {
        return this.props.record.data[this.props.name]?.records || [];
    }

    getLineCaption(line) {
        const n = line.data.name;
        if (n && String(n).trim()) {
            return String(n).trim();
        }
        const dn = line.data.display_name;
        if (dn && String(dn).trim()) {
            return String(dn).trim();
        }
        return _t("Image");
    }

    getDownloadFilename(line) {
        let base = this.getLineCaption(line);
        if (!/\.(png|jpe?g|gif|webp|bmp|svg)$/i.test(base)) {
            base += ".png";
        }
        return base.replace(/[/\\?%*:|"<>]/g, "_");
    }

    getDownloadUrl(line) {
        const id = line.resId;
        if (!id) {
            return null;
        }
        const lineModel = line.resModel || this.props.record.data[this.props.name]?.resModel;
        const fieldName = this.props.childImageField;
        const fname = encodeURIComponent(this.getDownloadFilename(line));
        const route = `/web/image/${lineModel}/${id}/${fieldName}/${fname}`;
        return url(route, {
            download: true,
            unique: line.data.write_date || this.props.record.data.write_date,
        });
    }

    onDownloadLine(line) {
        const href = line.resId
            ? this.getDownloadUrl(line)
            : this.getPreviewSrc(line);
        if (!href || href.includes("placeholder")) {
            return;
        }
        const fname = this.getDownloadFilename(line);
        const a = document.createElement("a");
        a.href = href;
        a.download = fname;
        a.rel = "noopener noreferrer";
        document.body.appendChild(a);
        a.click();
        a.remove();
    }

    onBatchZipKeydown(ev) {
        if (ev.key === "Enter" || ev.key === " ") {
            ev.preventDefault();
            this.onDownloadAllZip();
        }
    }

    async onDownloadAllZip() {
        const saved = this.records.filter((line) => line.resId);
        if (!saved.length) {
            this.notification.add(
                _t("Save the form first: batch ZIP needs database ids for each image row."),
                { type: "warning" }
            );
            return;
        }
        const lineModel =
            saved[0].resModel || this.props.record.data[this.props.name]?.resModel;
        const line_ids = JSON.stringify(saved.map((line) => line.resId));
        try {
            await download({
                url: "/mln_drag_drop/gallery_images_zip",
                data: {
                    model: lineModel,
                    field: this.props.childImageField,
                    line_ids,
                },
            });
        } catch {
            this.notification.add(_t("Could not build the ZIP file."), { type: "danger" });
        }
    }

    get tileStyle() {
        return this.props.cssStyles || "width:150px; height:150px; object-fit:cover;";
    }

    getPreviewSrc(line) {
        const fieldName = this.props.previewImage || this.props.childImageField;
        const value = line.data[fieldName] || line.data[this.props.childImageField];
        if (!value) {
            return "/web/static/img/placeholder.png";
        }
        const lineModel = line.resModel || this.props.record.data[this.props.name]?.resModel;
        if (isBinarySize(value) && line.resId) {
            return imageUrl(lineModel, line.resId, fieldName, {
                unique: line.data.write_date || this.props.record.data.write_date,
            });
        }
        const magic = fileTypeMagicWordMap[value[0]] || "png";
        return `data:image/${magic};base64,${value}`;
    }

    isPlaceholderPreview(line) {
        const src = this.getPreviewSrc(line);
        return !src || src.includes("placeholder");
    }

    getPreviewTitle(line) {
        return this.isPlaceholderPreview(line) ? "" : _t("Click to enlarge");
    }

    openLightbox(line) {
        if (this.isPlaceholderPreview(line)) {
            return;
        }
        this.state.lightbox = {
            src: this.getPreviewSrc(line),
            title: this.getLineCaption(line),
        };
    }

    closeLightbox() {
        this.state.lightbox = null;
    }

    onLightboxBackdropClick(ev) {
        if (ev.target === ev.currentTarget) {
            this.closeLightbox();
        }
    }

    onLightboxCloseKeydown(ev) {
        if (ev.key === "Enter" || ev.key === " ") {
            ev.preventDefault();
            this.closeLightbox();
        }
    }

    async _createRecordFromFile(file) {
        const dataUrl = await getDataURLFromFile(file);
        const base64 = dataUrl.split(",")[1];
        const vals = {
            ...this.props.extraData,
            [this.props.childImageField]: base64,
        };
        const baseName = (file.name || "").replace(/^.*[/\\]/, "").trim();
        vals.name = baseName || (vals.name && String(vals.name).trim()) || _t("Image");
        await this.props.record.update({
            [this.props.name]: [x2ManyCommands.create(false, vals)],
        });
    }

    async onInputChange(ev) {
        const files = Array.from(ev.target.files || []);
        for (const file of files) {
            await this._createRecordFromFile(file);
        }
        ev.target.value = "";
    }

    onDragOver(ev) {
        ev.preventDefault();
        this.state.dragging = true;
    }

    onDragLeave() {
        this.state.dragging = false;
    }

    async onDrop(ev) {
        ev.preventDefault();
        this.state.dragging = false;
        const files = Array.from(ev.dataTransfer?.files || []);
        for (const file of files) {
            await this._createRecordFromFile(file);
        }
    }

    async removeItem(line) {
        const id = line.resId || line._virtualId;
        if (!id) {
            return;
        }
        await this.props.record.update({
            [this.props.name]: [x2ManyCommands.delete(id)],
        });
    }

    onRemoveKeydown(ev, line) {
        if (ev.key === "Enter" || ev.key === " ") {
            ev.preventDefault();
            this.removeItem(line);
        }
    }

    onDownloadKeydown(ev, line) {
        if (ev.key === "Enter" || ev.key === " ") {
            ev.preventDefault();
            this.onDownloadLine(line);
        }
    }

    onPreviewImgKeydown(ev, line) {
        if (ev.key === "Enter" || ev.key === " ") {
            ev.preventDefault();
            this.openLightbox(line);
        }
    }
}

function buildRelatedFields(fieldInfo) {
    const options = fieldInfo.options || {};
    const extraData = options.extraData || {};
    const childImageField = options.childImageField || "image_1920";
    const previewImage = extraData.previewImage || options.previewImage;
    const fields = [
        { name: "display_name", type: "char" },
        // Must be writable: Odoo sets relatedFields without readonly to readonly=true, so
        // fromUnityToServerValues drops "name" on create/write and the server keeps default "Image".
        { name: "name", type: "char", readonly: false },
        { name: "write_date", type: "datetime" },
        // Odoo marks nested x2many sub-fields readonly unless explicitly false; otherwise
        // fromUnityToServerValues drops them on save and binary never reaches the server.
        { name: childImageField, type: "binary", readonly: false },
    ];
    if (previewImage && previewImage !== childImageField) {
        fields.push({ name: previewImage, type: "binary", readonly: false });
    }
    return fields;
}

export const dragDropImagesField = {
    component: DragAndDropImagesField,
    displayName: _t("Drag and Drop Images"),
    supportedTypes: ["one2many"],
    relatedFields: buildRelatedFields,
    isEmpty: () => false,
    extractProps: ({ options }) => {
        const rawExtra = options.extraData || {};
        const extraData = Object.fromEntries(
            Object.entries(rawExtra).filter(([k]) => !EXTRA_DATA_UI_KEYS.has(k))
        );
        return {
            childImageField: options.childImageField || "image_1920",
            acceptedFileExtensions:
                options.acceptedFileExtensions || options.accepted_file_extensions || "image/*",
            previewImage: rawExtra.previewImage || options.previewImage,
            enableZoom: Boolean(
                rawExtra.enable_zoom || options.enableZoom || options.enable_zoom
            ),
            cssStyles: rawExtra.cssStyles || "",
            extraData,
        };
    },
};

registry.category("fields").add("drag_drop_images", dragDropImagesField);
