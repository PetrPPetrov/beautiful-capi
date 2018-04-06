using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Linq;
using System.Text;

namespace ConsoleApp1
{
    class Program
    {
        static void show(Example.IShapeRawPtr shape)
        {
            shape.Show();
        }

        static void Main(string[] args)
        {
            Example.IShapeRawPtr triangle = Example.Functions.CreateTriangle();
            Example.IShapeRawPtr shape0 = Example.Functions.CreateCircle();
            Example.IShapeRawPtr shape1 = Example.Functions.CreateRectangle();

            show(triangle);
            show(shape0);
            show(shape1);

            // Manually delete these objects, because they are non-owning raw pointers
            triangle.Delete();
            shape0.Delete();
            shape1.Delete();

            Console.ReadKey();
        }
    }
}
