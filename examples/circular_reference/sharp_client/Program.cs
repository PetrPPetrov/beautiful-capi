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
            var a_object = new Circular.ClassARawPtr();
            var b_object = new Circular.ClassBRawPtr();
            var a_object1 = new Circular.ClassARawPtr();
            var b_object1 = new Circular.ClassBRawPtr();

            a_object.SetB(b_object);
            b_object1.SetA(a_object1);

            Circular.ClassARawPtr tmp_object = b_object1.GetA();
            tmp_object.SetB(b_object);

            a_object.GetB().SetA(a_object1);

            a_object.Delete();
            b_object.Delete();
            a_object1.Delete();
            b_object1.Delete();

            Console.ReadKey();
        }
    }
}
