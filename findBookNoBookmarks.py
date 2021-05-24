import PyPDF2
import os
import shutil
from time import sleep

from concurrent.futures import ThreadPoolExecutor

book_dir=r"D:\AllDowns\newbooks"
needing_dir=r"D:\AllDowns\newbooks\needingbooks"

fucking_dir=r"D:\AllDowns\newbooks\fuckingbooks"
good_dir=r"D:\AllDowns\newbooks\good"

if not os.path.exists(needing_dir):
    os.makedirs(needing_dir)

if not os.path.exists(fucking_dir):
    os.makedirs(fucking_dir)

if not os.path.exists(good_dir):
    os.makedirs(good_dir)

check_str="123456789"

def mv2dir(old_path,new_dir,book):
    new_path=new_dir+os.sep+book
    os.rename(old_path,new_path)

def check_one_book(book):
    book_path=book_dir+os.sep+book
    reader=PyPDF2.PdfFileReader(book_path)
    print("Book Name:{}".format(book))
    print("& Start Here &")
    titles=[]
    outlines=reader.getOutlines()
    if book.startswith("typetype1") and len(outlines)<=10:
        print("gan!")
        # mv2dir(book_path,fucking_dir,book)
        return 
    elif len(outlines)==0:
        print("cao!")
        mv2dir(book_path,needing_dir,book)
        return 
    elif len(outlines)<=10:
        suspect=1
        for each_page_bookmark_pack in outlines:
            try:
                title=each_page_bookmark_pack["/Title"]
                # print(titles)
                titles.append(each_page_bookmark_pack["/Title"])
                titles_s="".join(titles[0:25])
            except TypeError:
                print("Nested!")
                suspect=0
                mv2dir(book_path,good_dir,book)
                return 
        if suspect==1:
            print("cao!")
            mv2dir(book_path,needing_dir,book)
            return 
    for each_page_bookmark_pack in outlines:
        try:
            title=each_page_bookmark_pack["/Title"]
            # print(titles)
            titles.append(each_page_bookmark_pack["/Title"])
            titles_s="".join(titles[0:25])
            if check_str in titles_s:
                print("cao!")
                mv2dir(book_path,needing_dir,book)
                return
        except TypeError:
            print("Nested!")
            return 

def main():
    thread_pool = ThreadPoolExecutor(max_workers=5, thread_name_prefix="fbnb_")
    books=sorted(os.listdir(book_dir),key=lambda x: os.path.getmtime(os.path.join(book_dir, x)),reverse=True)
    for each_book in books:
        if each_book.endswith(".pdf"):
            future=thread_pool.submit(check_one_book,each_book)
    thread_pool.shutdown(wait=False)
    print("ThreadPool: All done.")
print("done.")


if __name__ == '__main__':
    main()