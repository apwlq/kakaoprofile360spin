import cv2
import numpy as np
from PIL import Image

# 설정
duration_sec = 6
fps = 60
total_frames = duration_sec * fps

# 이미지 불러오기
background = Image.open("background.png").convert("RGBA")
fg_original = Image.open("foreground.png").convert("RGBA")

# 크기 설정
bg_w, bg_h = background.size
scale = 0.6
fg_w, fg_h = int(bg_w * scale), int(bg_h * scale)
foreground = fg_original.resize((fg_w, fg_h), Image.Resampling.LANCZOS)

# 비디오 설정
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (bg_w, bg_h))

# 프레임 생성
for i in range(total_frames):
    angle = -360 * (i / total_frames)

    # 배경 크기의 투명 캔버스에 전경 중앙 배치
    canvas = Image.new("RGBA", (bg_w, bg_h), (0, 0, 0, 0))
    offset_x = (bg_w - fg_w) // 2
    offset_y = (bg_h - fg_h) // 2
    canvas.paste(foreground, (offset_x, offset_y), foreground)

    # 배경 크기 캔버스 자체를 중심 기준으로 회전
    rotated_canvas = canvas.rotate(angle, resample=Image.BICUBIC, center=(bg_w // 2, bg_h // 2))

    # 배경과 합성
    combined = Image.alpha_composite(background, rotated_canvas)
    frame = cv2.cvtColor(np.array(combined.convert("RGB")), cv2.COLOR_RGB2BGR)
    out.write(frame)

out.release()
