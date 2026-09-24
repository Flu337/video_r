import cv2
import numpy as np
import math
from moviepy.editor import VideoFileClip

def process_frame(get_frame, t):
    frame = get_frame(t)
    h, w, _ = frame.shape

    # изменения цвета
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    hue_shift = int((t / 10.0) * 179) 
    hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift) % 180
    color_shifted = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

    # сжатие растягивания видео 
    scale_x = 1.0 + 0.35 * math.sin(t * 3)
    scale_y = 1.0 + 0.35 * math.cos(t * 3)

    new_w = max(1, int(w * scale_x))
    new_h = max(1, int(h * scale_y))

    resized = cv2.resize(color_shifted, (new_w, new_h))

    # центрирование
    canvas = np.zeros((h, w, 3), dtype=np.uint8)
    x_offset = (w - new_w) // 2
    y_offset = (h - new_h) // 2

    y1, y2 = max(0, y_offset), min(h, y_offset + new_h)
    x1, x2 = max(0, x_offset), min(w, x_offset + new_w)
    
    res_y1 = max(0, -y_offset)
    res_y2 = res_y1 + (y2 - y1)
    res_x1 = max(0, -x_offset)
    res_x2 = res_x1 + (x2 - x1)

    canvas[y1:y2, x1:x2] = resized[res_y1:res_y2, res_x1:res_x2]

    # изменение содержания
    if t > 4.0:
        cv2.rectangle(canvas, (40, 40), (320, 120), (255, 0, 0), -1)
        cv2.putText(canvas, "KT-3 DEMO", (60, 95), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
    if 7.0 < t < 9.5:
        canvas = 255 - canvas

    return canvas

def main():
    clip = VideoFileClip("input.mp4")
    # ограничение на 10секк
    duration = min(clip.duration, 15.0)
    sub = clip.subclip(0, duration)

    modified_clip = sub.fl(process_frame)
    modified_clip.write_videofile("output.mp4", fps=30, codec="libx264", audio_codec="aac")

if __name__ == '__main__':
    main()