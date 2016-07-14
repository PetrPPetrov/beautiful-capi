using System;

public class CircularReference {
    static void Main() {
        Circular.ClassA a_object = new Circular.ClassA();
        Circular.ClassB b_object = new Circular.ClassB();
        Circular.ClassA a_object1 = new Circular.ClassA();
        Circular.ClassB b_object1 = new Circular.ClassB();

        a_object.SetB(b_object);
        b_object1.SetA(a_object1);

        Circular.ClassA tmp_object = b_object1.GetA();
        tmp_object.SetB(b_object);

        a_object.GetB().SetA(a_object1);
    }
}
