# CHỮ KÝ SỐ TRONG FILE PDF
K225480106070

Chuẩn bị: 
1. Cài đặt môi trường: python -m pip install cryptography
2. Tạo một chữ ký (ảnh), có thể dùng https://smallpdf.com/vi/sign-pdf#r=sign -> chuky.jpg
3. Chuẩn bị PDF, chuyển bài đã làm "original.docx" sang PDF. Để đúng chuẩn thì mở lưu dạng "Microsoft Pirnt to PDF". Đồng thời đảm bảo nó chuẩn Hybrid: False -> sẽ được PDF sạch

# I. TẠO KHÓA RIÊNG VÀ CHỨNG CHỈ CÔNG KHAI
File thực hiện: tao_khoa.py
- Sinh khóa riêng (private key) bằng rsa.generate_private_key().
- Dùng khóa này để tự ký chứng chỉ (self-signed certificate) bằng SHA256.
- Lưu ra thư mục keys/:
  + signer_key.pem → khóa riêng (để ký).
  + signer_cert.pem → chứng chỉ công khai (để xác thực).
 
<img width="1373" height="823" alt="image" src="https://github.com/user-attachments/assets/e0283e86-045e-4808-8c9e-4d25ea513a51" />

# 2. KÝ FILE PDF
File thực hiện: sign_pdf.py
- Mở file original.pdf (tài liệu cần ký).
- Thêm trường chữ ký /SigField1 (AcroForm).
- Dùng SHA-256 để tạo messageDigest trên vùng /ByteRange.
- Tạo PKCS#7/CMS detached chứa:
 + messageDigest
 + signingTime
 + certificate chain
- Nhúng chữ ký này vào /Contents của PDF.
- Ghi lại file mới signed.pdf (incremental update).
<img width="1379" height="906" alt="Screenshot 2025-10-31 165137" src="https://github.com/user-attachments/assets/c4d857da-d6d7-4495-9601-30cc0e890de4" />

# 3. KIỂM TRA TÍNH HỢP LỆ CHỮ KÝ
File thực hiện: kiem_thu.py
<img width="1424" height="652" alt="image" src="https://github.com/user-attachments/assets/45939191-8d0b-4f92-b6d8-18b015aad654" />
.






