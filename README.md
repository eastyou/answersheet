# answersheet

[![CI](https://github.com/eastyou/answersheet/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/answersheet/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](pyproject.toml)

给老师用的选择题答题卡生成器：给一个题量和选项数，一条命令生成 A4 可打印答题卡。**零依赖，不联网，打印即用。**

每页默认两栏、每栏 30 题，题目多了自动分页；选项圆圈按 A~F 自动编号，顶部留出姓名、班级、学号、日期填写栏。

## 特性

- **按题量生成**：`-q` 支持 1~200 题，自动分栏分页
- **选项可调**：`--options 2~6`，字母从 A 到 F 自动截取
- **分栏灵活**：`--columns 1~4`，窄栏适合低年级，宽栏适合大题量
- **涂卡圆圈**：每题一组圆形气泡，间距按 A4 纵向排版调好
- **信息栏**：姓名、班级、学号、日期四条填写线
- **科目可选**：`--subject 语文` 显示在标题下方
- **页脚统计**：显示页码、总题数、每题选项数，方便核对
- **参数校验**：题量、选项数、分栏数越界都会给出中文提示和退出码 2
- **44 个单元测试**：覆盖参数校验、分页分栏、渲染与命令行

## 安装

```bash
pip install answersheet
```

也可以直接下载源码，在项目目录里运行：

```bash
python -m answersheet --help
```

## 用法

生成 50 题、每题 4 个选项、两栏的答题卡：

```bash
python -m answersheet -q 50 --options 4 --columns 2 --subject 语文 -o 答题卡.html
```

生成 70 题、单栏、每题 2 个选项的答题卡（自动分 3 页）：

```bash
python -m answersheet -q 70 --options 2 --columns 1 -o 判断题答题卡.html
```

### 参数

| 参数 | 说明 | 默认 |
| --- | --- | --- |
| `-o, --output` | 输出 HTML 路径 | `答题卡.html` |
| `-q, --questions` | 题目数量 1~200 | `50` |
| `--options` | 每题选项数 2~6 | `4` |
| `--columns` | 分栏数 1~4 | `2` |
| `--subject` | 科目名称 | 空 |
| `--title` | 页面标题 | `答题卡` |

### 每页容量

每栏固定 30 行，所以每页容量 = 分栏数 × 30：

| 分栏数 | 每页题数 | 100 题需要 |
| --- | --- | --- |
| 1 | 30 | 4 页 |
| 2 | 60 | 2 页 |
| 3 | 90 | 2 页 |
| 4 | 120 | 1 页 |

## 打印

用浏览器打开生成的 HTML，按 `Ctrl/Cmd + P`：

- 纸张：A4 纵向
- 边距：无 / 默认
- 勾选「背景图形」，提示条底色才会打印

建议先打印一张让学生试涂，确认圆圈大小适合本班使用的铅笔。

## 项目结构

```text
answersheet/
├── answersheet/
│   ├── model.py    # 参数校验、选项字母与分栏分页
│   ├── render.py   # A4 答题卡排版
│   └── cli.py      # 命令行入口
└── tests/          # 44 个单元测试
```

## 开发

```bash
python -m unittest discover -s tests
```

## 许可证

[MIT](LICENSE) © 2026 eastyou
