What?
=====

This tool checks for a subset of C in which ranges variables reside.

Installation
============

This needs [ply](http://www.dabeaz.com/ply/)

Usage
=====

Annotate some variables in your C-Code with a range like this:

    int x; /*[4-5]*/

Run "./crf.py" or "./crf.py filename.c". The output will have every assignement
annotated with the range of the expression on the right. At the same time the
maximum ranges for the variable on the left are tracked and printed at the end
of the output.
