from pydantic import BaseModel
from typing import Optional


class CreateContentRequest(BaseModel):
    label: int
    level: int


class UserBase(BaseModel):
    name: str
    nickname: str
    e_mail: str
    level: str = "1"
    user_point: int = 0
    profile_image: int


class UserCreate(UserBase):
    hashed_password: str


class UserRead(UserBase):
    is_active: bool
    user_id: int


class PointsUpdate(BaseModel):
    user_point: int


# class RankingBase(BaseModel):
#     user_id: int
#     user_point: int
#
#
# class RankingCreate(RankingBase):
#     pass
#
#
# class RankingRead(RankingBase):
#     r_id: int
#
#
# class RankingUpdate(BaseModel):
#     user_point: Optional[int] = None


class Login(BaseModel):
    e_mail: str
    password: str


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    profile_image: Optional[int] = None


############################################
class ScriptsBase(BaseModel):
    level: int
    category_label: int
    content_1: str
    content_2: str
    content_3: str


class ScriptsCreate(ScriptsBase):
    pass


class ScriptsRead(ScriptsBase):
    scripts_id: int


class ScriptsUpdate(ScriptsBase):
    pass


class ModifyScriptRequest(BaseModel):
    new_prompt: str


class ShortformBase(BaseModel):
    form_url: str
    scripts_id: int


class ShortformCreate(ShortformBase):
    pass


class ShortformRead(ShortformBase):
    form_id: int


class ShortformUpdate(BaseModel):
    form_url: Optional[str] = None


class CategoryBase(BaseModel):
    content: str
    label: int


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryInDBBase(CategoryBase):
    category_id: int

    class Config:
        orm_mode = True


class Category(CategoryInDBBase):
    pass


#################################################################
class QuestionBase(BaseModel):
    scripts_id: int
    answer_option: int
    question: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str
    plus_point: int
    minus_point: int


class QuestionCreate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    q_id: int


class QuestionUpdate(BaseModel):
    answer_option: Optional[int] = None
    question: Optional[str] = None
    option_1: Optional[str] = None
    option_2: Optional[str] = None
    option_3: Optional[str] = None
    option_4: Optional[str] = None


class CaseScriptsBase(BaseModel):
    content_1: Optional[str]
    content_2: Optional[str]
    content_3: Optional[str]
    content_4: Optional[str]
    content_5: Optional[str]
    content_6: Optional[str]


class CaseScriptsCreate(CaseScriptsBase):
    scripts_id: int


class CaseScriptsUpdate(CaseScriptsBase):
    pass


class CaseScripts(CaseScriptsBase):
    case_scripts_id: int

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    q_id: int
    comment_1: str
    comment_2: str
    comment_3: str


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    c_id: int


class CommentUpdate(BaseModel):
    comment_1: Optional[str] = None
    comment_2: Optional[str] = None
    comment_3: Optional[str] = None
    comment_4: Optional[str] = None


class AdminBase(BaseModel):
    password: str


class AdminCreate(AdminBase):
    admin_name: str
    password: str
    qualification_level: int


class AdminRead(AdminBase):
    admin_id: int


class AdminUpdate(BaseModel):
    admin_id: int
    password: str = None
    admin_name: str = None
    qualification_level: int = None


class AdminLogin(BaseModel):
    admin_name: str
    password: str


class HistoryBase(BaseModel):
    user_id: int
    scripts_id: int
    T_F: bool


class HistoryCreate(HistoryBase):
    pass


class HistoryRead(HistoryBase):
    h_id: int


class HistoryUpdate(BaseModel):
    T_F: Optional[bool] = None
