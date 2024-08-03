import logging
import os
from logging.handlers import TimedRotatingFileHandler

from rich.logging import RichHandler
from pathlib import Path

logger = logging.getLogger(__name__)

current_path = Path(".")
log_dir = current_path / 'logs'
log_fname = current_path / 'logs' / 'logger.log'

if not log_dir.exists():
    log_dir.mkdir(exist_ok=True)

# shell_handler = logging.StreamHandler()
shell_handler = RichHandler()
file_handler = TimedRotatingFileHandler(
    log_fname.as_posix().strip('.'),  when='midnight', backupCount=30)
file_handler.suffix = r'%Y-%m-%d.log'

logger.setLevel(logging.DEBUG)
shell_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)


# the formatter determines what our logs will look like
# fmt_shell = '%(levelname)s %(asctime)s %(message)s'
fmt_shell = '%(message)s'
fmt_file = '%(levelname)4s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s'

shell_formatter = logging.Formatter(fmt_shell)
file_formatter = logging.Formatter(fmt_file)

# here we hook everything together
shell_handler.setFormatter(shell_formatter)
file_handler.setFormatter(file_formatter)

logger.addHandler(shell_handler)
logger.addHandler(file_handler)