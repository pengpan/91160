# 健康160全自动刷票程序

## 使用

需要运行在 python 3.6 以上版本（其它版本暂未测试)

**1. 安装依赖**
```bash
git clone https://github.com/pengpan/91160

pip install -r requirements.txt
```

**2. 启动程序**
```bash
python main.py
```

## Docker 使用

**1. 构建镜像**
```bash
docker build -t 91160:latest .
```

**2. 运行镜像**
```bash
docker run --rm --name 91160 -it 91160:latest
```
