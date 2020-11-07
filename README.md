# 健康160全自动挂号脚本

[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fpengpan%2F91160%2Fbadge&style=flat)](https://actions-badge.atrox.dev/pengpan/91160/goto)

## 规划
- [x] 实现基本功能
- [ ] 动态选择就诊人
- [ ] 接入IP池刷号
- [ ] 实现定时抢号

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
docker run --rm -it 91160:latest
```
