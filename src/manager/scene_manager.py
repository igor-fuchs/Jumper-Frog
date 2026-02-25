"""SceneManager - controls scene transitions."""


class SceneManager:
    """Holds the active scene and provides a method to switch scenes."""

    def __init__(self):
        self.current_scene = None

    def switch(self, scene) -> None:
        """Replace the current scene with *scene*."""
        self.current_scene = scene

    # Delegate interface so GameLoop can call the scene transparently ------

    def handle_events(self, input_handler) -> None:
        if self.current_scene:
            self.current_scene.handle_events(input_handler)

    def update(self, dt: float) -> None:
        if self.current_scene:
            self.current_scene.update(dt)

    def render(self, screen) -> None:
        if self.current_scene:
            self.current_scene.render(screen)
