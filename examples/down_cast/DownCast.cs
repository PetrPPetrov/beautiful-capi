using System;

public class DownCast {
    static void Main() {
        Example.IShape triangle = ExampleNS.CreateTriangle();
        Example.IShape shape0 = ExampleNS.CreateCircle();
        Example.IShape shape1 = ExampleNS.CreateSquare();

        System.Console.WriteLine("\nThe first pass.");
        Show(triangle);
        Show(shape0);
        Show(shape1);

        System.Console.WriteLine("\nThe second pass.");
        Show(triangle);
        Show(shape0);
        Show(shape1);
    }

    static void Show(Example.IShape shape)
    {
        shape.Show();

        //if (shape is Example.IPolygon)
        if (ExampleNS.IShape_to_IPolygon(shape) != null)
        {
            System.Console.WriteLine("IPolygon");
            Example.IPolygon polygon = ExampleNS.IShape_to_IPolygon(shape);
            //Example.IPolygon polygon = shape as Example.IPolygon;
            System.Console.WriteLine("number of points = " + Convert.ToString(polygon.GetPointsCount()));
        }

        //if (shape is Example.ITriangle)
        if (ExampleNS.IShape_to_ITriangle(shape) != null)
        {
            System.Console.WriteLine("ITriangle");
            Example.ITriangle triangle = ExampleNS.IShape_to_ITriangle(shape);
            triangle.SetPoints(-1, 1, 5, 6, 10, 15);
        }

        //if (shape is Example.ISquare)
        if (ExampleNS.IShape_to_ISquare(shape) != null)
        {
            System.Console.WriteLine("ISquare");
            Example.ISquare square = ExampleNS.IShape_to_ISquare(shape);
            square.SetSize(3.14);
        }

        //if (shape is Example.ICircle)
        if (ExampleNS.IShape_to_ICircle(shape) != null)
        {
            System.Console.WriteLine("ICircle");
            Example.ICircle circle = ExampleNS.IShape_to_ICircle(shape);
            circle.SetRadius(7.77);
        }
    }
}