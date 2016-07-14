using System;

public class BoostSharedPtr {
    static void Main() {
        Example.PrinterSharedPtr printer = create_printer();
        printer.Show("from main()");
        f1(printer);
    }

    static void f1(Example.PrinterSharedPtr p)
    {
        p.Show("from f1()");
    }

    static Example.PrinterSharedPtr create_printer()
    {
        Example.PrinterSharedPtr new_printer = new Example.PrinterSharedPtr();
        new_printer.Show("from create_printer()");
        return new_printer;
    }
}