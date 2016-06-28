
import PointSet

point_set = PointSet.PointSet()
point_set.SetName("Pointy")

points = PointSet.Points()
points.Reserve(3)
points.PushBack(PointSet.Position(1, 0, 0))
points.PushBack(PointSet.Position(0, 1, 0))
points.PushBack(PointSet.Position(0, 0, 1))
point_set.SetPoints(points)

print("PointSet '{name}'".format(name=point_set.GetName()))
other_points = point_set.GetPoints()

for index in xrange(0, other_points.Size()):
    pos = other_points.GetElement(index)
    print("\tpoint #{idx} ({x}, {y}, {z})".format(idx=index, x=pos.GetX(), y=pos.GetY(), z=pos.GetZ()))
