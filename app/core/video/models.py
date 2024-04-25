from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 프롬프트를 통한 금융 지식
class EducationData(Base):
    __tablename__ = 'education_data'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)


# 금융 학습 비디오
class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True, index=True)
    video_path = Column(String, unique=True, index=True)
    video_description = Column(String)
    education_data_id = Column(Integer, ForeignKey('education_data.id'))
    education_data = relationship("EducationData", back_populates="videos")


EducationData.videos = relationship("Video", order_by=Video.id, back_populates="education_data")