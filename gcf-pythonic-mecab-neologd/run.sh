#!/bin/bash
LD_LIBRARY_PATH=$PWD/local/lib/:$LD_LIBRARY_PATH ./pypy3-v5.9.0-linux64/bin/pypy3 ./mecabic.py
