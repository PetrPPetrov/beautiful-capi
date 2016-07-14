using System;

public class VirtualInterface {
    static void Main() {
        Example.IShape triangle = ExampleNS.CreateTriangle();
        Example.IShape shape0 = ExampleNS.CreateCircle();
        Example.IShape shape1 = ExampleNS.CreateRectangle();

        show(triangle);
        show(shape0);
        show(shape1);
    }
    
    static void show(Example.IShape shape)
    {
        shape.Show();
    }
}