import base64
import platform
from io import BytesIO
import cpuinfo
from PIL import Image, ImageDraw, ImageFont
from plugins.KawaiiDashboard.tool.sysinfo import get_status_info
from plugins.KawaiiDashboard.tool.utils import truncate_string
from plugins.KawaiiDashboard.tool.color import (
    cpu_color,
    ram_color,
    disk_color,
    swap_color,
    details_color,
    nickname_color,
    transparent_color,
)
from plugins.KawaiiDashboard.tool.path import (
    bg_img_path,
    adlam_font_path,
    baotu_font_path,
    marker_img_path,
    spicy_font_path,
    dingtalk_font_path,
)


system = platform.uname()

adlam_fnt = ImageFont.truetype(str(adlam_font_path), 36)
spicy_fnt = ImageFont.truetype(str(spicy_font_path), 38)
baotu_fnt = ImageFont.truetype(str(baotu_font_path), 64)
dingtalk_fnt = ImageFont.truetype(str(dingtalk_font_path), 38)


def draw(ap , nickname,runtime):
    """绘图"""
    LangBot_version = ap.ver_mgr.get_current_version()
    plugin_num = len(ap.plugin_mgr.plugins())
    with Image.open(bg_img_path).convert("RGBA") as base:
        img = Image.new("RGBA", base.size, (0, 0, 0, 0))
        marker = Image.open(marker_img_path).convert("RGBA")  # QQ头像

        # 创建圆形蒙版
        mask = Image.new("L", marker.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, marker.size[0], marker.size[1]), fill=255)

        cpu, ram, swap, disk = get_status_info()

        cpu_info = f"{cpu.usage}% - {cpu.freq}Ghz [{cpu.core} core]"
        ram_info = f"{ram.usage} / {ram.total} GB"
        swap_info = f"{swap.usage} / {swap.total} GB"
        disk_info = f"{disk.usage} / {disk.total} GB"

        content = ImageDraw.Draw(img)
        content.text((251, 581), nickname, font=baotu_fnt, fill=nickname_color)
        content.text((251, 772), cpu_info, font=spicy_fnt, fill=cpu_color)
        content.text((251, 927), ram_info, font=spicy_fnt, fill=ram_color)
        content.text((251, 1081), swap_info, font=spicy_fnt, fill=swap_color)
        content.text((251, 1235), disk_info, font=spicy_fnt, fill=disk_color)

        content.arc(
            (103, 724, 217, 838),
            start=-90,
            end=(cpu.usage * 3.6 - 90),
            width=115,
            fill=cpu_color,
        )
        content.arc(
            (103, 878, 217, 992),
            start=-90,
            end=(ram.usage / ram.total * 360 - 90),
            width=115,
            fill=ram_color,
        )
        if swap.total > 0:
            content.arc(
                (103, 1032, 217, 1146),
                start=-90,
                end=(swap.usage / swap.total * 360 - 90),
                width=115,
                fill=swap_color,
            )
        content.arc(
            (103, 1186, 217, 1300),
            start=-90,
            end=(disk.usage / disk.total * 360 - 90),
            width=115,
            fill=disk_color,
        )

        content.ellipse((108, 729, 212, 833), width=105, fill=transparent_color)
        content.ellipse((108, 883, 212, 987), width=105, fill=transparent_color)
        content.ellipse((108, 1037, 212, 1141), width=105, fill=transparent_color)
        content.ellipse((108, 1192, 212, 1295), width=105, fill=transparent_color)

        content.text(
            (352, 1378),
            f"{truncate_string(cpuinfo.get_cpu_info()['brand_raw'])}",
            font=adlam_fnt,
            fill=details_color,
        )
        content.text(
            (352, 1431),
            f"{truncate_string(system.system + ' ' + system.release)}",
            font=adlam_fnt,
            fill=details_color,
        )
        content.text(
            (352, 1484),
            f"LoneBot {LangBot_version}",
            font=adlam_fnt,
            fill=details_color,
        )
        content.text(
            (352, 1537),
            f"{plugin_num} loaded",
            font=adlam_fnt,
            fill=details_color,
        )
        content.text(
            (730, 1663),
            f'已运行{runtime}小时...',
            font=dingtalk_fnt,
            fill=details_color,
            anchor="ra",
        )

        nickname_length = baotu_fnt.getlength(nickname)
        # 使用圆形蒙版将marker图片粘贴到img上
        img.paste(marker, (110, 580), mask=mask)

        out = Image.alpha_composite(base, img)

        byte_io = BytesIO()
        out.save(byte_io, format="png")
        img_bytes = byte_io.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        # with open('plugins/KawaiiDashboard/tool/resources/images/temp.png', 'wb') as f:
        #     f.write(img_bytes)
        return img_base64



