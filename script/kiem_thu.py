import sys
sys.stdout.reconfigure(encoding='utf-8')

from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import validate_pdf_signature
from pyhanko_certvalidator import ValidationContext
from pyhanko.sign.general import load_cert_from_pemder

# --- Đường dẫn tới file PDF và chứng chỉ ---
SIGNED_PDF = r"D:\Apache24\anhtu\sencuri\pdf\signed.pdf"
TAMPERED_PDF = r"D:\Apache24\anhtu\sencuri\pdf\tampered.pdf"
CERT_PATH = r"D:\Apache24\anhtu\sencuri\keys\signer_cert.pem"

# --- Tạo ValidationContext từ chứng chỉ self-signed ---
vc = ValidationContext(trust_roots=[load_cert_from_pemder(CERT_PATH)])

def check_pdf_signature(pdf_path: str):
    """Kiểm tra chữ ký PDF và in kết quả."""
    print(f"\n=== Kiểm tra chữ ký PDF: {pdf_path} ===")
    with open(pdf_path, "rb") as f:
        reader = PdfFileReader(f)
        if not reader.embedded_signatures:
            print("❌ PDF không có chữ ký.")
            return
        sig = reader.embedded_signatures[0]
        status = validate_pdf_signature(sig, vc)
        print(status.summary())
        if status.trusted:
            print("✅ Chữ ký hợp lệ và chứng chỉ tin cậy!")
        else:
            print("❌ Chữ ký không hợp lệ hoặc chứng chỉ đã bị ai đó động tay.")

# --- Kiểm tra signed.pdf ---
check_pdf_signature(SIGNED_PDF)

# --- Kiểm tra tampered.pdf ---
check_pdf_signature(TAMPERED_PDF)
