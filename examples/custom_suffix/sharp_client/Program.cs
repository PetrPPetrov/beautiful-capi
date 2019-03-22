using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using hello_world;

namespace CustomSuffix
{
    class Program
    {
        static void Main(string[] args)
        {
            var printer = new hello_world.printer();
            printer.show();

            var scanner = new hello_world.scanner_raw_ptr();
            if(scanner.is_null())
            {
                Console.WriteLine("Error, scanner is null!");
                Console.ReadKey();
            }
            scanner.scan();
            scanner.deallocate();

            var plotter = new hello_world.plotter_ptr();
            if(plotter.is_null())
            {
                Console.WriteLine("Error, plotter is null!");
            }
            if(plotter.is_not_null())
            {
                plotter.draw();
            }

            Console.ReadKey();
        }
    }
}
