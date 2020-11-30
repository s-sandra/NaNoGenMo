from PyPDF2 import PdfFileMerger
import sys


novel_name = sys.argv[1]
pdfs = sys.argv[2:]
merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write(novel_name)
merger.close()
