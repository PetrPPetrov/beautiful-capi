using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace object_parameter_sharp_clayshaker
{
    class Program
    {
        static void Main(string[] args)
        {
            var main_doc = new Example.DocumentPtr();
            main_doc.Show();

            var new_page = new Example.PagePtr();
            main_doc.SetPage(new_page);
            main_doc.Show();

            {
                var existing_page = new Example.PagePtr();
                existing_page = main_doc.GetPage();
                existing_page.SetWidth(777);
                main_doc.Show();
            }

            Console.WriteLine("|Азино три топора {777}|");
            Console.ReadKey();
        }
    }
}
