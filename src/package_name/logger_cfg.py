import os
import sys
from pathlib import Path
from loguru import logger
from . import LOG_FILEPATH, DEBUG


def setup_logger():
    """Configuration unique, belle en dev et pro en production."""
    logger.remove()  # On enlève le handler par défaut moche

    # ── 1. Niveaux avec icônes emoji (le côté "geek sublime") ──
    custom_levels = [
        ("TRACE",   "<cyan>",    "[..]"),
        ("DEBUG",   "<white>",    "[dbg]"),
        ("INFO",    "<blue>",   "[i]"),
        ("SUCCESS", "<green>",   "[+]"),
        ("WARNING", "<yellow>",  "[!]"),
        ("ERROR",   "<red>",     "[x]"),
        ("CRITICAL","<red>",     "[X]"),
    ]
    for name, color, icon in custom_levels:
        logger.level(name, color=color, icon=icon)

    log_level = "INFO" if DEBUG else "DEBUG"

    # ── 3. Console sublime (toujours présente) ──
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> - "
        "<level>{level.icon} {level.name: <8}</level> - "
        # "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "{message}"
    )

    logger.add(
        sys.stderr,
        level=log_level,
        format=console_format,
        colorize=True,           # couleurs auto si terminal
        backtrace=True,
        diagnose=DEBUG,          # variables dans traceback → seulement en dev
        enqueue=True,            # thread / multiprocessing safe
    )

    # ── 4. Fichier de logs ──
    log_dir = Path(LOG_FILEPATH)
    os.makedirs(log_dir, exist_ok=True)

    if not DEBUG:
        # Production → JSON pur (parfait pour Loki, ELK, Datadog, etc.)
        logger.add(
            str(log_dir / "app_{time:YYYY-MM-DD}.jsonl"),
            level=log_level,
            format="{message}",          # ← important : JSON brut
            serialize=True,              # structure complète (extra, exception, etc.)
            rotation="500 MB",
            retention="30 days",
            compression="zip",
            enqueue=True,
            backtrace=True,
            diagnose=False,
        )
    else:
        # Développement → fichier texte lisible + console
        logger.add(
            str(log_dir / "app_{time:YYYY-MM-DD}.log"),
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level.name: <8} | {name}:{function}:{line} | {message}",
            rotation="100 MB",
            retention="7 days",
            enqueue=True,
        )

    return logger
