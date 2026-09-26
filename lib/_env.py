"""Internal helper to load .env when python-dotenv is available."""
from __future__ import annotations
from pathlib import Path

_ENV_LOADED = False
_LOADED_PATHS: list[str] = []


def env_candidates() -> list[Path]:
    out: list[Path] = []
    try:
        from dotenv import find_dotenv
        found = find_dotenv(usecwd=True)
        if found:
            out.append(Path(found))
    except ImportError:
        cur = Path.cwd()
        for d in [cur, *cur.parents]:
            if (d / ".env").is_file():
                out.append(d / ".env")
                break
    root = Path(__file__).resolve().parents[1] / ".env"
    if root not in out:
        out.append(root)
    return out


def loaded_env_paths() -> list[str]:
    return list(_LOADED_PATHS)


def load_env(force: bool = False) -> None:
    global _ENV_LOADED
    if _ENV_LOADED and not force:
        return

    try:
        from dotenv import find_dotenv, load_dotenv
        dotenv_path = find_dotenv(usecwd=True)
        if dotenv_path:
            load_dotenv(dotenv_path)
            _LOADED_PATHS.append(dotenv_path)

        repo_env = Path(__file__).resolve().parents[1] / ".env"
        if repo_env.is_file():
            load_dotenv(repo_env)
            _LOADED_PATHS.append(str(repo_env))
    except ImportError:
        pass

    _ENV_LOADED = True
