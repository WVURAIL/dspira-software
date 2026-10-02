#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr, gr_unittest
from gnuradio import blocks
from spectrometer_output import spectrometer_output

class qa_spectrometer_output (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_batch_generates_each_sample_and_reports_items(self):
        block = spectrometer_output(1, 20, 2, "", False)
        first = numpy.empty(7, numpy.float32)
        second = numpy.empty(5, numpy.float32)
        self.assertEqual(block.work([], [first]), 7)
        self.assertEqual(block.work([], [second]), 5)
        expected = 2 * numpy.sin(2 * numpy.pi * numpy.arange(1, 13) / 20)
        numpy.testing.assert_allclose(numpy.concatenate([first, second]), expected, atol=1e-6)

    def test_empty_output_preserves_phase(self):
        block = spectrometer_output(1, 20, 2, "", False)
        self.assertEqual(block.work([], [numpy.empty(0, numpy.float32)]), 0)
        self.assertEqual(block.i, 0)


if __name__ == '__main__':
    gr_unittest.run(qa_spectrometer_output, "qa_spectrometer_output.xml")
