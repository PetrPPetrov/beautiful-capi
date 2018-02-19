using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace template
{
    class Program
    {
        static void dump<T>(Example.Position<T> position)
        {
            Console.Write("X: ");
            dump(position.GetX());
            Console.Write("Y: ");
            dump(position.GetY());
            Console.Write("Z: ");
            dump(position.GetZ());
            Console.WriteLine();
        }

        static void dump<T>(Example.Position4D<T> position)
        {
            dump((Example.Position<T>)position);
            Console.Write("W: ");
            dump(position.GetW());
            Console.WriteLine();
        }

        static void dump<T>(Example.VectorOf<T> vector)
        {
            Console.WriteLine("Vector has " + vector.GetSize() + " elements");
            for (int i = 0; i < vector.GetSize(); ++i)
            {
                dump((T)vector.GetItem(i));
            }
            Console.WriteLine();
        }

        static void dump<T>(Example.ModelPtr<T> model)
        {
            Console.Write("Model");
            Console.Write("name: " + model.GetName() );
            dump((Example.Position<T>)model.GetPosition());
        }

        static void dump<T>(Example.VectorOfObjectsPtr<T> vector)
        {
            Console.Write("Vector has " + vector.GetSize() + " elements");
            for (int i = 0; i < vector.GetSize(); ++i)
            {
                dump((T)vector.GetItem(i));
            }
            Console.WriteLine();
        }

        static void dump<T>(Example.VectorOfObjectsDerivedPtr<T> vector)
        {
            Console.Write("VectorOfObjectsDerivedPtr");
            dump((Example.VectorOfObjectsPtr<T>)vector);
        }
        
        static void dump<SimpleType>(SimpleType value)
        {
            Console.Write(value + " ");
        }

        static void Main(string[] args)
        {
            {
                var vector = new Example.VectorOf<int>();
                vector.PushBack(5);
                vector.PushBack(7);
                vector.PushBack(3);
                vector.PushBack(10);
                dump(vector);

                var vector2 = new Example.VectorOf<double>();
                vector2.PushBack(3.14);
                vector2.PushBack(2.71);
                dump(vector2);

                var position = new Example.Position<float>();
                position.SetY(15.5f);
                dump(position);

                var position2 = new Example.Position4D<double>();
                position2.SetW(0.5);
                dump(position2);

                var vector3 = new Example.VectorOf<Example.Position4D<float>>();
                vector3.PushBack(new Example.Position4D<float>());
                vector3.PushBack(new Example.Position4D<float>());
                dump(vector3);

                var vectorz = new Example.VectorOf<Example.VectorOf<Example.Position4D<float>>>();
                vectorz.PushBack(vector3);
                vectorz.PushBack(vector3);
                dump(vectorz);

                var model_vector = new Example.VectorOfObjectsDerivedPtr<Example.ModelPtr<double>>();
                var model1 = new Example.ModelPtr<double>();
                var model2 = new Example.ModelPtr<double>();
                model1.SetName("model1");
                model2.SetName("model2");

                model_vector.PushBack(model1);
                model_vector.PushBack(model2);
                dump(model_vector);

                Console.Write(model_vector.GetA());

                var dummy = new Example.VectorOf<char>();
                dump(dummy);
            }
            GC.Collect();
            GC.WaitForPendingFinalizers();
            Console.Write("Press any key to close programm...");
            Console.ReadKey();

        }
    }
}
