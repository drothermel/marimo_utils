"""Inline dr_widget runtime script for plain-HTML hosts."""

from __future__ import annotations

from pathlib import Path


def _read_runtime_bundle() -> str:
    try:
        import dr_widget  # noqa: PLC0415
    except ImportError as exc:
        msg = "dr-widget is required to build plain-HTML pages with the runtime."
        raise ImportError(msg) from exc

    bundle_path = (
        Path(dr_widget.__file__).resolve().parent / "bundled/runtime/static/runtime.js"
    )
    if not bundle_path.is_file():
        msg = (
            f"Runtime bundle not found at {bundle_path}. "
            "Run `bun run build:runtime` in dr_widget first."
        )
        raise FileNotFoundError(msg)

    runtime_js = bundle_path.read_text(encoding="utf-8")
    if "</script>" in runtime_js.lower():
        msg = "Runtime bundle contains '</script>' and cannot be inlined safely."
        raise ValueError(msg)
    return runtime_js


_RUNTIME_GUARD_START = (
    "(function(){if(window.__drRuntimeLoaded)return;window.__drRuntimeLoaded=true;\n"
)
_RUNTIME_GUARD_END = "\n})();"


def runtime_script_tag() -> str:
    """Return a guarded inline ``<script>`` that registers ``<dr-*>`` elements."""
    runtime_js = _read_runtime_bundle()
    script = f"{_RUNTIME_GUARD_START}{runtime_js}{_RUNTIME_GUARD_END}"
    return f"<script>{script}</script>"
