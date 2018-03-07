using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using DerivedFromAbstract;

namespace DerivedFormAbstractSharp
{
    class Program
    {
        static void Main(string[] args)
        {
            var bird = new DerivedFromAbstract.Bird("Worm");
            bird.Move();
            bird.Sound();

            var wolf = new DerivedFromAbstract.Wolf("Meat");
            wolf.Move();
            wolf.Sound();

            Console.WriteLine("==============");
            Console.WriteLine("Program ending");
            Console.ReadKey();
        }
    }
}
