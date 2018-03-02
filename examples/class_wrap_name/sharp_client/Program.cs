using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Linq;
using System.Text;

namespace Example
{
    class Program
    {
        static void Main(string[] args)
        {
            var printer = new ClassWrapName.WrapPrinter();
            printer.Show();

            Console.ReadKey();
        }
    }
}
