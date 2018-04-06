using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.Diagnostics.Contracts;
using Example;

namespace Copysemantic
{
    class Program
    {
        static void f1(Example.Printer p)
        {
            p.Show("form f1()");
        }

        static Example.Printer create_printer()
        {
            var new_printer = new Example.Printer();
            new_printer.Show("from create_printer()");
            return new_printer;
        }

        static void Main(string[] args)
        {
            Example.Printer printer = create_printer();
            printer.Show("form main()");
            f1(printer);

            var dumper = new Example.Dumper();
            dumper.SetPrinter(printer);
            dumper.Dump();

            Example.Printer printer2 = dumper.GetPrinter();
            printer2.Show("printer2");

            Console.ReadKey();
        }
    }
}
