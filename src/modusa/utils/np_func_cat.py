#!/usr/bin/env python3

# This contains categorised NumPy functions
# This is useful while handling np operations on modusa signals

import numpy as np

SHAPE_PRESERVING_FUNCS = {
	np.sin, np.cos, np.tan, 
	np.sinh, np.cosh, np.tanh,
	np.arcsin, np.arccos, np.arctan,
	np.exp, np.expm1, np.log, np.log2, np.log10, np.log1p,
	np.abs, np.negative, np.positive,
	np.square, np.sqrt, np.cbrt,
	np.floor, np.ceil, np.round, np.rint, np.trunc,
	np.clip, np.sign,
	np.add, np.subtract, np.multiply, np.true_divide, np.floor_divide
}

REDUCTION_FUNCS = {
	np.sum, np.prod,
	np.mean, np.std, np.var,
	np.min, np.max,
	np.argmin, np.argmax,
	np.median, np.percentile,
	np.all, np.any,
	np.nanmean, np.nanstd, np.nanvar, np.nansum
}

CONCAT_FUNCS = {
	np.concatenate, np.stack, np.hstack, np.vstack, np.dstack,
	np.column_stack, np.row_stack
}

X_NEEDS_ADJUSTMENT_FUNCS = {
	np.diff,
	np.gradient,
	np.trim_zeros,
	np.unwrap,
	np.fft.fft, np.fft.ifft, np.fft.fftshift, np.fft.ifftshift,
	np.correlate, np.convolve
}


