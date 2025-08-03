#!/usr/bin/env python3
"""
PDF Text Attacker - Attack on AI-generated text detectors

Creates PDFs where text appears normal visually but gets copied/extracted 
in attacked order to increase perplexity and fool AI detectors.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import random
import os


class PDFAttacker:
    def __init__(self, page_size=letter, font_size=12):
        self.page_size = page_size
        self.font_size = font_size
        self.char_width = font_size * 0.6  # Exact character width for monospace
        self.line_height = font_size * 1.2  # Line spacing
        self.margin = margin

    def create_normal_pdf(self, text: str, output_path: str):
        """Create PDF with normal text ordering"""
        c = canvas.Canvas(output_path, pagesize=self.page_size)
        c.setFont("Courier", self.font_size)  # Monospace font

        # Character-based layout, fill entire width
        y_pos = self.page_size[1] - self.margin
        line_width = int((self.page_size[0] - 2 * self.margin) / self.char_width)

        # Remove line breaks and split into characters
        clean_text = " ".join(text.split())

        # Draw text character by character, filling entire width
        for i in range(0, len(clean_text), line_width):
            line = clean_text[i : i + line_width]
            c.drawString(self.margin, y_pos, line)
            y_pos -= self.line_height

        c.save()
        print(f"Normal PDF saved: {output_path}")
        
    def create_attacked_pdf(self, text: str, output_path: str, attack_factor=0.7):
        """
        Create PDF where characters are positioned to appear normal visually
        but get copied in attacked order when text is selected
        """
        c = canvas.Canvas(output_path, pagesize=self.page_size)
        c.setFont("Courier", self.font_size)  # Monospace font

        y_pos = self.page_size[1] - self.margin
        line_width = int((self.page_size[0] - 2 * self.margin) / self.char_width)

        # Remove line breaks and split into characters
        clean_text = " ".join(text.split())

        # Calculate character positions to match normal layout exactly
        char_positions = []
        for i, char in enumerate(clean_text):
            line_num = i // line_width
            char_pos_in_line = i % line_width
            x_pos = self.margin + (char_pos_in_line * self.char_width)
            y_pos_line = self.page_size[1] - self.margin - (line_num * self.line_height)
            char_positions.append((x_pos, y_pos_line, char))
        
        # Create attacked drawing order
        drawing_order = list(range(len(char_positions)))
        
        # Attack the order based on attack_factor
        num_to_attack = int(len(drawing_order) * attack_factor)
        indices_to_attack = random.sample(range(len(drawing_order)), num_to_attack)
        
        # Shuffle the selected indices
        attacked_values = [drawing_order[i] for i in indices_to_attack]
        random.shuffle(attacked_values)
        
        for i, new_val in zip(indices_to_attack, attacked_values):
            drawing_order[i] = new_val
            
        # Draw characters in attacked order
        for idx in drawing_order:
            x, y, char = char_positions[idx]
            c.drawString(x, y, char)

        c.save()
        print(f"Attacked PDF saved: {output_path}")


def main():
    # Sample AI-generated text (you can replace with actual AI text)
    ai_text = """
    The rapid advancement of artificial intelligence has transformed numerous industries 
    and revolutionized the way we approach complex problems. Machine learning algorithms 
    have demonstrated remarkable capabilities in pattern recognition, data analysis, 
    and predictive modeling. These technological innovations continue to push the 
    boundaries of what was previously thought impossible, enabling automation and 
    efficiency improvements across various sectors. As we move forward, the integration 
    of AI systems into our daily lives becomes increasingly prevalent and sophisticated.
    """

    # Clean up the text
    ai_text = " ".join(ai_text.split())
    
    attacker = PDFAttacker()
    
    # Create output directory
    os.makedirs("./tmp", exist_ok=True)
    
    # Generate different versions
    attacker.create_normal_pdf(ai_text, "./tmp/normal.pdf")
    
    # Set random seed for reproducible attacking
    random.seed(42)
    attacker.create_attacked_pdf(ai_text, "./tmp/attacked.pdf")


if __name__ == "__main__":
    main()
