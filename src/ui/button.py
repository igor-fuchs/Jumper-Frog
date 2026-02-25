"""Button - a clickable UI element with hover feedback."""

from typing import Callable, Optional

import pygame

from src.core.settings import WHITE, DARK_GREEN, GREEN, LIGHT_GREEN, BLACK


class Button:
    """Rectangular button with text, hover highlight and click callback."""

    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        callback: Optional[Callable] = None,
        *,
        font_size: int = 28,
        color: tuple = DARK_GREEN,
        hover_color: tuple = GREEN,
        text_color: tuple = WHITE,
        border_radius: int = 12,
    ):
        self.rect = rect
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont("arial", font_size, bold=True)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.hovered = False

    # ------------------------------------------------------------------
    def handle_event(
        self, mouse_pos: tuple[int, int], mouse_clicked: bool
    ) -> None:
        """Update hover state and fire callback on click."""
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and mouse_clicked and self.callback:
            self.callback()

    # ------------------------------------------------------------------
    def draw(self, screen: pygame.Surface) -> None:
        """Render the button onto *screen*."""
        color = self.hover_color if self.hovered else self.color

        # Shadow
        shadow_rect = self.rect.move(3, 3)
        pygame.draw.rect(
            screen, BLACK, shadow_rect, border_radius=self.border_radius
        )

        # Body
        pygame.draw.rect(
            screen, color, self.rect, border_radius=self.border_radius
        )

        # Border
        border_color = LIGHT_GREEN if self.hovered else DARK_GREEN
        pygame.draw.rect(
            screen, border_color, self.rect,
            width=2, border_radius=self.border_radius,
        )

        # Text (centered)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
