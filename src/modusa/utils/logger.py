#!/usr/bin/env python3

import logging

def setup_logging(log_level: int | None = logging.WARNING):
	logging.basicConfig(
		level=log_level,
		format="%(asctime)s | %(levelname)s | %(name)s | %(funcName)s():%(lineno)d\n> %(message)s\n",
		datefmt='%Y-%m-%d %H:%M:%S'
	)
	# Silence 3rd-party spam
	logging.getLogger("matplotlib").setLevel(logging.WARNING)
	logging.getLogger("PIL").setLevel(logging.WARNING)
	logging.getLogger("numba").setLevel(logging.WARNING)
	logging.getLogger("py").setLevel(logging.ERROR)
	
def get_logger(name=None):
	return logging.getLogger(name)
