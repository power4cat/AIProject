# -*- coding: utf-8 -*-
"""Generate AI-Robot architecture analysis PDF."""
import os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── register Chinese font ──
FONT = "Helvetica"
font_paths_to_try = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STSong.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
]
for fp in font_paths_to_try:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont("ChineseFont", fp, subfontIndex=0))
            FONT = "ChineseFont"
            print(f"Using font: {fp}")
            break
        except Exception as e:
            print(f"Font {fp} failed: {e}")
            continue

output_path = "/Users/shenma/Documents/project/AI-Robot/AI-Robot-Architecture-Analysis.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    topMargin=2.5 * cm,
    bottomMargin=2 * cm,
    leftMargin=2 * cm,
    rightMargin=2 * cm,
)

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="Title", fontName=FONT, fontSize=22, leading=30,
    textColor=HexColor("#1a1a2e"), spaceAfter=6, alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    name="SubTitle", fontName=FONT, fontSize=13, leading=18,
    textColor=HexColor("#555"), spaceAfter=18, alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    name="H1", fontName=FONT, fontSize=16, leading=22,
    textColor=HexColor("#16213e"), spaceBefore=18, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="H2", fontName=FONT, fontSize=13, leading=18,
    textColor=HexColor("#0f3460"), spaceBefore=12, spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="Body", fontName=FONT, fontSize=10.5, leading=16,
    textColor=HexColor("#333"), spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="Bullet", fontName=FONT, fontSize=10.5, leading=15,
    textColor=HexColor("#333"), leftIndent=18, spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="Code", fontName="Courier", fontSize=9.5, leading=14,
    textColor=HexColor("#c7254e"), leftIndent=12, spaceAfter=4,
))

elements = []

def h1(text):
    elements.append(Paragraph(text, styles["H1"]))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=HexColor("#0f3460"), spaceAfter=8))

def h2(text):
    elements.append(Paragraph(text, styles["H2"]))

def body(text):
    elements.append(Paragraph(text, styles["Body"]))

def bullet(text):
    elements.append(Paragraph(f"\u2022  {text}", styles["Bullet"]))

def code(text):
    elements.append(Paragraph(text, styles["Code"]))

def sp(h=6):
    elements.append(Spacer(1, h))

# ═══════════════════════  COVER  ═══════════════════════
elements.append(Spacer(1, 60))
elements.append(Paragraph("AI-Robot \u9879\u76ee\u67b6\u6784\u4e0e\u6280\u672f\u6808\u5206\u6790", styles["Title"]))
sp(8)
elements.append(Paragraph("FastAPI + LangChain RAG + CrewAI \u591a\u667a\u80fd\u4f53 \u667a\u80fd\u5ba2\u670d\u7cfb\u7edf", styles["SubTitle"]))
sp(12)
elements.append(HRFlowable(width="60%", thickness=2, color=HexColor("#e94560"), spaceAfter=12))
sp(20)
body("\u9879\u76ee\u8def\u5f84: /Users/shenma/Documents/project/AI-Robot")
body("\u751f\u6210\u65e5\u671f: 2026-09-16")
body("Python \u7248\u672c: 3.11 / 3.12")

elements.append(PageBreak())

# ═══════════════════════  1. \u9879\u76ee\u6982\u8ff0  ═══════════════════════
h1("\u4e00\u3001\u9879\u76ee\u6982\u8ff0")
body("AI-Robot \u662f\u4e00\u4e2a\u57fa\u4e8e FastAPI + LangChain RAG + CrewAI \u591a\u667a\u80fd\u4f53 \u7684\u667a\u80fd\u5ba2\u670d\u7cfb\u7edf\uff0c"
     "\u4e13\u95e8\u4e3a MOTORLOAN.MY\uff08\u6469\u6258\u8f66\u7535\u5546\u4e0e\u878d\u8d44\u5e73\u53f0\uff09\u63d0\u4f9b\u5ba2\u670d\u80fd\u529b\u3002"
     "\u9879\u76ee\u652f\u6301\u4e91\u7aef API\uff08\u963f\u91cc\u4e91 DashScope\uff09\u548c\u672c\u5730 Ollama \u4e24\u79cd\u90e8\u7f72\u6a21\u5f0f\u3002")

# ═══════════════════════  2. \u6574\u4f53\u67b6\u6784  ═══════════════════════
h1("\u4e8c\u3001\u6574\u4f53\u67b6\u6784")
h2("2.1 \u5206\u5c42\u67b6\u6784")
bullet("Web \u5c42: FastAPI \u8def\u7531 + \u4e2d\u95f4\u4ef6\uff08\u9650\u6d41 / \u65e5\u5fd7 / \u5f02\u5e38\u515c\u5e95\uff09")
bullet("\u5bf9\u8bdd\u7f16\u6392\u5c42: \u8bed\u4e49\u7f13\u5b58 \u2192 \u610f\u56fe\u5206\u7c7b \u2192 CrewAI / LangChain \u8def\u7531")
bullet("RAG \u68c0\u7d22\u5c42: \u5411\u91cf\u68c0\u7d22 + BM25 \u2192 RRF \u878d\u5408 \u2192 bge-reranker \u91cd\u6392")
bullet("\u5b58\u50a8\u5c42: InMemoryVectorStore\uff08\u9ed8\u8ba4\uff09\u6216 Milvus\uff08\u6301\u4e45\u5316\uff09")

h2("2.2 \u6838\u5fc3\u6570\u636e\u6d41")
code("\u7528\u6237\u8bf7\u6c42 \u2192 \u9650\u6d41\u68c0\u67e5 \u2192 \u8bed\u4e49\u7f13\u5b58 \u2192 \u610f\u56fe\u5206\u7c7b(knowledge/order/chat)")
code("  \u251c\u2500 knowledge \u2192 RAG \u68c0\u7d22 \u2192 LLM \u751f\u6210")
code("  \u251c\u2500 order     \u2192 \u8ba2\u5355\u67e5\u8be2\u5de5\u5177(Mock)")
code("  \u2514\u2500 chat      \u2192 \u95f2\u804a LLM")

# ═══════════════════════  3. \u76ee\u5f55\u7ed3\u6784  ═══════════════════════
h1("\u4e09\u3001\u76ee\u5f55\u7ed3\u6784")
code("AI-Robot/")
code("\u251c\u2500\u2500 app/                          # \u6838\u5fc3\u5e94\u7528\u4ee3\u7801")
code("\u2502   \u251c\u2500\u2500 main.py                   # FastAPI \u5165\u53e3\uff0c\u8def\u7531\u5b9a\u4e49")
code("\u2502   \u251c\u2500\u2500 config.py                 # \u5168\u5c40\u914d\u7f6e\uff08\u73af\u5883\u53d8\u91cf\u9a71\u52a8\uff09")
code("\u2502   \u251c\u2500\u2500 schemas.py                # Pydantic \u6570\u636e\u6a21\u578b")
code("\u2502   \u251c\u2500\u2500 agents/                   # \u667a\u80fd\u4f53\u6a21\u5757")
code("\u2502   \u2502   \u251c\u2500\u2500 crew.py               # CrewAI \u591a\u667a\u80fd\u4f53\u7f16\u6392")
code("\u2502   \u2502   \u2514\u2500\u2500 tools.py              # Agent \u5de5\u5177\u96c6")
code("\u2502   \u251c\u2500\u2500 rag/                      # RAG \u68c0\u7d22\u589e\u5f3a\u751f\u6210")
code("\u2502   \u2502   \u251c\u2500\u2500 retriever.py          # \u77e5\u8bc6\u5e93\u5168\u94fe\u8def")
code("\u2502   \u2502   \u251c\u2500\u2500 fusion.py             # RRF \u878d\u5408\u7b97\u6cd5")
code("\u2502   \u2502   \u251c\u2500\u2500 lexical.py            # BM25 \u8bcd\u9762\u68c0\u7d22")
code("\u2502   \u2502   \u251c\u2500\u2500 reranker.py           # bge-reranker \u91cd\u6392")
code("\u2502   \u2502   \u2514\u2500\u2500 loader.py             # \u6587\u6863\u52a0\u8f7d\u5668")
code("\u2502   \u2514\u2500\u2500 services/                 # \u670d\u52a1\u5c42")
code("\u2502       \u251c\u2500\u2500 chat.py               # \u5bf9\u8bdd\u7f16\u6392\uff08CrewAI\u4f18\u5148+\u964d\u7ea7\uff09")
code("\u2502       \u251c\u2500\u2500 memory.py             # \u4f1a\u8bdd\u8bb0\u5fc6\u7ba1\u7406")
code("\u2502       \u251c\u2500\u2500 resilience.py         # \u91cd\u8bd5/\u9000\u907f\u673a\u5236")
code("\u2502       \u251c\u2500\u2500 semantic_cache.py     # \u8bed\u4e49\u7f13\u5b58")
code("\u2502       \u251c\u2500\u2500 ratelimit.py          # \u9650\u6d41\u4e2d\u95f4\u4ef6")
code("\u2502       \u2514\u2500\u2500 tracing.py            # \u94fe\u8def\u8ffd\u8e2a")
code("\u251c\u2500\u2500 data/                         # \u77e5\u8bc6\u5e93\u6570\u636e")
code("\u251c\u2500\u2500 eval/                         # RAGAS \u8bc4\u6d4b")
code("\u251c\u2500\u2500 tests/                        # \u5355\u5143\u6d4b\u8bd5")
code("\u251c\u2500\u2500 docker-compose.yml            # Docker \u7f16\u6392\u914d\u7f6e")
code("\u251c\u2500\u2500 Dockerfile                    # \u5bb9\u5668\u5316\u90e8\u7f72")
code("\u2514\u2500\u2500 requirements*.txt             # \u4f9d\u8d56\u6587\u4ef6")

# ═══════════════════════  4. \u6280\u672f\u6808  ═══════════════════════
h1("\u56db\u3001\u6838\u5fc3\u6280\u672f\u6808")

h2("4.1 Web \u6846\u67b6")
bullet("FastAPI (>=0.110) \u2014 \u5f02\u6b65 Web \u6846\u67b6")
bullet("Uvicorn (>=0.29) \u2014 ASGI \u670d\u52a1\u5668")
bullet("sse-starlette (>=1.6) \u2014 SSE \u6d41\u5f0f\u54cd\u5e94")
bullet("python-multipart \u2014 \u6587\u4ef6\u4e0a\u4f20")

h2("4.2 AI / LLM \u6846\u67b6")
bullet("LangChain (>=0.3.0) \u2014 LLM \u5e94\u7528\u6846\u67b6")
bullet("  langchain-openai \u2014 OpenAI \u517c\u5bb9\u63a5\u53e3\u9002\u914d\u5668")
bullet("  langchain-text-splitters \u2014 \u6587\u6863\u5206\u5757")
bullet("  langchain-milvus (\u53ef\u9009) \u2014 Milvus \u5411\u91cf\u5e93\u96c6\u6210")
bullet("CrewAI (>=1.15.0, \u53ef\u9009) \u2014 \u591a\u667a\u80fd\u4f53\u7f16\u6392")

h2("4.3 \u5927\u6a21\u578b\u652f\u6301")
bullet("\u963f\u91cc\u4e91 DashScope\uff08\u901a\u4e49\u5343\u95ee qwen-plus\uff09\u2014 \u63a8\u8350")
bullet("DeepSeek\uff08deepseek-chat\uff09")
bullet("\u672c\u5730 Ollama\uff08qwen2.5:7b\uff09\u2014 \u79bb\u7ebf\u90e8\u7f72")
bullet("Embedding: text-embedding-v4 / nomic-embed-text")

h2("4.4 RAG \u68c0\u7d22\u5f15\u64ce")
bullet("\u5411\u91cf\u68c0\u7d22: OpenAI \u517c\u5bb9 Embedding API")
bullet("BM25 \u8bcd\u9762\u68c0\u7d22: jieba \u5206\u8bcd + rank_bm25")
bullet("RRF \u878d\u5408: Reciprocal Rank Fusion \u7b97\u6cd5")
bullet("\u91cd\u6392: sentence-transformers + BAAI/bge-reranker-base")

h2("4.5 \u5411\u91cf\u5b58\u50a8")
bullet("InMemoryVectorStore\uff08\u9ed8\u8ba4\uff0c\u96f6\u4f9d\u8d56\uff09")
bullet("Milvus v2.5.4\uff08\u53ef\u9009\uff0c\u6301\u4e45\u5316 ANN\uff09")

h2("4.6 \u7a33\u5b9a\u6027\u5de5\u7a0b")
bullet("tenacity (>=9.0) \u2014 \u6307\u6570\u9000\u907f\u91cd\u8bd5\uff08429/5xx/\u7f51\u7edc\u9519\u8bef\uff09")
bullet("\u8bed\u4e49\u7f13\u5b58 \u2014 \u4f59\u5f26\u76f8\u4f3c\u5ea6 + \u8bcd\u9762\u91cd\u53e0\u53cc\u95e8\u9650")
bullet("\u9650\u6d41 \u2014 \u6ed1\u52a8\u7a97\u53e3\u7b97\u6cd5\uff0830\u6b21/\u5206\u949f/IP\uff09")

h2("4.7 \u6587\u6863\u5904\u7406")
bullet("pypdf (>=4.2.0) \u2014 PDF \u89e3\u6790")
bullet("python-docx (>=1.1.0) \u2014 Word \u89e3\u6790")
bullet("MarkdownHeaderTextSplitter \u2014 Markdown \u6309\u6807\u9898\u5206\u5757")
bullet("RecursiveCharacterTextSplitter \u2014 \u9012\u5f52\u5b57\u7b26\u5206\u5757")

h2("4.8 \u90e8\u7f72\u4e0e CI/CD")
bullet("Docker \u2014 python:3.11-slim \u57fa\u7840\u955c\u50cf")
bullet("Docker Compose \u2014 \u670d\u52a1\u7f16\u6392")
bullet("GitHub Actions \u2014 \u8bed\u6cd5\u68c0\u67e5 \u2192 \u79bb\u7ebf\u5355\u6d4b \u2192 RAGAS \u8bc4\u6d4b")

# ═══════════════════════  5. \u6838\u5fc3\u8bbe\u8ba1\u4eae\u70b9  ═══════════════════════
h1("\u4e94\u3001\u6838\u5fc3\u8bbe\u8ba1\u4eae\u70b9")

h2("5.1 \u591a\u5c42\u964d\u7ea7\u7b56\u7565")
code("CrewAI \u591a\u667a\u80fd\u4f53 \u2192 LangChain \u5185\u7f6e\u8def\u7531 \u2192 \u5f02\u5e38\u515c\u5e95")
bullet("CrewAI \u672a\u5b89\u88c5\u6216\u8c03\u7528\u5931\u8d25\u65f6\u81ea\u52a8\u964d\u7ea7")
bullet("\u91cd\u6392\u6a21\u578b\u672a\u52a0\u8f7d\u65f6\u4fdd\u7559 RRF \u878d\u5408\u987a\u5e8f")
bullet("\u6240\u6709\u964d\u7ea7\u5bf9\u7528\u6237\u900f\u660e")

h2("5.2 \u6df7\u5408\u68c0\u7d22 + \u91cd\u6392")
code("\u5411\u91cf\u68c0\u7d22 + BM25 \u2192 RRF \u878d\u5408 \u2192 bge-reranker \u91cd\u6392")
bullet("\u5411\u91cf\u68c0\u7d22\u64c5\u957f\u8bed\u4e49\u7406\u89e3")
bullet("BM25 \u64c5\u957f\u4e13\u6709\u540d\u8bcd/\u8ba2\u5355\u53f7\u7cbe\u786e\u5339\u914d")
bullet("RRF \u65e0\u9700\u5f52\u4e00\u5316\u5206\u6570\u5373\u53ef\u878d\u5408\u591a\u8def\u7ed3\u679c")
bullet("CrossEncoder \u91cd\u6392\u63d0\u5347\u6700\u7ec8\u7cbe\u5ea6")

h2("5.3 \u8bed\u4e49\u7f13\u5b58\u4f18\u5316")
bullet("\u53cc\u95e8\u9650\u673a\u5236: \u4f59\u5f26\u76f8\u4f3c\u5ea6 >= 0.9 + \u8bcd\u9762\u91cd\u53e0\u7387 >= 0.5")
bullet("\u4ec5\u9996\u8f6e\u95ee\u9898\u53c2\u4e0e\u7f13\u5b58\uff0c\u907f\u514d\u4e0e\u4f1a\u8bdd\u8bb0\u5fc6\u8026\u5408")
bullet("\u52a8\u6001\u6570\u636e\uff08\u8ba2\u5355\u67e5\u8be2\uff09\u4e0d\u7f13\u5b58")

h2("5.4 \u5168\u94fe\u8def\u53ef\u89c2\u6d4b\u6027")
bullet("\u8bf7\u6c42\u65e5\u5fd7: HTTP \u65b9\u6cd5\u3001\u8def\u5f84\u3001\u72b6\u6001\u7801\u3001\u8017\u65f6")
bullet("\u94fe\u8def\u8ffd\u8e2a: \u5404\u9636\u6bb5\u8017\u65f6\uff08\u7f13\u5b58/\u610f\u56fe/\u68c0\u7d22/\u751f\u6210\uff09")
bullet("\u53ef\u89c6\u5316\u63a7\u5236\u53f0: /dashboard \u5b9e\u65f6\u76d1\u63a7")
bullet("\u6027\u80fd\u6307\u6807: P95 \u5ef6\u8fdf\u3001\u7f13\u5b58\u547d\u4e2d\u7387\u3001\u9650\u6d41\u62e6\u622a\u6570")

h2("5.5 \u4f1a\u8bdd\u8bb0\u5fc6\u7ba1\u7406")
bullet("\u6309 session_id \u9694\u79bb\u591a\u8f6e\u5bf9\u8bdd")
bullet("\u53ef\u914d\u7f6e\u6700\u5927\u4fdd\u7559\u8f6e\u6b21\uff08\u9ed8\u8ba4 20 \u8f6e\uff09")
bullet("\u8d85\u51fa\u4e0a\u9650\u81ea\u52a8\u88c1\u526a\u6700\u65e7\u6d88\u606f")
bullet("\u751f\u4ea7\u53ef\u66ff\u6362\u4e3a Redis/SQLite \u6301\u4e45\u5316")

# ═══════════════════════  6. \u90e8\u7f72\u6a21\u5f0f  ═══════════════════════
h1("\u516d\u3001\u90e8\u7f72\u6a21\u5f0f")

h2("6.1 \u4e91\u7aef API\uff08\u63a8\u8350\uff09")
code("docker compose up -d --build")
bullet("\u4f7f\u7528\u963f\u91cc\u4e91 DashScope \u901a\u4e49\u5343\u95ee")
bullet("\u65e0\u9700\u672c\u5730 GPU\uff0c\u5f00\u7bb1\u5373\u7528")

h2("6.2 \u672c\u5730 Ollama")
code("# \u4fee\u6539 .env \u6307\u5411 http://localhost:11434/v1")
code("docker compose up -d --build")
bullet("\u79bb\u7ebf\u90e8\u7f72\uff0c\u6570\u636e\u4e0d\u51fa\u5883")
bullet("\u9700\u8981\u672c\u5730\u8fd0\u884c Ollama \u670d\u52a1")

h2("6.3 \u6301\u4e45\u5316\u5411\u91cf\u5e93")
code("docker compose -f docker-compose-milvus.yml up -d")
bullet("Milvus Standalone + \u5185\u5d4c etcd")
bullet("\u652f\u6301\u77e5\u8bc6\u5e93\u6301\u4e45\u5316")

# ═══════════════════════  7. \u6027\u80fd\u914d\u7f6e  ═══════════════════════
h1("\u4e03\u3001\u6027\u80fd\u914d\u7f6e\u53c2\u6570")

tbl_data = [
    ["\u914d\u7f6e\u9879", "\u9ed8\u8ba4\u503c", "\u8bf4\u660e"],
    ["\u6587\u6863\u5206\u5757", "400 \u5b57\u7b26\uff0c\u91cd\u53e0 80", "\u5e73\u8861\u4e0a\u4e0b\u6587\u4e0e\u68c0\u7d22\u7cbe\u5ea6"],
    ["\u5411\u91cf\u56de\u53ec", "Top 5", "RRF \u878d\u5408\u540e\u53d6 Top 10"],
    ["\u68c0\u7d22\u7b56\u7565", "\u5411\u91cf 15 + BM25 15", "\u53cc\u8def\u56de\u53ec\u63d0\u5347\u8986\u76d6\u7387"],
    ["\u9650\u6d41", "30 \u6b21/\u5206\u949f/IP", "\u6ed1\u52a8\u7a97\u53e3\u7b97\u6cd5"],
    ["\u91cd\u8bd5", "\u6700\u591a 3 \u6b21", "\u6307\u6570\u9000\u907f\uff0c\u6700\u5927 8 \u79d2"],
    ["\u4f1a\u8bdd\u8bb0\u5fc6", "\u6700\u591a 20 \u8f6e\uff0c\u68c0\u7d22 6 \u8f6e", "\u5e73\u8861\u4e0a\u4e0b\u6587\u4e0e token \u6d88\u8017"],
]

col_w = [55 * mm, 55 * mm, 55 * mm]
t = Table(tbl_data, colWidths=col_w, repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#0f3460")),
    ("TEXTCOLOR", (0, 0), (-1, 0), white),
    ("FONTNAME", (0, 0), (-1, 0), FONT),
    ("FONTSIZE", (0, 0), (-1, 0), 10),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#ddd")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f4f4f8")]),
    ("FONTNAME", (0, 1), (-1, -1), FONT),
    ("FONTSIZE", (0, 1), (-1, -1), 9.5),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
]))
elements.append(Spacer(1, 6))
elements.append(t)

# ═══════════════════════  8. \u9002\u7528\u573a\u666f  ═══════════════════════
h1("\u516b\u3001\u9002\u7528\u573a\u666f")
bullet("\u667a\u80fd\u5ba2\u670d\u7cfb\u7edf: \u7535\u5546\u3001\u91d1\u878d\u3001\u6559\u80b2\u7b49\u884c\u4e1a\u7684\u95ee\u7b54\u673a\u5668\u4eba")
bullet("\u4f01\u4e1a\u77e5\u8bc6\u5e93: \u5185\u90e8\u6587\u6863\u68c0\u7d22\u4e0e\u95ee\u7b54")
bullet("RAG \u6280\u672f\u9a8c\u8bc1: \u6df7\u5408\u68c0\u7d22\u3001\u91cd\u6392\u3001\u8bed\u4e49\u7f13\u5b58\u7b49\u6700\u4f73\u5b9e\u8df5")
bullet("\u591a\u667a\u80fd\u4f53\u5b66\u4e60: CrewAI \u7f16\u6392\u6a21\u5f0f\u53c2\u8003\u5b9e\u73b0")

sp(16)
elements.append(HRFlowable(width="100%", thickness=1, color=HexColor("#ccc"), spaceAfter=8))
body("\u603b\u7ed3: \u8fd9\u662f\u4e00\u4e2a\u751f\u4ea7\u7ea7\u522b\u7684 RAG \u5e94\u7528\uff0c\u4ee3\u7801\u7ed3\u6784\u6e05\u6670\uff0c\u5de5\u7a0b\u5316\u7a0b\u5ea6\u9ad8\uff0c"
     "\u975e\u5e38\u9002\u5408\u4f5c\u4e3a\u5b66\u4e60\u53c2\u8003\u6216\u9879\u76ee\u8d77\u70b9\u3002")

# ── build ──
doc.build(elements)
print(f"PDF saved to: {output_path}")