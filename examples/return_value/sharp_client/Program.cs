using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace return_value_sharp_clayshake
{
    class Program
    {
        static void Main(string[] args)
        {
            var first_name = new ReturnValue.FirstName();
            first_name.SetFirstName("James");

            var middle_name = new ReturnValue.MiddleNamePtr();
            middle_name.SetMiddleName("Francis");

            var last_name = new ReturnValue.LastNameRawPtr();
            last_name.SetLastName("Stuatr");

            var person = new ReturnValue.Person();
            person.SetFirstName(first_name);
            person.SetMiddleName(middle_name);
            person.SetLastName(last_name);

            var printer = new ReturnValue.Printer();
            person.SetFirstName(person.GetFirstName());
            person.SetMiddleName(person.GetMiddleName());
            person.SetLastName(person.GetLastName());

            Console.ReadKey();
        }
    }
}
