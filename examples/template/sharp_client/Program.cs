using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace template
{
    class Program
    {
        static void Main(string[] args)
        {            
            var vector = new Example.VectorOf<int>();
            vector.PushBack(5);
            vector.PushBack(7);
            vector.PushBack(3);
            vector.PushBack(10);
            vector.dump();

            var vector2 = new Example.VectorOf<double>();
            vector2.PushBack(3.14);
            vector2.PushBack(2.71);
            vector2.dump();

            var position = new Example.Position<float>();
            position.SetY(15.5f);
            position.dump();

            var position2 = new Example.Position4D<double>();
            position2.SetW(0.5);
            position2.dump();

            var vector3 = new Example.VectorOf<Example.Position4D<float>>();
            vector3.PushBack(new Example.Position4D<float>());
            vector3.PushBack(new Example.Position4D<float>());
            vector3.dump();

            var vectorz = new Example.VectorOf<Example.VectorOf<Example.Position4D<float>>>();
            vectorz.PushBack(vector3);
            vectorz.PushBack(vector3);
            vectorz.dump();

            var model_vector = new Example.VectorOfObjectsDerivedPtr<Example.ModelPtr<double>>();
            var model1 = new Example.ModelPtr<double>();
            var model2 = new Example.ModelPtr<double>();
            model1.SetName("model1");
            model2.SetName("model2");

            model_vector.PushBack(model1);
            model_vector.PushBack(model2);
            model_vector.dump();

            Console.Write(model_vector.GetA());

            var dummy = new Example.VectorOf<char>();
            dummy.dump();
            
            GC.Collect();
            GC.WaitForPendingFinalizers();

        }
    }
}
