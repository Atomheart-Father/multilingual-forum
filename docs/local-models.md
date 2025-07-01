# 🤖 本地翻译模型部署指南

本文档介绍如何在多语言论坛中配置和使用本地翻译模型，实现离线翻译、隐私保护和成本控制。

## 🎯 本地模型的优势

- **🔒 隐私保护**: 数据不离开本地服务器
- **💰 成本控制**: 避免API调用费用
- **⚡ 离线使用**: 无需网络连接
- **🎛️ 完全控制**: 自定义模型和参数

## 🔧 支持的模型类型

### 1. Hugging Face Transformers模型

最简单的入门选择，支持多种预训练翻译模型。

#### 安装依赖
```bash
pip install torch transformers sentencepiece sacremoses
```

#### 推荐模型

**通用翻译模型：**
- `facebook/m2m100_418M` - 支持100种语言的轻量模型
- `facebook/m2m100_1.2B` - 更高质量的大型模型

**特定语言对模型（Helsinki-NLP）：**
- `helsinki-nlp/opus-mt-en-zh` - 英文到中文
- `helsinki-nlp/opus-mt-zh-en` - 中文到英文
- `helsinki-nlp/opus-mt-en-de` - 英文到德文
- `helsinki-nlp/opus-mt-fr-en` - 法文到英文

#### 配置示例
```env
LOCAL_MODEL_TYPE=transformers
LOCAL_MODEL_NAME=facebook/m2m100_418M
```

### 2. Ollama本地大语言模型

使用大语言模型进行翻译，质量更高但资源消耗更大。

#### 安装Ollama
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# 启动服务
ollama serve
```

#### 下载模型
```bash
# 下载多语言模型
ollama pull llama2:7b
ollama pull codellama:7b
ollama pull mistral:7b

# 下载中文优化模型
ollama pull qwen:7b
ollama pull chatglm3:6b
```

#### 配置示例
```env
LOCAL_MODEL_TYPE=ollama
LOCAL_MODEL_NAME=llama2:7b
OLLAMA_SERVER_URL=http://localhost:11434
```

### 3. 自定义模型服务器

部署自己的翻译模型服务器。

#### 配置示例
```env
LOCAL_MODEL_TYPE=custom
LOCAL_MODEL_SERVER_URL=http://localhost:8080
CUSTOM_MODEL_PATH=/path/to/your/model
```

## 🚀 快速开始

### 1. 选择模型类型

根据您的需求选择合适的模型：

| 模型类型 | 质量 | 速度 | 资源需求 | 适用场景 |
|---------|------|------|----------|----------|
| Helsinki-NLP | 中 | 快 | 低 | 特定语言对，生产环境 |
| M2M100 | 高 | 中 | 中 | 多语言支持，中等规模 |
| Ollama (LLM) | 很高 | 慢 | 高 | 高质量翻译，有GPU |

### 2. 安装依赖

```bash
# 基础依赖
pip install torch transformers

# 如果使用GPU
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 3. 配置环境变量

编辑 `server/.env` 文件：

```env
# 启用本地模型
LOCAL_MODEL_TYPE=transformers
LOCAL_MODEL_NAME=facebook/m2m100_418M
```

### 4. 测试翻译

```bash
curl -X POST http://localhost:3001/api/translate/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, world!",
    "target_lang": "zh",
    "service": "local"
  }'
```

## 📊 性能优化

### 1. GPU加速

```python
# 检查GPU可用性
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")
```

### 2. 模型缓存

模型会自动缓存到：
- Windows: `C:\Users\{username}\.cache\huggingface\transformers`
- macOS/Linux: `~/.cache/huggingface/transformers`

### 3. 批量翻译

对于大量文本，考虑实现批量翻译接口：

```python
# 批量翻译示例
async def batch_translate(texts: List[str], target_lang: str):
    # 实现批量处理逻辑
    pass
```

## 🛠️ 高级配置

### 1. 自定义模型服务器

创建独立的模型服务器：

```python
# model_server.py
from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()
translator = pipeline("translation", model="your-model")

@app.post("/translate")
async def translate(request: dict):
    result = translator(request["text"])
    return {"translated_text": result[0]["translation_text"]}
```

### 2. 模型微调

针对特定领域微调模型：

```python
# 示例：针对技术文档微调
from transformers import AutoModelForSeq2SeqLM, Trainer

# 加载预训练模型
model = AutoModelForSeq2SeqLM.from_pretrained("helsinki-nlp/opus-mt-en-zh")

# 准备训练数据
# ...

# 微调训练
trainer = Trainer(model=model, train_dataset=train_dataset)
trainer.train()
```

### 3. 多模型负载均衡

部署多个模型实例进行负载均衡：

```yaml
# docker-compose.yml
services:
  model-server-1:
    image: your-model-server
    ports: ["8001:8000"]
  
  model-server-2:
    image: your-model-server
    ports: ["8002:8000"]
  
  nginx:
    image: nginx
    # 配置负载均衡
```

## 🔍 故障排除

### 常见问题

1. **内存不足**
   ```bash
   # 使用更小的模型
   LOCAL_MODEL_NAME=helsinki-nlp/opus-mt-en-zh
   ```

2. **GPU不可用**
   ```bash
   # 安装CUDA版本的PyTorch
   pip install torch --index-url https://download.pytorch.org/whl/cu118
   ```

3. **模型下载失败**
   ```bash
   # 设置镜像源
   export HF_ENDPOINT=https://hf-mirror.com
   ```

### 监控和日志

```python
# 添加性能监控
import time
import psutil

def monitor_translation_performance():
    start_time = time.time()
    memory_before = psutil.Process().memory_info().rss
    
    # 执行翻译
    result = translate(text)
    
    end_time = time.time()
    memory_after = psutil.Process().memory_info().rss
    
    logger.info(f"Translation took {end_time - start_time:.2f}s")
    logger.info(f"Memory used: {(memory_after - memory_before) / 1024 / 1024:.2f}MB")
```

## 📚 更多资源

- [Hugging Face模型库](https://huggingface.co/models?pipeline_tag=translation)
- [Ollama模型库](https://ollama.ai/library)
- [PyTorch官方文档](https://pytorch.org/docs/)
- [Transformers文档](https://huggingface.co/docs/transformers)

## 🤝 贡献

欢迎提交新的模型集成和优化建议！ 