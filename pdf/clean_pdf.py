# pdf/check_hybrid.py có trách nhiệm kiểm tra xem file PDF có sử dụng hybrid xref hay không
# nếu Hybrid: False thì file PDF không dùng hybrid xref, có thể dùng để ký an toàn
from pyhanko.pdf_utils.reader import PdfFileReader
with open(r"D:\Apache24\anhtu\sencuri\pdf\original.pdf", "rb") as f:
    r = PdfFileReader(f)
    print("Hybrid:", r.xrefs.hybrid_xrefs_present)
