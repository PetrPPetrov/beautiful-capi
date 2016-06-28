
import CircularReference

a_object = CircularReference.ClassA()
b_object = CircularReference.ClassB()
a_object1 = CircularReference.ClassA()
b_object1 = CircularReference.ClassB()

a_object.SetB(b_object)
b_object1.SetA(a_object1)

tmp_object = b_object1.GetA()
tmp_object.SetB(b_object)

a_object.GetB().SetA(a_object1) # We need to use "." operator here, as GetB() returns forward_pointer_holder<CircularReference.ClassB>