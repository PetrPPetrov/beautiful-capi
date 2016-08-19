
import BoostSharedPtr


def f1(p):
    p.Show("from f1()")


def create_printer():
    new_printer = BoostSharedPtr.PrinterSharedPtr()
    new_printer.Show("from create_printer()")
    return new_printer


def main():
    printer = create_printer()
    printer.Show("from main()")
    f1(printer)


main()