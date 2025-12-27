"""FastAPI后端主入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import bazi, compatibility, date_selection, advanced, bonefate

app = FastAPI(
    title="Fortune Tracer API",
    description="生辰八字AI解读服务 - RESTful API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(bazi.router, prefix="/api")
app.include_router(compatibility.router, prefix="/api")
app.include_router(date_selection.router, prefix="/api")
app.include_router(advanced.router, prefix="/api")
app.include_router(bonefate.router, prefix="/api")


@app.get("/")
async def root():
    """API根路径"""
    return {
        "name": "Fortune Tracer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

