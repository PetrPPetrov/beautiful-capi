using System;

public class CustomSuffix {
    static void Main() {
        hello_world.printer printer = new hello_world.printer(); // It has copy semantic (value semantic)
        printer.show();

        using (hello_world.scanner scanner = new hello_world.scanner()) // It has non-owning pointer (raw pointer) semantic
        {
            if (scanner == null)
            {
                System.Console.WriteLine("Error, scanner is null!");
                return;
            }
            scanner.scan();
        }

        hello_world.plotter plotter = new hello_world.plotter(); // It has reference counted smart pointer semantic
        if (plotter == null)
        {
            System.Console.WriteLine("Error, plotter is null!");
            return;
        }
        if (plotter != null)
        {
            plotter.draw();
        }

    }
}