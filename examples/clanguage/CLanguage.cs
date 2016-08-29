using System;

public class CopySemantic {
    static void Main() {
        Example.Printer printer = new Example.Printer();
        printer.Show("from main()");
        f1(printer);
    }
    
    static void f1(Example.Printer p)
    {
        p.Show("from f1()");
    }
}