
import DownCast


def show(shape):
    shape.Show()

    if DownCast.IShape_to_IPolygon(shape):
        print("IPolygon")
        polygon = DownCast.IShape_to_IPolygon(shape)
        print("number of points = {count}".format(count=polygon.GetPointsCount()))

    if DownCast.IShape_to_ITriangle(shape):
        print("ITriangle")
        triangle = DownCast.IShape_to_ITriangle(shape)
        triangle.SetPoints(-1, 1, 5, 6, 10, 15)

    if DownCast.IShape_to_ISquare(shape):
        print("ISquare")
        square = DownCast.IShape_to_ISquare(shape)
        square.SetSize(3.14)

    if DownCast.IShape_to_ICircle(shape):
        print("ICircle")
        circle = DownCast.IShape_to_ICircle(shape)
        circle.SetRadius(7.77)


def main():
    triangle = DownCast.CreateTriangle()
    shape0 = DownCast.CreateCircle()
    shape1 = DownCast.CreateSquare()

    print("\nThe first pass.")
    show(triangle)
    show(shape0)
    show(shape1)

    print("\nThe second pass.")
    show(triangle)
    show(shape0)
    show(shape1)

main()