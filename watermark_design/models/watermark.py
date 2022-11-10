import io
import base64
import logging
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from PyPDF2 import PdfFileWriter, PdfFileReader
from odoo import fields, models
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import os
from .config import FLAGS

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def binary_content(self, *args, **kwargs):
        """附件上传时候不添加水印，只有下载时候添加"""
        status, headers, content = super(IrHttp, self).binary_content(*args, **kwargs)
        content_type = dict(headers).get('Content-Type')
        download = kwargs.get('download')

        # 给PDF添加水印
        if content_type == 'application/pdf' and download == 'true':
            content = self.add_watermark(base64.b64decode(content))
            content = base64.b64encode(content)

        # 给图片添加水印
        if content_type in ['image/png', 'image/jpeg'] and download == 'true':
            stream = self.image_add_watermark(base64.b64decode(content))
            content = base64.b64encode(stream)
        return status, headers, content

    def _generate_watermark(self):
        """
        pdf生成水印
        :return:
        """
        # 水印文件临时存储路径
        filename = f'watermark.pdf'
        design_id = self.env['watermark.design.order'].search([('create_uid', '=', self.env.user.id)],
                                                              limit=1, order='create_date DESC')
        font_txt = f'{self.env.user.name} {self.env.company.name} {fields.Date.context_today(self)}'
        font_color = '#d21717'
        font_size = 30
        if design_id:
            font_size = design_id.font_size
            font_txt = f'%s' % design_id.name
            font_color = '%s' % design_id.colorpicker
            if design_id.show_date:
                font_txt = f'%s %s' % (font_txt, fields.Date.context_today(self))
        watermark = font_txt
        # 获取画布并修改原点坐标
        c = canvas.Canvas(filename)
        # translate设置水印起始位置：translate(x, y)：x约小越 y越大约上
        c.translate(-10 * cm, 8 * cm)
        try:
            font_name = 'SimSun'
            # 从系统路径中引入中文字体(新宋)
            f_name = 'SimSun.ttf'
            font_path = os.path.join(FLAGS.model_dir, f_name)
            pdfmetrics.registerFont(ttfonts.TTFont(font_name, font_path))
        except Exception as e:
            # 默认字体，不支持中文
            font_name = 'Helvetica'
            _logger.error(f'Register Font Error: {e}')
        # 设置字体及大小，旋转 -20 度并设置颜色和透明度
        c.setFont(font_name, font_size)

        # 旋转角度
        c.rotate(-20)
        # 设置填充颜色
        c.setFillColor(font_color, 0.30)
        # 平铺写入水印，(0, 30, 15) 其中15是指的文字字间距
        for i in range(0, 30, 15):
            for j in range(0, 30, 5):
                c.drawString(i * cm, j * cm, watermark)
        c.save()
        return filename

    def add_watermark(self, content):
        """
        PDF添加水印功能
        :param content:
        :return:
        """
        watermark = self._generate_watermark()
        pdf_input = PdfFileReader(io.BytesIO(content), strict=False)
        watermark = PdfFileReader(open(watermark, "rb"), strict=False)
        pdf_output = PdfFileWriter()
        page_count = pdf_input.getNumPages()
        for page_number in range(page_count):
            input_page = pdf_input.getPage(page_number)
            input_page.mergePage(watermark.getPage(0))
            pdf_output.addPage(input_page)
        stream = io.BytesIO()
        pdf_output.write(stream)
        data = stream.getvalue()
        return data

    def image_add_watermark(self, content):
        """
        给图片添加水印
        :param content:
        :return:
        """
        # 水印内容 和 字体
        design_id = self.env['watermark.design.order'].search(
            [('create_uid', '=', self.env.user.id)], limit=1, order='create_date DESC')
        font_txt = f'{self.env.user.name} {self.env.company.name} {fields.Date.context_today(self)}'
        font_color = '#d21717'
        font_size = 20
        if design_id:
            font_size = design_id.font_size
            font_txt = f'%s' % design_id.name
            font_color = '%s' % design_id.colorpicker
            if design_id.show_date:
                font_txt = f'%s %s' % (font_txt, fields.Date.context_today(self))
        image_name = 'SimSun.ttf'
        font_path = os.path.join(FLAGS.model_dir, image_name)
        font = ImageFont.truetype(font_path, font_size)
        # 二进制流图片内容
        image = Image.open(BytesIO(content)).convert('RGBA')
        # 添加背景
        new_img = Image.new('RGBA', (image.size[0] * 3, image.size[1] * 3), (0, 0, 0, 0))
        new_img.paste(image, image.size)

        # 添加水印
        font_len = len(font_txt)
        rgba_image = new_img.convert('RGBA')
        text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
        image_draw = ImageDraw.Draw(text_overlay)
        for i in range(0, rgba_image.size[0], font_len * 15 + 150):
            for j in range(0, rgba_image.size[1], 100):
                # draw.text #设置文字位置/内容/颜色/字体
                image_draw.text((i, j), font_txt, font_color, font=font)
        text_overlay = text_overlay.rotate(-20)
        # 合并原图与文字图片
        out = Image.alpha_composite(rgba_image, text_overlay)
        # 裁切图片
        out = out.crop((image.size[0], image.size[1], image.size[0] * 2, image.size[1] * 2))
        out = out.convert('RGB')
        stream = io.BytesIO()
        out.save(stream, format="PNG")
        data = stream.getvalue()
        return data
