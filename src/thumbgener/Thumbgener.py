from abc import ABC, abstractmethod
from pathlib import Path

from PIL import ImageFont


class Thumbgener(ABC):
    def __init__(self):
        self.width = 800
        self.height = 400
        self.font_size = 50
        self.font_file = "Ubuntu-Medium.ttf"
        self.font_margin = 50  # отступ от края
        self.line_padding = 10  # отступ между строками

    def wrap_text(self, text, font, max_px_width) -> list[str]:
        words = text.split(" ")
        lines, current = [], []
        for word in words:
            test_line = " ".join(current + [word])
            w = font.getlength(test_line)
            if w <= max_px_width:
                current.append(word)
            else:
                lines.append(" ".join(current))
                current = [word]
        if current:
            lines.append(" ".join(current))
        return lines

    def draw_text(self, title, draw) -> None:
        # 1. создаем шрифты
        dirname = Path(__file__).parent
        font = ImageFont.truetype(dirname / "fonts" / self.font_file, self.font_size)

        # 2. делим на строки с учетом ширины
        max_width = self.width - (self.font_margin * 2)
        lines = self.wrap_text(title, font, max_width)

        # 3. считаем сколько текст будет занимать в высоту
        ascent, descent = font.getmetrics()
        single_line_height = ascent + descent
        total_text_height = single_line_height * len(lines)  # сами строки
        total_text_height += self.line_padding * (len(lines) - 1)  # и отступы между

        # 4. рисуем строки
        current_y = (self.height - total_text_height) // 2
        for line in lines:
            line_width = font.getlength(line)
            line_x = (self.width - line_width) // 2
            draw.text((line_x, current_y), line, font=font, fill=(40, 40, 40))
            current_y += single_line_height + self.line_padding

    @abstractmethod
    def draw(self, title, filename) -> None: ...
