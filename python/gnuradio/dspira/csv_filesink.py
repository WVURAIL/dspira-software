#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 DSPIRA.
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


import numpy as np
from gnuradio import gr
from ._spectrum_file import write_spectrum

class csv_filesink(gr.sync_block):
    """
    Save selected integrations while save_toggle is the string "True".
    Each selected spectrum receives its own CSV file, including batched input.
    """
    def __init__(self, vec_length, samp_rate, freq, prefix, save_toggle, integration_select, short_long_time_scale, az, elev, location):
        gr.sync_block.__init__(self,
            name="csv_filesink",
            in_sig=[(np.float32, int(vec_length))],
            out_sig=None)

        self.vec_length = int(vec_length)
        self.samp_rate = samp_rate
        self.freq = freq
        self.prefix = prefix
        self.save_toggle = save_toggle
        self.integration_select = integration_select
        self.short_long_time_scale = short_long_time_scale
        self.az = az
        self.elev = elev
        self.location = location

        self.frequencies = np.arange(freq - samp_rate/2, freq + samp_rate/2, samp_rate/vec_length)[:vec_length]
        self.data_array = np.zeros((vec_length,2))
        self.N_long_counter = 0
        self.spectrum = np.zeros(vec_length)

    def work(self, input_items, output_items):
        for spectrum in input_items[0]:
            if self.save_toggle != "True":
                continue
            if self.integration_select == 0:
                self._save(spectrum)
                self.N_long_counter += 1
            elif self.N_long_counter >= self.short_long_time_scale - 1:
                self._save(spectrum)
                self.N_long_counter = 0
            else:
                self.N_long_counter += 1
        return len(input_items[0])

    def _save(self, spectrum):
        self.data_array[:, 0] = np.round(self.frequencies / 1e6, decimals=4)
        self.data_array[:, 1] = np.round(spectrum, decimals=4)
        self.textfilename = write_spectrum(
            self.prefix, self.location, self.az, self.elev, self.data_array)

    def set_save_toggle(self, save_toggle):
        self.save_toggle = save_toggle

    def set_integration_select(self, integration_select):
        self.integration_select = integration_select

    def set_az(self, az):
        self.az = az

    def set_elev(self, elev):
        self.elev = elev

    def set_location(self, location):
        self.location = location

