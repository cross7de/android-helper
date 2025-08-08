import sys
from ..constants import ctx

def log(msg: str, *, force: bool=False):
    if not ctx.quiet or force:
        print(msg)

def warn(msg: str):
    print(f"⚠️  {msg}", file=sys.stderr)

def err_fatal(msg: str, code: int = 2):
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(code)
