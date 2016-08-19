using System;

public class ObjectParameter {
    static void Main() {
        Example.Document main_document = new Example.Document();
        main_document.Show();

        Example.Page new_page = new Example.Page();
        main_document.SetPage(new_page);
        main_document.Show();

        {
            Example.Page existing_page = main_document.GetPage();
            existing_page.SetWidth(777);
            main_document.Show();
        }
    }
}