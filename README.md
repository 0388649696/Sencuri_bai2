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
Trường hợp signed.pdf hợp lệ.
<img width="1424" height="652" alt="image" src="https://github.com/user-attachments/assets/45939191-8d0b-4f92-b6d8-18b015aad654" />
.
Trường hợp tampered.pdf đã bị phát hiện sửa đổi. 
Ở đây là bị sửa theo phương pháp lật bit
<img width="1445" height="833" alt="image" src="https://github.com/user-attachments/assets/957baaeb-10c6-4fde-855f-501c2cc92953" />

### Rủi ro có thể gặp phải nếu bị tấn công:
#### Padding oracle
Vì mã dùng RSA với padding PKCS#1 v1.5 làm cơ chế ký
+ Nếu có oracle, kẻ tấn công có thể phục hồi khóa bí mật hoặc plaintext, hoặc tấn công nhằm phá vỡ tính bảo mật của dữ liệu được mã hóa/đã ký.
+ Trong ngữ cảnh PDF signing/CMS, việc tiết lộ thông tin lỗi chi tiết trong quá trình verify/parse PKCS#7 có thể làm lộ vector tấn công.
- Biện pháp giảm thiểu:
+ Dùng RSA-PSS (nếu có hỗ trợ) hoặc ECC cho chữ ký thay cho PKCS#1 v1.5.
+ Tránh lộ thông báo lỗi chi tiết cho input không hợp lệ — logs nội bộ OK, nhưng responses ra ngoài/HTTP nên generic.

#### Replay
có rủi ro replay cụ thể vì mã không dùng TSA (timestamp third-party) và không gắn bất kỳ cơ chế chống tái sử dụng nào cho chữ ký/tài liệu.
Do đó, một chữ ký hợp lệ từ thời điểm A có thể bị tái sử dụng (replay) ở thời điểm B để chứng minh điều gì đó đã xảy ra, hoặc một attacker có thể gửi lại signature/file trong bối cảnh khác.
- Biện pháp giảm thiểu:
+ Sử dụng TSA (RFC 3161) để nhận timestamp token từ bên thứ ba đáng tin cậy; timestamp này là bằng chứng thời gian khách quan, khó bị làm giả.
+ Gắn unique document identifier (UUID/hash) inside signedAttrs — đảm bảo chữ ký ràng buộc chặt với một ID duy nhất của tài liệu.
+ Lưu evidence/manifest: lưu log dấu thời gian, hash file, và metadata ký (serial số chứng chỉ, nonce) ở kho chứng cứ trung tâm; khi verify, so sánh với bản registry.
+ Policy xử lý detached signatures: không chấp nhận signature nếu metadata/hash không khớp hoặc nếu đã bị dùng trước đó mà policy cấm reuse.
+ Sử dụng nonces trong các protocol giao tiếp (nếu chữ ký phát sinh qua giao thức) để ngăn replay trong phiên.



