import PyPDF2
import os
import shutil
from time import sleep

book_dir=r"D:\AllDowns\newbooks"
needing_dir=r"D:\AllDowns\needingbooks"
def main():
    books=sorted(os.listdir(book_dir),key=lambda x: os.path.getmtime(os.path.join(book_dir, x)),reverse=True)
    check_str="123456789"
    for each in books:
        if each.endswith(".pdf"):
            book_path=book_dir+os.sep+each
            reader=PyPDF2.PdfFileReader(book_path)
            print("Book Name:{}".format(each))
            print("& Start Here &")
            titles=[]
            outlines=reader.getOutlines()
            if bool(outlines)==0:
                print("cao!")
                old_path=book_path
                new_path=needing_dir+os.sep+each
                os.rename(old_path,new_path)
                continue
            elif len(outlines)<=6:
                print("cao!")
                old_path=book_path
                new_path=needing_dir+os.sep+each
                os.rename(old_path,new_path)
                continue
            for each_page_bookmark_pack in reader.getOutlines():
                try:
                    title=each_page_bookmark_pack["/Title"]
                    # print(titles)
                    titles.append(each_page_bookmark_pack["/Title"])
                    titles_s="".join(titles[0:25])
                    if check_str in titles_s[10:21]:
                        print("cao!")
                        old_path=book_path
                        new_path=needing_dir+os.sep+each
                        os.rename(old_path,new_path)
                        break
                except TypeError:
                    print("Nested!")
                    break
print("done.")


if __name__ == '__main__':
    main()