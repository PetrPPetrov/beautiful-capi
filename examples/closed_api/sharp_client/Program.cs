using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Linq;
using System.Text;
using System.Reflection;

namespace ConsoleApp1
{
    class Program
    {
        static void Dump(Example.Person person)
        {
            Console.WriteLine("==========");
            Console.WriteLine("Name: " + person.GetFirstName() + " " + person.GetLastName());
            Console.WriteLine("Age: " + person.GetAge());
            Console.WriteLine("Sex: " +  (person.GetSex() == Example.Person.ESex.male ? "Male" : "Female"));
        }
        static void Main(string[] args)
        {
            var famous_person = new Example.Person();
            famous_person.SetAge(26);
            famous_person.SetFirstName("Isaac");
            famous_person.SetLastName("Newton");
            famous_person.SetSex(Example.Person.ESex.male);
            Dump(famous_person);

            var teacher = new Example.Education.School.Teacher();
            teacher.SetFirstName("John");
            teacher.SetAge(25);
            teacher.SetSex(Example.Person.ESex.male);
            teacher.Teach();

            var professor = new Example.Education.A.University.Professor();
            professor.SetFirstName("Vanessa");
            professor.SetSex(Example.Person.ESex.female);
            professor.Do();

            Console.WriteLine("Done");

            Console.ReadKey();
        }
    }
}
