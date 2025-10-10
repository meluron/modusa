#!/usr/bin/env python3

import logging

class Config:
	LOG_LEVEL = logging.WARNING
	SR = 44100  # Default sampling rate
	TIME_UNIT = "sec"
	
	
	def __str__(self):
		return self.__dict__
	
	def __repr__(self):
		return self.__dict__

# Create a singleton instance
config = Config()