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
from harmonicgenerator import harmonicgenerator

class qa_harmonicgenerator (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_batch_advances_every_vector_and_reports_items(self):
        block = harmonicgenerator(2, 4, [1.0, 0.5], 1, [1, 3], 40)
        first = [numpy.empty((3, 4), numpy.float32) for _ in range(2)]
        second = [numpy.empty((2, 4), numpy.float32) for _ in range(2)]
        self.assertEqual(block.work([], first), 3)
        self.assertEqual(block.work([], second), 2)
        samples = numpy.arange(4, 24).reshape(5, 4)
        for port, amplitude, harmonic in [(0, 1.0, 1), (1, 0.5, 3)]:
            expected = amplitude * numpy.sin(2 * numpy.pi * harmonic * samples / 40)
            numpy.testing.assert_allclose(
                numpy.concatenate([first[port], second[port]]), expected, atol=1e-6)

    def test_empty_output_preserves_phase(self):
        block = harmonicgenerator(1, 4, [1.0], 1, [1], 40)
        phase = block.i.copy()
        self.assertEqual(block.work([], [numpy.empty((0, 4), numpy.float32)]), 0)
        numpy.testing.assert_array_equal(block.i, phase)


if __name__ == '__main__':
    gr_unittest.run(qa_harmonicgenerator, "qa_harmonicgenerator.xml")
