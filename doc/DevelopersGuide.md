Beautiful-Capi Developer's Guide
================================

1. [Introduction](#introduction)
    * [C++ problems](#c-problems)
        * [C++ ABI](#c-abi)
        * [Name mangling](#name-mangling)
        * [C++ STL ABI](#c-stl-abi)
        * [Exceptions](#exceptions)
    * [Basic solutions](#basic-solutions)
    * [Beautiful Capi solution](#beautiful-capi-solution)
2. [Lifecycle semantics](#lifecycle-semantics)
    * [Copy semantic](#copy-semantic)
    * [Reference counted semantic](#reference-counted-semantic)
    * [Raw pointer semantic](#raw-pointer-semantic)
    * [Mixing semantics](#mixing-semantics)
3. [Exceptions](#exceptions)
4. [Callbacks](#callbacks)
6. [Templates](#templates)
5. [Making compiler-independent libraries](#making-compiler-independent-libraries)
    * [Dynamic loader](#dynamic-loader)
    * [Windows](#windows)
    * [Linux](#linux)
    * [MacOSX](#macosx)

Introduction
------------

Beautiful Capi is a tool which automatizes the creation of compiler-independent
and binary compatible (between different C++ compilers) C++ libraries.
Any C++ library compiled once could be used many times by the other C++ compilers without recompilation.
Of course, the compiled C++ libraries are compatible only on the same platforms and architectures where they were built.

Beautiful Capi is written in Python 3. It _does not parse_ the library source code to obtain its
[API](https://en.wikipedia.org/wiki/Application_programming_interface) description.
Instead of that, you should provide the library API description in XML format.
Usually XML files which describe the library API are created by hand.
There are not any tools for creating XML API description files yet, however, such tools could be created in the future.
There are [plans](https://github.com/PetrPPetrov/beautiful-capi/issues/24)
to add support of some convenient DSL (Domain-Specific Language) in parallel to XML format. 

Beautiful Capi is not intended as a tool for automatizing cross-language C++ libraries creation (for instance, 
the cases when a C++ library is used in Java or C# application) like [SWIG](http://www.swig.org/).
However, in the future Beautiful Capi could introduce such features and support of some target languages are planned.
For details please see [issue 7](https://github.com/PetrPPetrov/beautiful-capi/issues/7) and
[issue 39](https://github.com/PetrPPetrov/beautiful-capi/issues/39).

### C++ problems

#### C++ ABI

The one of the main C++ language problems is [ABI](https://en.wikipedia.org/wiki/Application_binary_interface)
(Application Binary Interface). The C++ language standard does not specify any ABI and it is implementation specific.
For instance, the C++ language standard does not define size of _int_ type.
Each C++ compiler vendor can provide his own implementation of ABI.
Any C++ library should be built again and again for every C++ compiler which is planned
to use as a compiler for applications which use the library.   

#### Name mangling

The second problem in C++ is [name mangling](https://en.wikipedia.org/wiki/Name_mangling).
In C++ name mangling is an encoding scheme which translates
complex C++ identifiers (including overloaded functions and methods, template instantiations,
namespaces, etc.) to plain C functions. The C++ language standard does not specify any name mangling scheme.
Again, each C++ compiler vendor can provide his own implementation of name manging. C++ compiler which
is used by an application could use a different name mangling scheme rather than C++ compiler
which was used for building of the library. As result a developer of a application will get unresolved
symbol linking errors.

#### C++ STL ABI

The third problem is binary incompatible C++ standard libraries.
For instance, the size of _std::string_ class is implementation specific and could vary
from one C++ compiler to another, and even from one build configuration to another.

#### Exceptions
 
Different C++ compilers implement different exception throwing and catching schemes.
An exception thrown from one C++ compiler runtime, in general, could not be caught into another C++ compiler runtime.

### Basic solutions

The basic solution for providing a stable ABI is to use special types which have fixed sizes.
For instance, using _int32_t_ type instead of _int_ type, etc.
The calling convention is also important, so, the developer should manually specify the calling
convention for each method or function.

The basic solution for overcoming different name mangling schemas is manually writing plain C function.
However, it is boiler-plate and error-prone.

The basic solution for binary incompatible C++ standard libraries problem is avoiding
of exposing C++ standard library classes from the library API.
So, the library API should contain only primitive
and fixed sized types in its API. As result, a developer should manually split some
complex C++ standard library templates (such as _std::vector<>_, _std::map<>_) to primitive functions and types,
which is also boiler-plate and error-prone.

Also, the developer should manually write C++ wrapper classes which will propose some higher level API rather
than plain C functions and types. Such process is laborious, boiler-plate and error-prone.

### Beautiful Capi solution

Beautiful Capi is a tool which automatizes the creation of compiler-independent C++ libraries and it helps
a lot to solve name mangling problem, generating C++ wrapper classes, wrapping C++ STL library template classes,
catching and rethrowing exceptions and some more.

Consider [hello_world](https://github.com/PetrPPetrov/beautiful-capi/tree/master/examples/hello_world)
Beautiful Capi example. It exposes the following class:
~~~C++
#include <iostream>

namespace HelloWorld
{
    class PrinterImpl
    {
    public:
        void Show() const;
    };
}

void HelloWorld::PrinterImpl::Show() const
{
    std::cout << "Hello Beautiful World!" << std::endl;
}
~~~

In fact _HelloWorld::PrinterImpl_ class is an internal class and it is not exposed directly
for _HelloWorld_ library clients. Instead of _HelloWorld::PrinterImpl_ class an opaque _void*_ pointer is used
by the following automatic generated plain C functions:
~~~C
void* hello_world_printer_default()
{
    return new HelloWorld::PrinterImpl();
}

void hello_world_printer_show_const(void* object_pointer)
{
    const HelloWorld::PrinterImpl* self = static_cast<HelloWorld::PrinterImpl*>(object_pointer);
    self->Show();
}

void* hello_world_printer_copy(void* object_pointer)
{
    return new HelloWorld::PrinterImpl(*static_cast<HelloWorld::PrinterImpl*>(object_pointer));
}

void hello_world_printer_delete(void* object_pointer)
{
    delete static_cast<HelloWorld::PrinterImpl*>(object_pointer);
}
~~~

For simplicity we put down some details here, like calling conventions or C linkage options for these functions.

Note that all plain C function names have *hello_world_* prefix which came from _HelloWorld_ namespace.
The second part of all plain C function names is *printer_* which came from _Printer_ class name.
And the rest parts are method names. You can note that there are some simple rules for conversion any C++ identifier
to plain C function name.

And automatic generated C++ wrapper class:
~~~C++
namespace HelloWorld
{
    class Printer
    {
    public:
        Printer()
        {
            SetObject(hello_world_printer_default());
        }
        void Show() const
        {
            hello_world_printer_show_const(GetRawPointer());
        }
        Printer(const Printer& other)
        {
            if (other.GetRawPointer())
            {
                SetObject(hello_world_printer_copy(other.GetRawPointer()));
            }
            else
            {
                SetObject(0);
            }
        }
        ~Printer()
        {
            if (GetRawPointer())
            {
                hello_world_printer_delete(GetRawPointer());
                SetObject(0);
            }
        }
        void* GetRawPointer() const
        {
            return mObject;
        }
    protected:
        void SetObject(void* object_pointer)
        {
            mObject = object_pointer;
        }
        void* mObject;
    };
}
~~~

Of course, you need to create manually the following XML API description file:
~~~XML
<?xml version="1.0" encoding="utf-8" ?>
<hello_world:api xmlns:hello_world="http://gkmsoft.ru/beautifulcapi" project_name="HelloWorld">
  <namespace name="HelloWorld">
    <class name="Printer" lifecycle="copy_semantic" implementation_class_name="HelloWorld::PrinterImpl" implementation_class_header="PrinterImpl.h">
      <constructor name="Default"/>
      <method name="Show" const="true"/>
    </class>
  </namespace>
</hello_world:api>
~~~

And sample usage of this class from client side:
~~~C++
#include <iostream>
#include <cstdlib>
#include "HelloWorld.h"

int main()
{
    HelloWorld::Printer printer;
    printer.Show();

    return EXIT_SUCCESS;
}
~~~

In this example _HelloWorld::PrinterImpl_ is the __implementation class__,
_HelloWorld::Printer_ is the __wrapper class__. In XML API description file _HelloWorld::Printer_ identifier could be
used for referencing this wrapped class and it is called __API identifier__ or just __identifier__.
In this example wrapper class name is the same as identifier, but, in general, they could be different.

Note that _HelloWorld::PrinterImpl_ class has copy semantic. It means that the implementation class object instances
are always copied when the wrapper class object instances are copied, and the implementation class object instances
are deleted when the wrapper class object instances are deleted. There are possible other behaviours.
In terms of Beautiful Capi tool a such behaviour is called __lifecycle semantic__.
Beautiful Capi supports several typical lifecycle semantics.

We can designate the following three things:
1. The __implementation side__. It means all code inside the C++ library, all classes,
functions, methods and other types inside the C++ library. The implementation classes are used in the C++ library.
Usually the C++ libraries are shared libraries which are intended to use by different C++ compilers.
2. The tiny __C glue layer__. The bodies of C glue functions are located inside the C++ library, in automatic
generated .cpp file. In fact these functions are written in C++ (to have access to the implementation classes)
and just have C linkage option enabled. So, outside the C++ library these functions are seen as pure C functions.
Beautiful Capi generates both bodies of these functions and their declarations. The declarations are visible outside
of the C++ library.
3. The __wrap side__. It means all code inside any client of the C++ library, all classes,
functions, methods and other types inside any client of the C++ library. Clients of the C++ library
could be executable files, static libraries and shared libraries. The clients could be written both in pure
C language and in C++ language. The C++ clients usually use the generated wrapper classes. The C clients use pure
C functions directly. The wrapper classes are automatically generated by Beautiful Capi and visible only outside
of the C++ library, inside the C++ library the wrapper classes are unavailable.

Lifecycle semantics
-------------------

Beautiful Capi assumes that the implementation class object instances are always created on the heap.
This fact is applied for all lifecycle semantics.

### Copy semantic

Copy semantics means that the implementation class object instance is always copied when
the wrapper class object instance is copied. In other words, copy semantics emulates objects by value,
however, as we noted above, Beautiful Capi assumes that the implementation class object instances are always created
on the heap. So, Beautiful Capi generates a special *_copy* function and the wrapper class calls the copy function.
~~~C
void* namespace_prefix_class_name_copy(void* object_pointer)
{
    return new ImplementationClass(*static_cast<ImplementationClass*>(object_pointer));
}
~~~

It works only if copy constructor for implementation class is available. If a class has copy semantic
then Beautiful Capi assumes that a copy constructor for implementation class is available.
Currently such supposition is hard-coped inside Beautiful Capi and can not be changed.

The copy function is used both in the wrapper class copy constructor and the assignment operator.

Copy semantic emulates objects by value, thus, the generated wrapper classes propose to use "." (the dot sign)
for accessing the wrapped class methods.

### Reference counted semantic
TODO:

### Raw pointer semantic
TODO:

### Mixing semantics
TODO:

XML API description schema reference
------------------------------------
TODO:

Exceptions
----------
TODO:

Callbacks
---------
TODO:

Templates
---------
TODO:

Making compiler-independent libraries
-------------------------------------
TODO:

### Dynamic loader
TODO:

### Windows
TODO:

### Linux
TODO:

### MacOSX
TODO:
