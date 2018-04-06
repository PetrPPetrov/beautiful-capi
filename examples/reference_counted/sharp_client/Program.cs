using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace reference_counted_sharp_claim
{
    class Program
    {
        static void f1(Example.PrinterPtr p)
        {
            p.Show("from f1()");
        }

        static Example.PrinterPtr create_printer()
        {
            var new_printer = new Example.PrinterPtr();
            new_printer.Show("from create_printer()");
            return new_printer;
        }

        static void Main()
        {
            var printer = new Example.PrinterPtr();
            printer = create_printer();
            printer.Show("from main()");
            f1(printer);

            var dumper = new Example.Dumper();
            dumper.SetPrinter(printer);
            dumper.Dump();

            Example.PrinterPtr printer2 = dumper.GetPrinter();
            printer2.Show("printer2");

            Console.ReadKey();
        }
    }
}
