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
            var person = new MappedTypes.Person();
            person.SetFirstName("John");
            person.SetSecondName("Snow");
            person.SetAge(14);
            person.SetSex(true);
            Console.WriteLine(person.GetFirstName());
            Console.WriteLine(person.GetSecondName());
            Console.WriteLine(person.GetAge());
            Console.WriteLine(person.IsMan());

            var device = new MappedTypes.Device();
            device.SetName("Printer");
            device.SetBusy(false);
            Console.WriteLine(device.GetName());
            Console.WriteLine(device.IsBusy());

            Console.ReadKey();
        }
    }
}
