using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace OverloadSuffix
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Namespace overload_suffix_mode = Notify");
            Console.WriteLine("Class overload_suffix_mode = Silent");
            Console.WriteLine("Create Printer");
            var printer = new OverloadSuffix.Printer();

            Console.WriteLine("Overloaded methods:");
            printer.Show();
            printer.ShowConst();
            printer.Show(7);
            printer.Show(4.2);

            Console.WriteLine("Overloaded functions:");
            OverloadSuffix.Functions.Show();
            OverloadSuffix.Functions.Show(5);
            OverloadSuffix.Functions.Show(1.3);

            Console.ReadKey();
        }
    }
}
