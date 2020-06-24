#  !/usr/bin/env python
#
#  classes.py
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on reportlab.lib.pagesizes and reportlab.lib.units
#    www.reportlab.co.uk
#    Copyright ReportLab Europe Ltd. 2000-2017
#    Copyright (c) 2000-2018, ReportLab Inc.
#    All rights reserved.
#    Licensed under the BSD License
#
#  Includes data from en.wikipedia.org.
#  Licensed under the Creative Commons Attribution-ShareAlike License
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
from collections import namedtuple
from typing import List, Tuple

# this package
from ._types import AnyNumber
from .units import Unit, _rounders, cicero, cm, didot, inch, mm, new_cicero, new_didot, pica, pt, scaled_point, um
from .utils import convert_from

__all__ = [
		"BaseSize",
		"Size_mm",
		"Size_inch",
		"Size_cm",
		"Size_um",
		"Size_pica",
		"Size_didot",
		"Size_cicero",
		"Size_new_didot",
		"Size_new_cicero",
		"Size_scaled_point",
		"PageSize",
		]


class BaseSize(namedtuple("__BaseSize", "width, height")):
	"""
	Base class namedtuple representing a page size, in point

	:param width: The page width
	:type width: int, float, Decimal or Unit
	:param height: The page height
	:type height: int, float, Decimal or Unit
	"""

	__slots__: List[str] = []
	_unit: Unit = pt
	width: Unit
	height: Unit

	def __new__(cls, width: AnyNumber, height: AnyNumber):
		return super().__new__(
				cls,
				cls._unit(width),
				cls._unit(height),
				)

	def __str__(self) -> str:
		return f"{self.__class__.__name__}(width={_rounders(self.width, '0')}, height={_rounders(self.height, '0')})"

	@classmethod
	def from_pt(cls, size: Tuple[float, float]):
		"""
		Create a :class:`~domdf_python_tools.pagesizes.classes.BaseSize` object from a
		page size in point..

		:param size: The size, in point, to convert from

		:rtype: A subclass of :class:`~domdf_python_tools.pagesizes.classes.BaseSize`
		"""

		assert isinstance(size, PageSize)

		return cls(cls._unit.from_pt(size[0]), cls._unit.from_pt(size[1]))

	@classmethod
	def from_size(cls, size: Tuple[AnyNumber, AnyNumber]) -> "BaseSize":
		"""
		Create a :class:`~domdf_python_tools.pagesizes.classes.BaseSize` object from a tuple
		"""

		return cls(*size)

	def is_landscape(self) -> bool:
		"""
		Returns whether the page is in the landscape orientation
		"""

		return self.width >= self.height

	def is_portrait(self) -> bool:
		"""
		Returns whether the page is in the portrait orientation
		"""

		return self.width < self.height

	def is_square(self) -> bool:
		"""
		Returns whether the given pagesize is square
		"""

		return self.width == self.height

	def landscape(self) -> "BaseSize":
		"""
		Returns the pagesize in landscape orientation
		"""

		if self.is_portrait():
			return self.__class__(self.height, self.width)
		else:
			return self

	def portrait(self) -> "BaseSize":
		"""
		Returns the pagesize in portrait orientation
		"""

		if self.is_landscape():
			return self.__class__(self.height, self.width)
		else:
			return self

	def to_pt(self) -> "PageSize":
		"""
		Returns the page size in point
		"""

		return PageSize(self.width.as_pt(), self.height.as_pt())


# TODO: conversion to Point for the __eq__ function in the below


class Size_mm(BaseSize):
	"""
	Subclass of :class:`~domdf_python_tools.pagesizes.classes.BaseSize`
	representing a pagesize in millimeters.

	:param width: The page width
	:type width: int, float, Decimal or Unit
	:param height: The page height
	:type height: int, float, Decimal or Unit
	"""

	_unit = mm


class Size_inch(BaseSize):
	"""
	Subclass of :class:`~domdf_python_tools.pagesizes.classes.BaseSize`
	representing a pagesize in inches.

	:param width: The page width
	:type width: int, float, Decimal or Unit
	:param height: The page height
	:type height: int, float, Decimal or Unit
	"""

	_unit = inch


class Size_cm(BaseSize):
	"""
	Subclass of :class:`~domdf_python_tools.pagesizes.classes.BaseSize`
	representing a pagesize in centimeters.

	:param width: The page width
	:type width: int, float, Decimal or Unit
	:param height: The page height
	:type height: int, float, Decimal or Unit
	"""

	_unit = cm


class Size_um(BaseSize):
	"""
	Subclass of :class:`~domdf_python_tools.pagesizes.classes.BaseSize`
	representing a pagesize in micrometers.

	:param width: The page width
	:type width: int, float, Decimal or Unit
	:param height: The page height
	:type height: int, float, Decimal or Unit
	"""

	_unit = um


class Size_pica(BaseSize):
	"""
	Subclass of :class:`~domdf_python_tools.pagesizes.classes.BaseSize`
	representing a pagesize in pica.

	:param width: The page width
	:type width: int, float, Decimal or Unit
	:param height: The page height
	:type height: int, float, Decimal or Unit
	"""

	_unit = pica


class Size_didot(BaseSize):
	"""
	Subclass of :class:`~domdf_python_tools.pagesizes.classes.BaseSize`
	representing a pagesize in didots / French Points.

	:param width: The page width
	:type width: int, float, Decimal or Unit
	:param height: The page height
	:type height: int, float, Decimal or Unit
	"""

	_unit = didot


class Size_cicero(BaseSize):
	"""
	Subclass of :class:`~domdf_python_tools.pagesizes.classes.BaseSize`
	representing a pagesize in ciceros.

	:param width: The page width
	:type width: int, float, Decimal or Unit
	:param height: The page height
	:type height: int, float, Decimal or Unit
	"""

	_unit = cicero


class Size_new_didot(BaseSize):
	"""
	Subclass of :class:`~domdf_python_tools.pagesizes.classes.BaseSize`
	representing a pagesize in new didots.

	:param width: The page width
	:type width: int, float, Decimal or Unit
	:param height: The page height
	:type height: int, float, Decimal or Unit
	"""

	_unit = new_didot


class Size_new_cicero(BaseSize):
	"""
	Subclass of :class:`~domdf_python_tools.pagesizes.classes.BaseSize`
	representing a pagesize in ciceros.

	:param width: The page width
	:type width: int, float, Decimal or Unit
	:param height: The page height
	:type height: int, float, Decimal or Unit
	"""

	_unit = new_cicero


class Size_scaled_point(BaseSize):
	"""
	Subclass of :class:`~domdf_python_tools.pagesizes.classes.BaseSize`
	representing a pagesize in scaled points.

	:param width: The page width
	:type width: int, float, Decimal or Unit
	:param height: The page height
	:type height: int, float, Decimal or Unit
	"""

	_unit = scaled_point


class PageSize(BaseSize):
	"""
	Subclass of :class:`~domdf_python_tools.pagesizes.classes.BaseSize`
	representing a pagesize in point.

	:param width: The page width
	:type width: int, float, Decimal or Unit
	:param height: The page height
	:type height: int, float, Decimal or Unit

	The pagesize can be converted to other units using the properties below.
	"""

	__slots__: List[str] = []

	def __new__(cls, width: AnyNumber, height: AnyNumber, unit: AnyNumber = pt):
		"""
		Create a new :class:`~domdf_python_tools.pagesizes.classes.PageSize` object.

		:param width:
		:param height:
		:param unit:
		"""

		width, height = convert_from((width, height), unit)
		return super().__new__(cls, width, height)

	@property
	def inch(self) -> Size_inch:
		"""
		Returns the pagesize in inches.
		"""

		return Size_inch.from_pt(self)

	@property
	def cm(self) -> Size_cm:
		"""
		Returns the pagesize in centimeters.
		"""

		return Size_cm.from_pt(self)

	@property
	def mm(self) -> Size_mm:
		"""
		Returns the pagesize in millimeters.
		"""

		return Size_mm.from_pt(self)

	@property
	def um(self) -> Size_um:
		"""
		Returns the pagesize in micrometers.
		"""

		return Size_um.from_pt(self)

	@property
	def pc(self) -> Size_pica:
		"""
		Returns the pagesize in pica.
		"""

		return Size_pica.from_pt(self)

	pica = pc

	@property
	def dd(self) -> Size_didot:
		"""
		Returns the pagesize in didots.
		"""

		return Size_didot.from_pt(self)

	didot = dd

	@property
	def cc(self) -> Size_cicero:
		"""
		Returns the pagesize in ciceros.
		"""

		return Size_cicero.from_pt(self)

	cicero = cc

	@property
	def nd(self) -> Size_new_didot:
		"""
		Returns the pagesize in new didots.
		"""

		return Size_new_didot.from_pt(self)

	new_didot = nd

	@property
	def nc(self) -> Size_new_cicero:
		"""
		Returns the pagesize in new ciceros.
		"""

		return Size_new_cicero.from_pt(self)

	new_cicero = nc

	@property
	def sp(self) -> Size_scaled_point:
		"""
		Returns the pagesize in scaled point.
		"""

		return Size_scaled_point.from_pt(self)

	scaled_point = sp
