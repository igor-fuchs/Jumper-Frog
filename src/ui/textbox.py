"""TextBox - a simple static text label area."""

import pygame

from src.core.settings import WHITE, DARK_GRAY, LIGHT_GRAY


class TextBox:
    """Non-interactive text box rendered at a given position."""

    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        *,
        font_size: int = 18,
        text_color: tuple = WHITE,
        bg_color: tuple = DARK_GRAY,
        border_color: tuple = LIGHT_GRAY,
        border_radius: int = 8,
    ):
        self.rect = rect
        self.text = text
        self.font = pygame.font.SysFont("arial", font_size)
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_radius = border_radius

    def draw(self, screen: pygame.Surface) -> None:
        """Render the text box onto *screen*."""
        # Background
        pygame.draw.rect(
            screen, self.bg_color, self.rect,
            border_radius=self.border_radius,
        )
        # Border
        pygame.draw.rect(
            screen, self.border_color, self.rect,
            width=1, border_radius=self.border_radius,
        )
        # Text (centered)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
