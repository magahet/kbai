#!/bin/bash

pandoc --toc -V geometry:margin=1in,columnsep=1cm,twocolumn -o paper.pdf paper.md
