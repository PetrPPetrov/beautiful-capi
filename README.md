# beautiful-capi
Another wrapper generator for producing beautiful C API.

This program generates the required C++ and C code to wrap
your C++ classes to use them in a compiler-independent way.

For instance, a .DLL library which was built by vs2015 compiler
could be used by vs2003 compiler or by any other C++ or C compiler.

Another main concept is to generate a beautiful C API,
which is visibly suitable for human usage (not for computers or compilers).

*Background, Motivation*

In today's modern software development environment, there are may
C/C++ parsing techniques such as SWIG, web services and many more.

This project is meant to write a new automatic code generation tool similar
to SWIG, except the output is not Java/Python, it is ANSI-C & C++.

This is a little different than SWIG, generating pure C API output, formatted to be visually appealing.
Compiled  libs could be linked by another compiler or language (unlike
default C++ to C++ which requires the same compiler to be used on both
sides).

For example, a C++ vs2015 lib could be wrapped and called by vs2008 by
using C API (allowing both forward and backward compatibility).

Furthermore, the generation tool is written in Python, so is easily ported without compilation.

The main goal of this project is to produce highly efficient code and design elegance.
Knowing Java programmers prefer to write wrappers by hand to avoid sub-optimal SWIG outputs. 
This prototype project will primarily be for C++ applications calling C++ library classes, but via a wrapped API.
It's goal is not cross-language like SWIG.

Regarding the license, the code generated by this tool can be used for any purpose, including commercial.
Only the code generator tool itself is subject to GPL licensing.

