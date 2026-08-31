import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, JSON, Boolean, Integer
from sqlalchemy.orm import relationship
from core.database import Base


class PStatus(str, PyEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class OFormat(str, PyEnum):
    HTML = "html"
    REACT = "react"
    JSON = "json"


class DType(str, PyEnum):
    PRD = "prd"
    DESIGN = "design"
    CODE = "code"
    OTHER = "other"


class AStatus(str, PyEnum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    ERROR = "error"


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    display_name = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    projects = relationship("Project", back_populates="owner")
    keys = relationship("PKey", back_populates="owner")


class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    owner_id = Column(String, ForeignKey("users.id"))
    status = Column(Enum(PStatus), default=PStatus.DRAFT)
    output_format = Column(Enum(OFormat), default=OFormat.HTML)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner = relationship("User", back_populates="projects")
    docs = relationship("PDoc", back_populates="project")
    runs = relationship("ARun", back_populates="project")
    versions = relationship("Version", back_populates="project")


class PKey(Base):
    __tablename__ = "provider_keys"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("users.id"))
    label = Column(String, nullable=False)
    provider_id = Column(String, nullable=False)
    base_url = Column(String, nullable=True)
    key_enc = Column(Text, nullable=False)
    default_model = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="keys")


class SPrompt(Base):
    __tablename__ = "prompts"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    content = Column(Text, default="")
    category = Column(String, default="general")
    created_at = Column(DateTime, default=datetime.utcnow)


class Template(Base):
    __tablename__ = "templates"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    content = Column(Text, default="")
    category = Column(String, default="landing")
    created_at = Column(DateTime, default=datetime.utcnow)


class PDoc(Base):
    __tablename__ = "project_docs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    name = Column(String, nullable=False)
    dtype = Column(Enum(DType), default=DType.OTHER)
    content = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="docs")


class ARun(Base):
    __tablename__ = "agent_runs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    status = Column(Enum(AStatus), default=AStatus.PENDING)
    input_text = Column(Text, default="")
    output = Column(Text, default="")
    logs = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    project = relationship("Project", back_populates="runs")


class Version(Base):
    __tablename__ = "versions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    number = Column(Integer, default=1)
    code = Column(Text, default="")
    meta = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="versions")
