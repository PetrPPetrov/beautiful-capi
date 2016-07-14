using System;

public class PointSetExample {
    static void Main() {
        PointSet.PointSet point_set = new PointSet.PointSet();
        point_set.SetName("Pointy");
        {
            PointSet.Points points = new PointSet.Points();
            points.Reserve(3);
            points.PushBack( new PointSet.Position(1, 0, 0) );
            points.PushBack( new PointSet.Position(0, 1, 0) );
            points.PushBack( new PointSet.Position(0, 0, 1) );
            point_set.SetPoints(points);
        }

        {
            System.Console.WriteLine(String.Format("PointSet '{0}'", point_set.GetName()));
            PointSet.Points points = point_set.GetPoints();

            for (uint i = 0; i < points.Size() ; ++i)
            {
                PointSet.Position pos = points.GetElement(i);
                System.Console.WriteLine(String.Format("\tpoint #{0} ({1}, {2}, {3})", i, pos.GetX(), pos.GetY(), pos.GetZ()));
            }
        }

    }
}