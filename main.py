import os
import shutil
import sys
from pathlib import Path

# helpers
def sanity_check(cmd) -> bool:
	if shutil.which(cmd, mode=os.F_OK | os.X_OK, path=None) == None:
		print(f"Missing {cmd} or venv with {cmd}.")
		return False
	else:
		return True


# shorter to write
def _err():
	raise SystemExit(1)


# some platforms stuff
def user_cache_dir() -> Path:
	if sys.platform == "win32":
		base = (
			os.getenv("LOCALAPPDATA")
			or Path.home() / "AppData" / "Local"
		)
	elif sys.platform == "darwin":
		base = Path.home() / "Library" / "Caches"
	else:
		base = os.getenv("XDG_CACHE_HOME") or Path.home() / ".cache"
	return Path(base)


# early bail if ruff isn't in $PATH
# could add other tools here...
if sanity_check("ruff") == False:
	_err()

# consts/vars
cache_dir = user_cache_dir().as_posix()

# here you can define a "style" for your code-base.
# by default ruff uses a set from many linters/formatters.
# https://docs.astral.sh/ruff/default-rules/
# https://docs.astral.sh/ruff/settings/
# https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md

GEN_CONF = f"""
[tool.ruff]
# keep cache out of my project
cache-dir = "{cache_dir}/ruff"

# style
line-length = 80
indent-width = 8

[tool.ruff.format]
quote-style = "double"
indent-style = "tab"
"""

# all you then need to know is 2 commands:
# ruff check
# and optionally use --fix when safe.
# ruff format

CONF_PATH = Path("pyproject.toml")

if CONF_PATH.exists():
	print(f"{CONF_PATH} already exists.")
else:
	CONF_PATH.write_text(GEN_CONF.lstrip(), encoding="utf-8")
	print(f"Wrote {CONF_PATH}.")
