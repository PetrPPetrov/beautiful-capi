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
            MixedSemantic.Printer printer = new MixedSemantic.Printer();

            MixedSemantic.Name name = new MixedSemantic.Name("Jon", "Edward", "Snow");
            printer.Show(name);
            printer.ShowByPointer(name);
            printer.ShowByReference(name);

            MixedSemantic.PersonRawPtr person = new MixedSemantic.PersonRawPtr();
            person.SetName(name);
            person.SetDay(27);
            person.SetMonth(12);
            person.SetYear(324);
            printer.Show(person);
            printer.ShowByPointer(person);
            printer.ShowByReference(person);

            MixedSemantic.AddressPtr address = new MixedSemantic.AddressPtr();
            address.SetStreetName("Wall");
            person.SetAddress(address);
            printer.Show(person.GetAddress());
            printer.ShowByPointer(person.GetAddress());
            printer.ShowByReference(person.GetAddress());


            Console.WriteLine("Mutate \n");
            MixedSemantic.Mutator mutator = new MixedSemantic.Mutator();
            mutator.Mutate(name);
            mutator.MutateByPointer(name);
            mutator.MutateByReference(name);

            mutator.Mutate(person);
            mutator.MutateByPointer(person);
            mutator.MutateByReference(person);

            mutator.Mutate(person.GetAddress());
            mutator.MutateByPointer(person.GetAddress());
            mutator.MutateByReference(person.GetAddress());

            printer.Show(name);
            printer.ShowByPointer(name);
            printer.ShowByReference(name);

            printer.Show(person);
            printer.ShowByPointer(person);
            printer.ShowByReference(person);

            printer.Show(person.GetAddress());
            printer.ShowByPointer(person.GetAddress());
            printer.ShowByReference(person.GetAddress());

            Console.Write("Press any key to close programm...");
            Console.ReadKey();

        }
    }
}
