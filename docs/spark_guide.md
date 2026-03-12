# Hướng dẫn Thuyết trình: Apache Spark Deep Dive

Tài liệu này hỗ trợ bạn trình bày 4 nội dung chính theo yêu cầu.

---

## 1. Viết và Triển khai ứng dụng Spark (Writing & Deploying)

### Cách viết ứng dụng
- **Ngôn ngữ hỗ trợ**: Scala (Gốc), Java, Python (PySpark), R.
- **Cấu trúc**: Luôn bắt đầu bằng `SparkSession`. Đây là điểm vào (entry point) để làm việc với DataFrame/Dataset API.

### Chế độ triển khai (Deployment Modes)
Spark có thể chạy trên nhiều trình quản lý cụm khác nhau:
1. **Standalone**: Bộ quản lý cụm đơn giản đi kèm với Spark (Chúng ta dùng trong lab này).
2. **Apache YARN**: Phổ biến trong các hệ sinh thái Hadoop.
3. **Kubernetes (K8s)**: Xu hướng hiện đại để quản lý tài nguyên linh hoạt.

**Deployment Mode: Client vs. Cluster**
- **Client mode**: Driver chạy ngay trên máy submit job. Phù hợp để debug.
- **Cluster mode**: Driver chạy bên trong cụm (Worker). Phù hợp cho production.

---

## 2. Các trường hợp sử dụng phổ biến (Common Use Cases)

- **ETL (Extract, Transform, Load)**: Xử lý và làm sạch dữ liệu khổng lồ nhanh hơn MapReduce.
- **Xử lý luồng (Streaming)**: Sử dụng Spark Streaming hoặc Structured Streaming để xử lý dữ liệu thời gian thực (ví dụ: phát hiện gian lận ngân hàng).
- **Machine Learning**: Thư viện MLlib cung cấp các thuật toán phân loại, hồi quy, phân cụm có khả năng mở rộng cực lớn.
- **Xử lý Đồ thị (Graph Processing)**: Thư viện GraphX để phân tích các mạng lưới liên kết phức tạp.

---

## 3. Thuật toán lặp trong Spark (Iterative Algorithms)

Đây là điểm "ăn tiền" nhất của Spark so với Hadoop MapReduce:
- **MapReduce**: Mỗi vòng lặp phải đọc dữ liệu từ đĩa, xử lý, rồi lại ghi xuống đĩa. Gây nghẽn I/O rất nặng.
- **Spark**: Cho phép lưu trữ dữ liệu trong **RAM (Caching/Persist)** giữa các vòng lặp. 
    - Kết quả của vòng lặp 1 được giữ lại trong bộ nhớ để vòng lặp 2 dùng ngay lập tức.
    - Giúp các thuật toán cần chạy nhiều lần (như PageRank, K-Means, Logistic Regression) nhanh hơn gấp 10-100 lần.

---

## 4. Demo: PageRank với tập dữ liệu Google

### Cách chạy Lab:
1. **Khởi động môi trường**:
   ```bash
   docker-compose up -d
   ```
2. **Submit Job Spark**:
   ```bash
   docker exec -it spark-master spark-submit --master spark://spark-master:7077 /opt/bitnami/spark/work/demo/pagerank_demo.py
   ```
3. **Quan sát Spark UI**:
   Mở trình duyệt tại: `http://localhost:8080` (Master UI) và `http://localhost:4040` (Job UI khi đang chạy).

### Kết quả mong đợi:
- Script sẽ đọc file `data/web-Google.txt`.
- Chạy 10 vòng lặp để cập nhật rank.
- In ra danh sách 10 trang web có thứ hạng cao nhất (quan trọng nhất) trong mạng lưới.
