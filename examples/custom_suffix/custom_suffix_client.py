
import CustomSuffix

printer = CustomSuffix.printer()  # It has copy semantic (value semantic)
printer.show()

scanner = CustomSuffix.scanner()  # It has non-owning pointer (raw pointer) semantic
if not scanner:
    print('Error, scanner is None!')
    exit()

scanner.scan()
# del scanner  # We need to manually deallocate object from non-owning pointer

plotter = CustomSuffix.plotter()  # It has reference counted smart pointer semantic
if not plotter:
    print('Error, plotter is None!')
    exit()

if plotter:
    plotter.draw()
