using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Linq;
using System.Text;

namespace DownCastExample
{
    class Program
    {
        static void show(Example.IShapePtr shape)
        {
            if (shape.IsNull())
            {
                Console.WriteLine("Shape is null");
                return;
            }
            shape.Show();
            if (Example.IPolygonPtr.DownCast(shape).IsNotNull())
            {
                Console.WriteLine("IPolygon");
                Example.IPolygonPtr polygon = Example.IPolygonPtr.DownCast(shape);
                Console.WriteLine("number of points = " + polygon.GetPointsCount());
            }
            if (Example.ITrianglePtr.DownCast(shape).IsNotNull())
            {
                Console.WriteLine("ITriangle");
                Example.ITrianglePtr triangle = Example.ITrianglePtr.DownCast(shape);
                triangle.SetPoints(-1, 1, 5, 6, 10, 15);
            }
            if (Example.ISquarePtr.DownCast(shape).IsNotNull())
            {
                Console.WriteLine("ISquare");
                Example.ISquarePtr square = Example.ISquarePtr.DownCast(shape);
                square.SetSize(3.14);
            }
            if (Example.ICirclePtr.DownCast(shape).IsNotNull())
            {
                Console.WriteLine("ICircle");
                Example.ICirclePtr circle = Example.ICirclePtr.DownCast(shape);
                circle.SetRadius(7.77);
            }
        }

        static void Main(string[] args)
        {
            try
            {
                Example.IShapePtr null_shape = Example.IShapePtr.Null();
                Example.IShapePtr triangle = Example.Functions.CreateTriangle();
                Example.IShapePtr shape0 = Example.Functions.CreateCircle();
                Example.IShapePtr shape1 = Example.Functions.CreateSquare();


                Console.WriteLine();
                Console.WriteLine("Null shape.");
                show(null_shape);


                Console.WriteLine();
                Console.WriteLine("The first pass.");
                show(triangle);
                show(shape0);
                show(shape1);


                Console.WriteLine();
                Console.WriteLine("The second pass.");
                show(triangle);
                show(shape0);
                show(shape1);
                Console.WriteLine();
            }
            catch (Exception e)
            {
                Console.WriteLine("{0} Second exception caught.", e);
            }
        }
    }
}
