import os, sys
from tkinter import filedialog
from tkinter import *
from chardet.universaldetector import UniversalDetector
import mimetypes
import terminal

def main():
    root = Tk()
    root.withdraw()
    rootdir = filedialog.askdirectory()
    print(f'Current directory is: {rootdir}')
    text = input("What search terms are you looking for?")
    files_to_search=[]
    for root, subFolder, files in os.walk(rootdir):
        for file in files:
            filepath = os.path.join(root,file)
            detector = UniversalDetector()
            
            for line in open(filepath, 'rb'):
                detector.feed(line)
                if detector.done: break
            detector.close()
            
            if detector.result['encoding'] != None:
                if 'windows' in detector.result['encoding'] or 'Windows' in detector.result['encoding']:
                    detector.result['encoding'] = 'cp'+detector.result['encoding'][8:]
            try:
                assert os.path.isfile(filepath)
                if detector.result['encoding'] != None and detector.result['confidence'] > .85:
                    print(f"Now evaluating {filepath}.")
                    with open(filepath, 'r', encoding=detector.result['encoding']) as file:
                        content = file.read()
                        if text in content:
                            files_to_search.append(file)
                            print(f"FOUND ONE\n{file}\n")
                        else: pass
                else:
                    pass
            except PermissionError as e:
                #print(e)
                pass
    print("File search complete. Printing results.")
    for file in files_to_search:
        print(file)
main()
