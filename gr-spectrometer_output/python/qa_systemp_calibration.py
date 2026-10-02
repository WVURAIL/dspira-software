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
from systemp_calibration import systemp_calibration

class qa_systemp_calibration (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def run_batch(self, block, data, capacity=None):
        count = len(data) if capacity is None else capacity
        outputs = [numpy.full((count, 4), numpy.nan, numpy.float32) for _ in range(3)]
        produced = block.work([data], outputs)
        self.assertEqual(produced, min(len(data), count))
        return [output[:produced].copy() for output in outputs]

    def test_calibration_batches_match_individual_spectra(self):
        batched = systemp_calibration(4, "hot")
        separate = systemp_calibration(4, "hot")
        for mode, values in [("hot", [340, 350, 360]),
                             ("cold", [50, 60, 70]),
                             ("cal", [80, 90, 100]),
                             ("nocal", [1, 2, 3])]:
            batched.set_parameters(mode)
            separate.set_parameters(mode)
            data = numpy.array([[value] * 4 for value in values], numpy.float32)
            actual = self.run_batch(batched, data)
            expected = [self.run_batch(separate, row[None, :]) for row in data]
            for port in range(3):
                numpy.testing.assert_allclose(
                    actual[port], numpy.concatenate([item[port] for item in expected]))
            numpy.testing.assert_array_equal(batched.hot, separate.hot)
            numpy.testing.assert_array_equal(batched.cold, separate.cold)

    def test_empty_batch_does_not_change_calibration(self):
        block = systemp_calibration(4, "hot")
        hot = block.hot.copy()
        self.run_batch(block, numpy.empty((0, 4), numpy.float32))
        numpy.testing.assert_array_equal(block.hot, hot)

    def test_output_capacity_limits_consumption(self):
        block = systemp_calibration(4, "hot")
        data = numpy.array([[340] * 4, [350] * 4, [360] * 4], numpy.float32)
        outputs = self.run_batch(block, data, capacity=2)
        numpy.testing.assert_array_equal(outputs[0], data[:2])
        numpy.testing.assert_array_equal(block.hot, data[1])

    def test_finite_flowgraph_processes_calibration_vectors(self):
        data = numpy.array([[340] * 4, [350] * 4, [360] * 4], numpy.float32)
        block = systemp_calibration(4, "hot")
        output = blocks.vector_sink_f(4)
        self.tb.connect(blocks.vector_source_f(data.ravel().tolist(), False, 4),
                        block, output)
        self.tb.connect((block, 1), blocks.null_sink(gr.sizeof_float * 4))
        self.tb.connect((block, 2), blocks.null_sink(gr.sizeof_float * 4))
        self.tb.run()
        numpy.testing.assert_array_equal(numpy.array(output.data()).reshape(-1, 4), data)


if __name__ == '__main__':
    gr_unittest.run(qa_systemp_calibration, "qa_systemp_calibration.xml")
