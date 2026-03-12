# Lab 02: Apache Spark - PageRank Demo

Dự án này chứa đầy đủ nội dung cho bài thuyết trình số 2 về Apache Spark.

## Cấu trúc thư mục
- `data/`: Chứa bộ dữ liệu `web-Google.txt`.
- `demo/`: Chứa mã nguồn PySpark `pagerank_demo.py`.
- `docs/`: Chứa tài liệu hướng dẫn thuyết trình `spark_guide.md`.
- `docker-compose.yml`: Cấu hình cụm Spark.

## Hướng dẫn chạy nhanh
1. **Khởi động Spark Cluster**:
   ```bash
   docker-compose up -d
   ```
2. **Chạy demo PageRank**:
   ```bash
   docker exec -u root -it -e HOME=/root spark-master spark-submit \
     --master spark://spark-master:7077 \
     --conf "spark.driver.extraJavaOptions=-Divy.home=/tmp -Duser.home=/tmp" \
     --conf "spark.executor.extraJavaOptions=-Divy.home=/tmp -Duser.home=/tmp" \
     /opt/bitnami/spark/work/demo/pagerank_demo.py
   ```
3. **Kiểm tra kết quả**:
   - **Xếp hạng**: Terminal sẽ in ra **Top 10 Ranked Pages**.
   - **File kết quả**: Xem đủ Top 100 tại `data/pagerank_results.txt`.
   - **Giao diện**: Xem `http://localhost:8080` (Master) và `http://localhost:4040` (chỉ khi đang chạy).

## Tài liệu thuyết trình
Bạn hãy mở file `docs/spark_guide.md` để xem nội dung chi tiết phục vụ cho việc trình bày 4 yêu cầu của bài.
