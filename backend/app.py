from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel  # ← Adicione esta importação
import os

# ✅ CORREÇÃO: Configuração robusta do banco de dados
def get_database_url():
    # No Railway, use DATABASE_URL fornecida
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return database_url
    
    # No local, construa a URL das variáveis individuais
    user = os.environ.get('POSTGRES_USER', 'postgres')
    password = os.environ.get('POSTGRES_PASSWORD', '')
    host = os.environ.get('POSTGRES_HOST', 'localhost')
    port = os.environ.get('POSTGRES_PORT', '5432')
    database = os.environ.get('POSTGRES_DB', 'postgres')
    
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

# ✅ Use a função para obter a URL
database_url = get_database_url()
print(f"Conectando ao banco: {database_url}")  # Debug
# Configuração do banco de dados
engine = create_engine(os.environ.get('DATABASE_URL'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de exemplo
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

# Modelo Pydantic para criação
class ItemCreate(BaseModel):
    name: str
    description: str

# Modelo Pydantic para resposta
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://testedocker-production-4e85.up.railway.app", "https://teste-docker.vercel.app", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello from Python Backend with PostgreSQL!"}

@app.get("/api/items", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items

# ROTA ATUALIZADA - Agora aceita JSON!
@app.post("/api/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/health")
def health_check():
    return {"status": "healthy"}