"""HotReloader - watches source files and reloads modules on change.

Uses the ``watchdog`` library to monitor the ``src/`` directory for
``.py`` file modifications.  When a change is detected, every
previously imported ``src.*`` module is reloaded via
:func:`importlib.reload`, and the active scene is re-instantiated so
that the player immediately sees the updated behaviour without
restarting the game.

Usage inside the game loop
--------------------------
1. Create a ``HotReloader`` and call :meth:`start` once.
2. Each frame, call :meth:`check` — if files changed, it performs the
   reload and returns ``True`` so the caller can take any extra action.
3. Call :meth:`stop` when the game shuts down to clean up the observer
   thread.

Design notes
------------
* The reloader is **development-only** tooling.  It can be disabled in
  production by simply not instantiating it.
* Re-instantiation of the current scene is done through the
  ``SceneManager`` so existing architecture is respected.
* A small cooldown prevents multiple rapid reloads when editors write
  temporary files before the final save.
"""

import importlib
import sys
import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent


# Cooldown (seconds) to collapse rapid sequential changes into one reload.
_RELOAD_COOLDOWN = 0.5


class _SourceChangeHandler(FileSystemEventHandler):
    """Flags that a ``.py`` source file was modified."""

    def __init__(self):
        super().__init__()
        self.changed = False

    def on_modified(self, event: FileModifiedEvent) -> None:
        """Set the changed flag when a Python file is written."""
        if not event.is_directory and event.src_path.endswith(".py"):
            self.changed = True


class HotReloader:
    """Watches ``src/`` for changes and reloads modules at runtime.

    Parameters
    ----------
    scene_manager : SceneManager
        The scene manager whose current scene will be re-created after a
        reload so the player sees updated code immediately.
    watch_path : str, optional
        Directory to monitor.  Defaults to ``src/`` relative to the
        project root.
    """

    def __init__(self, scene_manager, watch_path: str | None = None):
        self.scene_manager = scene_manager

        # Resolve the directory to watch (default: <project>/src)
        if watch_path is None:
            # hot_reloader.py lives at src/core/, so go up two levels
            project_root = Path(__file__).resolve().parent.parent.parent
            watch_path = str(project_root / "src")

        self._watch_path = watch_path
        self._handler = _SourceChangeHandler()
        self._observer = Observer()
        self._last_reload: float = 0.0

    # ── Lifecycle ────────────────────────────────────────────────────

    def start(self) -> None:
        """Begin watching for file changes in a background thread."""
        self._observer.schedule(
            self._handler, self._watch_path, recursive=True,
        )
        self._observer.daemon = True
        self._observer.start()
        print(f"[HotReload] Watching {self._watch_path} for changes …")

    def stop(self) -> None:
        """Stop the file-system observer thread."""
        self._observer.stop()
        self._observer.join(timeout=2)
        print("[HotReload] Stopped.")

    # ── Per-frame check ──────────────────────────────────────────────

    def check(self) -> bool:
        """Check whether source files changed since the last frame.

        If a change is detected (and the cooldown has elapsed), all
        ``src.*`` modules are reloaded and the current scene is
        re-instantiated through the scene manager.

        Returns
        -------
        bool
            ``True`` if a reload was performed this frame.
        """
        if not self._handler.changed:
            return False

        # Enforce cooldown so rapid saves don't trigger multiple reloads
        now = time.time()
        if now - self._last_reload < _RELOAD_COOLDOWN:
            return False

        self._handler.changed = False
        self._last_reload = now

        self._reload_modules()
        self._rebuild_scene()
        return True

    # ── Internal helpers ─────────────────────────────────────────────

    @staticmethod
    def _reload_modules() -> None:
        """Reload every imported ``src.*`` module.

        Modules are sorted so that leaf modules (deeper paths) are
        reloaded before their parents, which avoids stale references.
        """
        src_modules = sorted(
            [name for name in sys.modules if name.startswith("src")],
            key=lambda n: n.count("."),
            reverse=True,
        )
        for mod_name in src_modules:
            module = sys.modules.get(mod_name)
            if module is None:
                continue
            try:
                importlib.reload(module)
            except Exception as exc:  # pylint: disable=broad-except
                print(f"[HotReload] Failed to reload {mod_name}: {exc}")

        print(f"[HotReload] Reloaded {len(src_modules)} module(s).")

    def _rebuild_scene(self) -> None:
        """Re-instantiate the current scene so it picks up reloaded code.

        The new scene class is fetched from the *reloaded* module to
        ensure updated ``__init__`` / ``render`` / etc. methods are used.
        """
        current = self.scene_manager.current_scene
        if current is None:
            return

        # Get the class from the freshly-reloaded module
        scene_class_name = type(current).__name__
        module_name = type(current).__module__
        reloaded_module = sys.modules.get(module_name)

        if reloaded_module is None:
            print("[HotReload] Could not find reloaded module for scene.")
            return

        new_class = getattr(reloaded_module, scene_class_name, None)
        if new_class is None:
            print(
                f"[HotReload] Class {scene_class_name} not found in "
                f"{module_name} after reload."
            )
            return

        # Create a new instance of the scene with the same manager
        try:
            new_scene = new_class(self.scene_manager)
            self.scene_manager.switch(new_scene)
            print(f"[HotReload] Scene rebuilt: {scene_class_name}")
        except Exception as exc:  # pylint: disable=broad-except
            print(f"[HotReload] Failed to rebuild scene: {exc}")
