using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace sharp_client
{
    class Program
    {
        static void Main(string[] args)
        {
            var printer = new PrinterNS.Printer();
            var a = new Classes.ClassA();
            var b = new Classes.ClassBRawPtr();
            var c = new Classes.ClassCPtr();
            a.SetValue(3);
            b.SetValue("str");
            c.SetValue(7.2);
            var comp_a = new Components.ComponentA();
            comp_a.SetA(a);
            comp_a.SetB(b);
            comp_a.SetC(c);
            var comp_b = new Components.ComponentBRawPtr();
            comp_b.SetA(a);
            comp_b.SetB(b);
            comp_b.SetC(c);
            var comp_c = new CompC.ComponentCPtr();
            comp_c.SetA(a);
            comp_c.SetB(b);
            comp_c.SetC(c);

            printer.Show(comp_a);
            printer.Show(comp_b);
            printer.Show(comp_c);

            Console.WriteLine("Change values to '8', 'another string' and '3.14':");
            a.SetValue(8);
            b.SetValue("another string");
            c.SetValue(3.14);

            printer.Show(comp_a);
            printer.Show(comp_b);
            printer.Show(comp_c);

            b.SetValue("string");
            printer.Show(comp_b);
        }
    }
}
