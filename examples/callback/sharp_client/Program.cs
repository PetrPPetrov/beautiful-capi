using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Linq;
using System.Text;    
using System.Reflection;

namespace ConsoleApp1
{

    class CustomPrinterImplementation
    {
        string mLastPrintedText;
        Example.PrinterPtr.EQuality mQuality;

        public CustomPrinterImplementation()
        {
            Console.WriteLine("CustomPrinterImplementation ctor");
        }

        ~CustomPrinterImplementation()
        {
            Console.WriteLine("CustomPrinterImplementation dtor");
        }

        public void Print(string text) // Note that this method is non-virtual
        {
            if (text == "")
            {
                // This exception will be correctly passed through the library boundary
                // and will be caught by the library code
                throw new Exception.NullArgument();
            }
            mLastPrintedText = text;
            mLastPrintedText = mLastPrintedText.ToUpper();
            Console.WriteLine(mLastPrintedText);
        }

        public void SetPrintingQuality(Example.PrinterPtr.EQuality printing_quality)
        {
            mQuality = printing_quality;
        }

        public Example.PrinterPtr.EQuality GetPrintingQuality()
        {
            return mQuality;
        }

        public Example.EPrintingDevice GetDeviceType()
        {
            return Example.EPrintingDevice.printer;
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            var famous_person = new Example.Person();
            famous_person.SetAge(26);
            famous_person.SetFirstName("Isaac");
            famous_person.SetSecondName("Newton");
            famous_person.SetSex(Example.Person.ESex.male);

            Example.PrinterPtr printing_device = Example.Functions.CreateDefaultPrinter(Example.EPrintingDevice.printer);
            famous_person.Dump(printing_device);
            famous_person.Print(printing_device, "Hello World");

            CustomPrinterImplementation my_printer_implementation = new CustomPrinterImplementation();
            printing_device = Example.Functions.create_callback_for_printer(my_printer_implementation);
            famous_person.Dump(printing_device);            

            // CustomPrinterImplementation.Print() will throw exception (Exception.NullArgument)
            // and this exception will be caught by the library code
            famous_person.Print(printing_device, "");
            Console.WriteLine("Done");
            Console.ReadKey();
        }
    }
}
