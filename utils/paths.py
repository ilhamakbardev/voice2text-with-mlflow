import os
import platform


def get_ffmpeg_path():
    base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ffmpeg")
    system = platform.system().lower()
    if system == "windows":
        return os.path.join(base, "windows", "ffmpeg.exe")
    elif system == "linux":
        return os.path.join(base, "linux", "ffmpeg")
    elif system == "darwin":
        return os.path.join(base, "macos", "ffmpeg")
    else:
        raise RuntimeError(f"Unsupported platform: {system}")
