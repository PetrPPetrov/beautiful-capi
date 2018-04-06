using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Linq;
using System.Text;

using ApiInclude;

namespace ApiIncludeClient1
{
    class Program
    {
        static void Main2(string[] args)
        {
            var printer = new Printer();
            printer.SayHello();
            Functions.SayHello();

            var exist_class = new ExistingClass();
            exist_class.SayHello();
            Functions.ExistingFunc();

            ApiInclude.ExistingNS.Functions.SayHello();

            Console.ReadKey();
        }
    }
}
