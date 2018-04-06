using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Linq;
using System.Text;

namespace ConsoleApp1
{
    class Program
    {
        static void Main(string[] args)
        {
            HelloWorld.Printer printer = new HelloWorld.Printer();
            printer.Show();

            Console.ReadKey();
        }
    }
}
