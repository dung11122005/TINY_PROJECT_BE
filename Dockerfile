# Dùng Python 3.11 slim
FROM python:3.11-slim

# Đặt thư mục làm việc
WORKDIR /app

# Cài các package hệ thống cần thiết để build mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements.txt
COPY requirements.txt .

# Cài dependencies Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code
COPY . .

# Expose cổng cho Django
EXPOSE 8000

# Lệnh mặc định
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
