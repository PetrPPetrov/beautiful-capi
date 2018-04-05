using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace mixed_semantic
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Create address_ref.");
            var address_ref = new MixedSemantic2.AddressPtr();
            Console.WriteLine("Create address_raw and address_copy appropriating them address_ref.");
            Console.WriteLine();
            MixedSemantic2.AddressRawPtr address_raw = (MixedSemantic2.AddressRawPtr)address_ref;
            MixedSemantic2.AddressCopy address_copy = (MixedSemantic2.AddressCopy)address_ref;

            Console.WriteLine("Set address_ref name: Avenu N.5");
            address_ref.SetStreetName("Avenu N.5");

            Console.WriteLine("Names:");
            Console.WriteLine("street name (RefCount) = " + address_ref.GetStreetName());
            Console.WriteLine("street name (RawPtr) = " + address_raw.GetStreetName());
            Console.WriteLine("street name (Copy) = " + address_copy.GetStreetName());
            Console.WriteLine();

            Console.WriteLine("Set address_raw name: Koshevogo");
            address_raw.SetStreetName("Koshevogo");

            Console.WriteLine("Names:");
            Console.WriteLine("street name (RefCount) = " + address_ref.GetStreetName());
            Console.WriteLine("street name (RawPtr) = " + address_raw.GetStreetName());
            Console.WriteLine("street name (Copy) = " + address_copy.GetStreetName());
            Console.WriteLine();

            Console.WriteLine("Set address_copy name: Lenina");
            address_copy.SetStreetName("Lenina");

            Console.WriteLine("Names:");
            Console.WriteLine("street name (RefCount) = " + address_ref.GetStreetName());
            Console.WriteLine("street name (RawPtr) = " + address_raw.GetStreetName());
            Console.WriteLine("street name (Copy) = " + address_copy.GetStreetName());
            Console.WriteLine();


            var printer = new MixedSemantic2.Printer();
            Console.WriteLine("Create copy semantic name.");
            Console.WriteLine();
            var name = new MixedSemantic2.Name("default_name", "", "");
            Console.WriteLine("name:");
            printer.Show(name);

            Console.WriteLine("Create RawPtr semantic name_ptr, appropriating him name.");
            MixedSemantic2.NameRawPtr name_ptr = (MixedSemantic2.NameRawPtr)name;
            Console.WriteLine("change name_ptr");
            name_ptr.SetFirstName("changed_name");
            Console.WriteLine("name_ptr:");
            printer.Show(name);
            Console.WriteLine();


            Console.WriteLine("Create RawPtr semantic Person:");
            var person = new MixedSemantic2.PersonRawPtr();
            person.SetName(name);
            person.GetName().SetFirstName("inplace modification");
            Console.WriteLine(person.GetName().GetFirstName());
            person.SetDay(27);
            person.SetMonth(12);
            person.SetYear(324);
            printer.Show(person);
            printer.ShowByPointer(person);
            printer.ShowByReference(person);
            Console.WriteLine();

            Console.WriteLine("Create copy semantic Person and appropriating him Person.");
            MixedSemantic2.PersonCopy person_copy = new MixedSemantic2.PersonCopy(person);
            Console.WriteLine("Change person_copy");
            person_copy.SetDay(0);
            person_copy.SetMonth(0);
            person_copy.SetYear(0);
            printer.Show(person_copy);
            printer.ShowByPointer(person_copy);
            printer.ShowByReference(person_copy);
            Console.WriteLine();

            Console.WriteLine("original Person:");
            printer.Show(person);
            printer.ShowByPointer(person);
            printer.ShowByReference(person);
        }
    }
}
