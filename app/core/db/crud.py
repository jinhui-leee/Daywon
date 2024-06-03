from sqlalchemy.orm import Session
from app.core.db import models, schemas
from app.core.db.models import Scripts, Question, Shortform, Admin, History, Ranking, CaseScripts
from passlib.hash import bcrypt


def create_user(db: Session, user_create: schemas.UserCreate):
    # 평문 패스워드를 bcrypt 해시로 변환
    hashed_password = bcrypt.hash(user_create.hashed_password)

    # User 모델 인스턴스 생성
    user = models.User(
        name=user_create.name,
        nickname=user_create.nickname,
        e_mail=user_create.e_mail,
        level=user_create.level,
        user_point=user_create.user_point,
        hashed_password=hashed_password,  # 해싱된 비밀번호 저장
        profile_image=user_create.profile_image

    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_email(db: Session, e_mail: str) -> object:
    return db.query(models.User).filter(models.User.e_mail == e_mail).first()


# 닉네임 중복 검사 함수

def get_user_by_nickname(db: Session, nickname: str):
    return db.query(models.User).filter(models.User.nickname == nickname).first()


def update_user(db: Session, user_id: int, update_data: dict):
    # 사용자 정보 갱신 (닉네임과 프로필 이미지만)
    db.query(models.User).filter(models.User.user_id == user_id).update({
        models.User.nickname: update_data["nickname"],
        models.User.profile_image: update_data["profile_image"]
    }, synchronize_session=False)
    db.commit()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user_points(db: Session, user_id: int, new_points: int):
    # 사용자 포인트 업데이트
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        raise ValueError("User not found")

    user.user_point = new_points
    db.commit()
    db.refresh(user)

    # 랭킹 업데이트
    ranking = db.query(models.Ranking).filter(models.Ranking.user_id == user_id).first()
    if ranking is None:
        # 랭킹이 없으면 새로 생성
        ranking = models.Ranking(user_id=user_id, user_point=new_points)
        db.add(ranking)
    else:
        # 랭킹이 있으면 업데이트
        ranking.user_point = new_points
    db.commit()
    db.refresh(ranking)

    # 랭킹 재정렬
    update_rankings(db)


def update_rankings(db: Session):
    # 모든 랭킹 데이터를 가져와서 포인트로 정렬
    rankings = db.query(models.Ranking).order_by(models.Ranking.user_point.desc()).all()

    # 랭킹 업데이트
    for rank, ranking in enumerate(rankings, start=1):
        ranking.ranking_position = rank
    db.commit()


###################################################################


# Scripts 모델을 위한 CRUD 함수들
def get_script(db: Session, scripts_id: int):
    return db.query(Scripts).filter(Scripts.scripts_id == scripts_id).first()


def create_script(db: Session, script_data):
    new_script = Scripts(
        level=script_data['level'],
        category_name=script_data['category_name'],
        content_1=script_data['content_1'],
        content_2=script_data['content_2'],
        content_3=script_data['content_3']
    )
    db.add(new_script)
    db.commit()
    db.refresh(new_script)
    return new_script.scripts_id


def update_script(db: Session, script_id: int, update_data):
    script = db.query(Scripts).filter(Scripts.scripts_id == script_id).first()
    if script:
        for key, value in update_data.items():
            setattr(script, key, value)
        db.commit()
        return script
    return None


def delete_script(db: Session, script_id: int):
    script = db.query(Scripts).filter(Scripts.scripts_id == script_id).first()
    if script:
        db.delete(script)
        db.commit()
        return True
    return False


def get_scripts_by_category(db: Session, category_name: int):
    return db.query(Scripts).filter(Scripts.category_name == category_name).all()


###################################################################
# Question
def create_question(db: Session, question_data):
    question = Question(
        scripts_id=question_data['scripts_id'],
        answer_option=question_data['answer_option'],
        question=question_data['question'],
        option_1=question_data['option_1'],
        option_2=question_data['option_2'],
        option_3=question_data['option_3'],
        option_4=question_data['option_4'],
        plus_point=question_data['plus_point'],
        minus_point=question_data['minus_point']
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def update_question(db: Session, q_id: int, update_data):
    question = db.query(Question).filter(Question.q_id == q_id).first()
    if question:
        if 'answer_option' in update_data:
            question.answer_option = update_data['answer_option']
        if 'question' in update_data:
            question.question = update_data['question']
        if 'option_1' in update_data:
            question.option_1 = update_data['option_1']
        if 'option_2' in update_data:
            question.option_2 = update_data['option_2']
        if 'option_3' in update_data:
            question.option_3 = update_data['option_3']
        if 'plus_point' in update_data:
            question.plus_point = update_data['plus_point']
        if 'minus_point' in update_data:
            question.minus_point = update_data['minus_point']

        db.commit()
        return question
    return None


###################################################################
def create_case_script(db: Session, case_script_data):
    new_case_script = CaseScripts(
        scripts_id=case_script_data['scripts_id'],
        content_1=case_script_data['content_1'],
        content_2=case_script_data['content_2'],
        content_3=case_script_data['content_3'],
        content_4=case_script_data['content_4'],
        content_5=case_script_data['content_5'],
        content_6=case_script_data['content_6']
    )
    db.add(new_case_script)
    db.commit()
    db.refresh(new_case_script)
    return new_case_script


def get_case_script(db: Session, case_scripts_id: int):
    return db.query(CaseScripts).filter(CaseScripts.case_scripts_id == case_scripts_id).first()


def get_case_scripts_by_script_id(db: Session, scripts_id: int):
    return db.query(CaseScripts).filter(CaseScripts.scripts_id == scripts_id).all()


def update_case_script(db: Session, case_scripts_id: int, content: list):
    case_script = db.query(CaseScripts).filter(CaseScripts.case_scripts_id == case_scripts_id).first()
    if not case_script:
        return None
    case_script.content_1 = content[0] if len(content) > 0 else case_script.content_1
    case_script.content_2 = content[1] if len(content) > 1 else case_script.content_2
    case_script.content_3 = content[2] if len(content) > 2 else case_script.content_3
    case_script.content_4 = content[3] if len(content) > 3 else case_script.content_4
    case_script.content_5 = content[4] if len(content) > 4 else case_script.content_5
    case_script.content_6 = content[5] if len(content) > 5 else case_script.content_6
    db.commit()
    db.refresh(case_script)
    return case_script


def delete_case_script(db: Session, case_scripts_id: int):
    case_script = db.query(CaseScripts).filter(CaseScripts.case_scripts_id == case_scripts_id).first()
    if not case_script:
        return None
    db.delete(case_script)
    db.commit()
    return case_script


# # comment
# def create_comment(db: Session, comment_data):
#     comment = Comment(
#         q_id=comment_data['q_id'],
#         comment_1=comment_data['comment_1'],
#         comment_2=comment_data['comment_2'],
#         comment_3=comment_data['comment_3']
#     )
#     db.add(comment)
#     db.commit()
#     db.refresh(comment)
#     return comment
#
#
# def get_comments_by_question_id(db: Session, q_id: int):
#     return db.query(Comment).filter(Comment.q_id == q_id).all()


# Shortform
def create_shortform(db: Session, shortform_data):
    new_shortform = Shortform(
        form_url=shortform_data['form_url'],
        scripts_id=shortform_data['scripts_id']
    )
    db.add(new_shortform)
    db.commit()
    db.refresh(new_shortform)
    return new_shortform


def get_shortform_by_id(db: Session, form_id: int):
    return db.query(Shortform).filter(Shortform.form_id == form_id).first()


# admin

def create_admin(db: Session, admin_data):
    admin = Admin(
        password=admin_data['password']
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def delete_admin(db: Session, admin_id: int):
    admin = db.query(Admin).filter(Admin.admin_id == admin_id).first()
    if admin:
        db.delete(admin)
        db.commit()
        return True
    return False


# history

def log_history(db: Session, history_data):
    history = History(
        user_id=history_data['user_id'],
        scripts_id=history_data['scripts_id'],
        T_F=history_data['T_F']
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


# ranking

def create_ranking(db: Session, ranking_data):
    ranking = Ranking(
        user_id=ranking_data['user_id'],
        user_point=ranking_data['user_point']
    )
    db.add(ranking)
    db.commit()
    db.refresh(ranking)
    return ranking


def update_ranking_points(db: Session, user_id: int, new_points):
    ranking = db.query(Ranking).filter(Ranking.user_id == user_id).first()
    if ranking:
        ranking.user_point = new_points
        db.commit()
        return ranking
    return None
