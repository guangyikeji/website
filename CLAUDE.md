# Claude Code 项目配置

## GitHub Pages 部署步骤

### 推送代码到GitHub
```bash
# 添加并提交所有更改
git add .
git commit -m "更新网站内容"

# 推送到GitHub（使用已配置的token）
git push origin main
```

### GitHub仓库信息
- 仓库地址: https://github.com/guangyikeji/website
- 网站地址: https://guangyikeji.github.io/website
- 分支: main

### 注意事项
- 推送后等待2-5分钟GitHub Pages会自动更新网站
- 确保GitHub Pages设置为从main分支的根目录部署
- HTTPS已启用，所有访问会自动加密

## 文档阅读经验总结

### 直接可读文件类型
- **HTML/CSS/JS**: 使用 Read 工具直接读取
- **TXT/MD**: 使用 Read 工具直接读取
- **PDF**: Read 工具支持，可视觉化显示内容
- **图片**: Read 工具支持，JPG/PNG等格式可直接查看

### 二进制文件处理方法

#### PPT/PPTX文件
```bash
# 方法1: 使用Task工具调用专门的代理
# 代理会使用Python解析PPTX文件（本质是ZIP格式）
# 可提取所有幻灯片的文本内容

# 方法2: 检查文件结构
file *.pptx  # 确认文件类型
```

#### DOC/DOCX文件
```bash
# 同样使用Task工具调用专门代理
# 可处理Word文档的文本内容提取
```

### 综合文档分析流程
1. **先用Read工具**尝试直接读取所有文件
2. **识别无法读取的文件类型**（通常是二进制格式）
3. **使用Task工具**调用general-purpose代理处理复杂文件
4. **整合所有信息**进行综合分析

### 最佳实践
- 对于混合文档类型的目录，先全量尝试Read工具
- 遇到二进制文件时，使用Task工具进行专门处理
- 图片文件优先使用Read工具查看，通常包含重要信息
- PDF文件优先使用Read工具，支持多页文档分析