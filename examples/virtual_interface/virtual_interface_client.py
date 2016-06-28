
import VirtualInterface


def show(shape):
    shape.Show()

triangle = VirtualInterface.CreateTriangle()
shape0 = VirtualInterface.CreateCircle()
shape1 = VirtualInterface.CreateRectangle()

show(triangle)
show(shape0)
show(shape1)

# Manually delete these objects, because they are non-owning raw pointers
# del triangle
# del shape0
# del shape1
