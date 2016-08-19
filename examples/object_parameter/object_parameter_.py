
import ObjectParameter

main_document = ObjectParameter.Document()
main_document.Show()

new_page = ObjectParameter.Page()
main_document.SetPage(new_page)
main_document.Show()

existing_page = main_document.GetPage()
existing_page.SetWidth(777)
main_document.Show()
