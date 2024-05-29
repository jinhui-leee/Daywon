import httpx
import random
from app.core.api import util_api, get_api_key


async def call_api(api_url, headers, data):
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            return f"Error: {response.status_code}, {response.text}"


async def create_prompt():
    api_key = get_api_key()
    model = 'gpt-4'

    level = get_finance_level()
    category = get_finance_category()
    print(level)
    print(category)
    if level == 1:
        system_prompt = """
        다음 조건들을 모두 만족하는 문장을 만들어주세요.
        1 - 공백을 포함한 글자 수를 300자 이내로 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 초등학교 저학년 학생들의 금융 지식 수준에 맞도록 작성해주세요.
        4 - 당신은 초등학교 저학년 학생들에게 금융 지식을 설명해야 합니다. 이 연령대의 학생들이 쉽게 이해할 수 있도록 간단한 용어를 사용하고, 재미있고 친근한 예시를 포함하세요.
        5 - 대상을 언급하지 마세요.
        """

    elif level == 2:
        system_prompt = """
        다음 조건들을 모두 만족하는 문장을 만들어주세요.
        1 - 공백을 포함한 글자 수를 300자 이내로 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 초등학교 고학년 학생들의 금융 지식 수준에 맞도록 작성해주세요.
        4 - 당신은 초등학교 고학년 학생들에게 금융 지식을 설명해야 합니다. 이 연령대의 학생들은 간단한 개념을 이해할 수 있으며, 더 구체적인 예시도 가능합니다.
        5 - 대상을 언급하지 마세요.
        """

    elif level == 3:
        system_prompt = """
        다음 조건들을 모두 만족하는 문장을 만들어주세요.
        1 - 공백을 포함한 글자 수를 300자 이내로 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 중학교 학생들의 금융 지식 수준에 맞도록 작성해주세요.
        4 - 당신은 중학생들에게 금융 지식을 설명해야 합니다. 이 연령대의 학생들은 추상적인 개념을 이해할 수 있으며, 실제 생활과 관련된 예시를 통해 더 깊이 있는 내용을 다룰 수 있습니다.
        5 - 대상을 언급하지 마세요.
        """

    elif level == 4:
        system_prompt = """
        다음 조건들을 모두 만족하는 문장을 만들어주세요.
        1 - 공백을 포함한 글자 수를 300자 이내로 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 고등학교 학생들의 금융 지식 수준에 맞도록 작성해주세요.
        4 - 당신은 고등학생들에게 금융 지식을 설명해야 합니다. 이 연령대의 학생들은 복잡한 개념을 이해하고 생각할 수 있습니다.
        5 - 대상을 언급하지 마세요.
        """

    elif level == 5:
        system_prompt = """
        다음 조건들을 모두 만족하는 문장을 만들어주세요.
        1 - 공백을 포함한 글자 수를 300자 이내로 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 대학생들의 금융 지식 수준에 맞도록 작성해주세요.
        4 - 당신은 대학생들에게 금융 지식을 설명해야 합니다. 이 연령대의 학생들은 독립적인 재무 결정을 내릴 준비가 되어 있으며, 고급 금융 개념을 이해할 수 있습니다. 
        5 - 대상을 언급하지 마세요.
        """
    else:
        return "Invalid level"

    user_prompt = f"""
    다음 동작을 수행하세요.
    1 - {category}에 대해서 명확하게 설명해주세요. 
    """
    api_url, headers, data = util_api(api_key, model, system_prompt, user_prompt)

    # return await call_api(api_url, headers, data)

    conceptual_script = await call_api(api_url, headers, data)
    return conceptual_script, level, category


async def create_example_prompt(finance_category, level):
    api_key = get_api_key()
    model = 'gpt-4'

    if level == 1:
        system_prompt = """
        다음 조건들을 모두 만족하는 예시 문장을 만들어주세요.
        1 - 각 문장의 글자 수가 80자 이내로 총 6개의 문장을 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 온점은 오로지 문장이 끝났을 때만 사용해주세요.
        4 - 문장들을 숫자로 구분하지 말고, 이어지게 문장들만 출력해주세요.
        5 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 초등학교 저학년 학생들이 겪을 만한 실제 상황을 예시에 포함해주세요.
        6 - 이 연령대의 학생들이 쉽게 이해할 수 있도록 간단한 용어를 사용하고, 재미있고 친근한 예시를 포함하세요.
        7 - 대상을 언급하지 마세요.
        """

    elif level == 2:
        system_prompt = """
        다음 조건들을 모두 만족하는 예시 문장을 만들어주세요.
        1 - 각 문장의 글자 수가 80자 이내로 총 6개의 문장을 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 온점은 오로지 문장이 끝났을 때만 사용해주세요.
        4 - 문장들을 숫자로 구분하지 말고, 이어지게 문장들만 출력해주세요.
        5 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 초등학교 고학년 학생들이 겪을 만한 실제 상황을 예시에 포함해주세요.
        6 - 이 연령대의 학생들이 쉽게 이해할 수 있도록 간단한 용어를 사용하고, 재미있고 친근한 예시를 포함하세요.
        7 - 대상을 언급하지 마세요.
        """

    elif level == 3:
        system_prompt = """
        다음 조건들을 모두 만족하는 예시 문장을 만들어주세요.
        1 - 각 문장의 글자 수가 80자 이내로 총 6개의 문장을 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 온점은 오로지 문장이 끝났을 때만 사용해주세요.
        4 - 문장들을 숫자로 구분하지 말고, 이어지게 문장들만 출력해주세요.
        5 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 중학교 학생들이 겪을 만한 실제 상황을 예시에 포함해주세요.
        6 - 이 연령대의 학생들이 쉽게 이해할 수 있도록 간단한 용어를 사용하고, 재미있고 친근한 예시를 포함하세요.
        7 - 대상을 언급하지 마세요.
        """
    elif level == 4:
        system_prompt = """
        다음 조건들을 모두 만족하는 예시 문장을 만들어주세요.
        1 - 각 문장의 글자 수가 80자 이내로 총 6개의 문장을 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 온점은 오로지 문장이 끝났을 때만 사용해주세요.
        4 - 문장들을 숫자로 구분하지 말고, 이어지게 문장들만 출력해주세요.
        5 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 고등학교 학생들이 겪을 만한 실제 상황을 예시에 포함해주세요.
        6 - 이 연령대의 학생들이 쉽게 이해할 수 있도록 간단한 용어를 사용하고, 재미있고 친근한 예시를 포함하세요.
        7 - 대상을 언급하지 마세요.
        """

    elif level == 5:
        system_prompt = """
        다음 조건들을 모두 만족하는 예시 문장을 만들어주세요.
        1 - 각 문장의 글자 수가 80자 이내로 총 6개의 문장을 작성해주세요.
        2 - 영어가 아닌 한글만 사용해주세요.
        3 - 온점은 오로지 문장이 끝났을 때만 사용해주세요.
        4 - 문장들을 숫자로 구분하지 말고, 이어지게 문장들만 출력해주세요.
        5 - 문장들의 앞 뒤 문맥을 고려해서, 문장의 내용을 대학생 학생들이 겪을 만한 실제 상황을 예시에 포함해주세요.
        6 - 이 연령대의 학생들이 쉽게 이해할 수 있도록 간단한 용어를 사용하고, 재미있고 친근한 예시를 포함하세요.
        7 - 대상을 언급하지 마세요.
        """
    else:
        return "Invalid level"

    user_prompt = f"""
    다음 동작을 수행하세요. 
    1 - {finance_category}에 대한 구체적인 실생활 예시를 들어주세요.
    """
    api_url, headers, data = util_api(api_key, model, system_prompt, user_prompt)
    return await call_api(api_url, headers, data)


def get_finance_category():
    finance_categories = [
        #금융/경제 지표 및 통계
        "가계부실위험지수(HDRI)", "가계수지", "가계순저축률", "가계신용통계", "가계처분가능소득", "고용률", "고용보조지표", "고용유발효과/취업유발효과", "고정이하여신비율",
        "고정분류여신",
        "고정자본소모", "고정환율제도/자유변동환율제도", "경기동향지수(경기확산지수)", "경기종합지수", "경상수지", "경제성장률", "경제심리지수", "경제협력개발기구(OECD)",
        "경제활동인구/비경제활동인구/경제활동참가율", "경제후생지표",
        "고통지수", "국내총생산(GDP)", "국내총투자율", "국민계정체계(SNA)", "국민대차대조표", "국민부담률", "국민소득", "국민소득 3면 등가의 법칙", "국민처분가능소득",
        "국민총소득(GNI)",
        "국가경쟁력지수", "국가신용등급", "국가채무", "국내공급물가지수", "국내신용", "명목GDP목표제", "명목국내총생산/실질국내총생산", "명목금리/실질금리", "명목소득/실질소득",
        "물가지수",
        "부가가치기준 무역(TiVA)", "부가가치유발계수/부가가치계수", "수출경합도지수", "수출입물가지수", "수출입물량지수", "실업률", "실업률갭", "실질임금", "실효환율", "지니계수",
        "생산자물가지수(PPI)", "서비스수지", "순이자마진(NIM)", "총부채상환비율(DTI)", "총부채원리금상환비율(DSR)", "평균소비성향/평균저축성향", "청년실업률", "통상임금",
        "물가안정목표제", "소비자물가지수(CPI)",
        "생활물가지수", "기대인플레이션", "금융중개지원대출제도"
        
        # 금융 시장 및 제도
        "가동률", "가변예치의무제도", "가산금리", "가상통화", "가상통화공개(ICO)", "간접금융/직접금융", "간접세/직접세", "거액결제시스템",
        "거액익스포저 규제", "결제", "결제리스크", "결제부족자금 공동분담제", "결제완결성", "고객확인절차(KYC)", "고정금리", "고정금리부채권(SB)", "골디락스경제", "공개시장운영", "교환사채(EB)",
        "교환성 통화", "구매력평가환율", "국가신용등급", "국가채무", "구제금융", "구조적 이익률", "규제 샌드박스", "그린본드", "그림자 금융", "금리선물", "금리스왑",
        "금리자유화", "금리평가이론", "금본위제", "금융제도", "금융지주회사", "금융채", "금융통화위원회", "금전신탁", "기업・개인간(B2C) 지급결제시스템",
        "기업간(B2B) 지급결제시스템", "기업경기실사지수(BSI)", "기준금리", "기준환율", "기초가격", "기축통화", "긴급수입제한조치", "긴축정책"
        
        # 정부 및 공공정책
        "감독자협의회", "갑기금(Capital A)", "거시건전성 정책",
        "경기조절정책/경제안정화정책", "경영실태평가/은행경영실태 등급평가제도", "경영지도비율", "경영평가지표", "계절변동조정시계열", "공공재", "공매도",
        "관리변동환율제도", "관리통화제도", "고용유발효과/취업유발효과", "국제결제은행(BIS)", "국제금융시장", "국제금융중심지", "국제산업연관표", "국제수지(BOP)", "국제수지표",
        "국제원유가격",
        "국제통화기금(IMF)", "국제투자대조표(IIP)", "국제회계기준", "국채", "대외지급준비자산", "대체비용리스크", "대체재", "독점/과점", "동남아시아국가연합(ASEAN)",
        "동남아시아국가연합+한・중・일(ASEAN+3)",
        "동남아중앙은행기구(SEACEN)", "동아시아 외환위기", "동아시아・태평양중앙은행기구(EMEAP)", "동일인 신용공여한도제(동일인 여신한도제)", "동일인/특수관계인",
        "동태적 대손충당금 제도", "등록발행", "디레버리징", "디스인플레이션", "디커플링/커플링",
        "디플레이션", "라퍼곡선", "레그테크", "레버리지 효과", "레버리지비율", "로렌츠곡선", "로보어드바이저", "리디노미네이션", "마샬의 k", "마스트리히트조약",
        "마이크로 크레디트", "마찰적 실업", "만기수익률", "매매보호 서비스(escrow)", "매몰비용", "매입외환/환가료", "매출액영업이익률", "무디스", "무역지수", "물가안정목표제",
        "물가지수", "뮤추얼펀드", "미달러화 지수", "미달러화페그제도", "미발행화폐", "바젤은행감독위원회/바젤위원회(BCBS)", "발행시장", "발행중지화폐/유통정지화폐", "방카슈랑스",
        "배당할인모형",
        "밴드웨건효과", "뱅크런", "범위의 경제", "법률리스크", "베블런효과", "변동금리", "변동금리부채권(FRN)", "보기화폐(견양화폐)", "보완자본(Tier 2)", "보완재",
        "보통주자본(Common Equity Tier 1)", "보호무역주의", "복수통화바스켓제도", "본원소득", "본원소득수지", "본원통화", "볼커룰", "부가가치",
        "부가가치기준 무역(TiVA)", "부가가치유발계수/부가가치계수",
        "부동화/무권화", "부실채권정리기금", "부채담보부증권(CDO)", "부채비율", "북미자유무역협정(NAFTA)", "분리결제", "분산원장기술", "분수효과", "불완전경쟁시장", "불태화정책",
        "브레튼우즈체제", "브렉시트(Brexit)", "브릭스", "블록체인", "블록체인과 탈중앙화", "비관측경제(NOE)", "비교우위", "비용인상 인플레이션", "비트코인", "빅데이터",
        "빅맥지수", "사이버리스크", "사전담보제", "사전적 정책방향 제시(forward guidance)", "4차 산업혁명", "사회보장제도", "사회보험", "산업연관표(I/O Tables)",
        "삼불원칙", "상계관세",
        "상대적 빈곤율", "상시감시제도/상시감시전담데스크", "상장지수펀드(ETF)", "상품공동기금(CFC)", "상품수지", "생산세", "생산유발효과", "생산자물가지수(PPI)",
        "생산자제품재고지수", "생산자제품출하지수/생산자출하지수",
        "생활물가지수", "서비스수지", "서킷브레이커", "선물거래", "선물환거래", "선불카드/선불전자지급수단", "선행종합지수", "성장기여도", "세계경제포럼(다보스포럼)",
        "세계무역기구(WTO)",
        "세계은행(World Bank)", "소득5분위배율", "소득교역조건/소득교역조건지수", "소득주도성장", "소비의 비가역성", "소비자동향지수(CSI)", "소비자물가지수(CPI)",
        "소비자심리지수", "소액결제시스템", "속물효과(스놉효과)",
        "수요견인 인플레이션", "수요탄력성", "수입유발계수", "수입징수관/지출관", "수출경합도지수", "수출보험", "수출입물가지수", "수출입물량지수", "수쿠크", "수확체감의 법칙",
        "순상품교역조건", "순안정자금조달비율", "순이자마진(NIM)", "순이체한도제", "숨은 그림(은화)", "슈퍼301조", "스마트계약", "스무딩오퍼레이션", "스왑", "스왑레이트",
        "스태그플레이션", "스탠더드 & 푸어스", "스톡옵션", "스트레스 테스트(위기상황분석)", "시뇨리지", "시스템 리스크", "시스템적으로 중요한 금융기관", "시장리스크", "시장평균환율제도",
        "신용경색",
        "신용레버리지", "신용스프레드", "신용연계증권(CLN)", "신용위험(신용리스크)", "신용창조", "신용파생상품", "신용평가제도", "신용환산율", "신 재생에너지",
        "신주인수권부사채(BW)",
        "신흥시장국채권지수(EMBI+)", "실망실업자", "실물화폐/명목화폐", "실업률", "실업률갭", "실질임금", "실효환율", "아세안+3 거시경제조사기구(AMRO)", "아시아개발은행(ADB)",
        "아시아인프라은행(AIIB)",
        "아시아태평양경제협력체(APEC)", "애그플레이션", "양도성예금증서(CD)", "양적완화정책", "어음관리계좌(CMA)", "어음교환", "업무지속계획", "에너지바우처제도", "엥겔의 법칙",
        "여신심사 가이드라인",
        "여신전문금융회사", "역모기지론", "역선택", "역외금융", "역외펀드", "연방준비제도(FRS)/연방준비은행(FRB)", "연불수출", "연쇄가중법", "연지급수입", "영업잉여",
        "영향력계수", "예금보험제도", "예대금리차(예대마진)", "예대율", "예상손실", "예약자금이체제도", "옵션", "와타나베 부인", "완충자본", "외국환거래법",
        "외국환업무취급기관/외국환은행", "외국환평형기금", "외국환포지션", "외국환포지션한도", "외부자금", "외부효과", "외채/대외채권", "외화가득액/외화가득율", "외화자금시장",
        "외환건전성부담금제도",
        "외환결제리스크", "외환동시결제(PVP)", "외환보유액", "외환스왑거래", "외환시장", "외환전산망", "요소비용", "요소비용 국민소득", "우발부채(채무)", "우발전환사채(코코본드)",
        "운영리스크", "워싱턴 컨센서스", "워크아웃", "원/위안 직거래시장", "원금리스크", "원금이자분리채권(STRIPS)", "위험가중자산/위험가중치", "위험기준자기자본비율(RBC비율)",
        "유동비율", "유동성",
        "유동성 함정", "유동성딜레마", "유동성리스크", "유동성커버리지비율", "유럽부흥개발은행(EBRD)", "유럽연합(EU)", "유럽중앙은행(ECB)", "유로달러(Euro Dollar)",
        "유로마켓(Euro Market)", "유리보(EURIBOR)",
        "유통시장", "은선", "은행경영공시제도", "은행인수어음(BA)", "을기금(Capital B)", "의중임금", "이슬람금융", "이자보상배율", "이전소득수지",
        "이중통화채(dual currency bond)",
        "이표채", "익스포저", "인구고령화", "인적자본", "인터넷뱅킹", "인터넷전문은행", "인플레이션", "일물일가의 법칙", "일반특혜관세", "일중RP제도",
        "일중당좌대출제도", "입금이체", "자금관리서비스(CMS)공동망", "자금순환표", "자금조달비용지수(COFIX)", "자기띠 카드", "자기자본비율", "자동안정화장치", "자발적 실업",
        "자본거래자유화",
        "자본생산성", "자본시장통합법", "자본이동자유화규약", "자본적정성", "자본적지출", "자산건전성 분류", "자산유동화", "자연독점", "자연실업률", "자유무역협정(FTA)",
        "자유재", "작업증명", "잠상", "잠재GDP성장률", "잠재경제활동인구", "장기금융시장(자본시장)", "장기침체", "장내시장", "장단기금리차", "장외시장",
        "재산소득", "재정수지", "재정정책", "재정환율", "저축률/총저축/평균소비성향/평균저축성향", "적기시정조치제도", "전방연쇄효과", "전산업생산지수", "전자금융", "전자금융공동망",
        "전자단기사채", "전자상거래", "전자서명", "전자어음", "전자정보교환제도", "전자지급결제대행", "전자화폐", "전자화폐공동망", "전환사채(CB)", "정규직/비정규직",
        "정보의 비대칭성", "정부당좌예금계정", "정부실패", "정책시차", "정크본드", "제1차 통화조치", "제2차 통화조치", "제로금리정책", "제조업생산능력/가동률지수", "제조업평균가동률갭",
        "조세부담률", "종합금융투자사업자", "죄수의 딜레마", "주가수익비율(PER)", "주가연계증권(ELS)", "주가지수", "주가지수선물거래", "주가지수옵션", "주당순이익(EPS)",
        "주식시장",
        "주택저당증권(MBS)", "중간소비", "중개무역", "중계무역", "중앙거래당사자", "중앙예탁기관", "중앙은행", "중앙은행 여수신제도", "증거금", "증권결제리스크",
        "증권대금동시결제(DVP)", "지급", "지급결제 및 시장인프라 위원회(BIS CPMI)", "지급결제시스템", "지급결제제도 감시", "지급수단", "지급준비자산제도", "지급준비제도",
        "지니계수", "지로(GIRO)",
        "지방은행공동망", "지수기준년", "지역금융협정", "지적소유권", "지정시점처리제도", "지주회사", "직불카드", "직불카드공동망", "직접투자", "진성어음/융통어음",
        "집단대출", "집중도 지수(HHI)", "차액결제선물환(NDF) 거래", "차액결제시스템", "차입매수(LBO)", "채권시가평가", "채권시장", "채권시장안정펀드",
        "채무상환유예(moratorium)", "청산",
        "총고정자본형성", "총산출", "총수입스왑(Total Return Swap)", "총액결제시스템", "최저임금제", "최종대부자 기능", "최종수요/중간수요", "추가경정예산", "추심",
        "추정손실",
        "출구전략", "출금이체", "출자총액제한제도", "치앙마이 이니셔티브(CMI)", "치킨게임", "카르텔", "캐리트레이드", "커버드본드(이중상환청구권부 채권)", "컨트리리스크", "코리보",
        "콜시장", "콜옵션", "크라우드펀딩", "타행환공동망", "탄소배출권", "테이퍼링(tapering)", "테일러 준칙(Taylor's rule)", "텔레뱅킹(폰뱅킹)",
        "토빈세(Tobin tax)", "통합발행제도",
        "통화스왑", "통화승수", "통화안정계정", "통화안정증권", "통화옵션", "통화유통속도", "통화전쟁", "통화정책", "통화정책 운영체제(monetary policy regime)",
        "통화정책 커뮤니케이션",
        "통화정책 파급경로", "통화정책수단", "통화정책체계(monetary policy framework)", "통화지표", "투입계수", "투자율", "투자은행",
        "트리핀 딜레마(Triffin's dilemma)", "특별인출권(SDR)", "특수목적기구(SPV)",
        "파레토최적", "파생금융상품", "펀드", "페더럴펀드", "평가절상", "평가절하", "표면금리", "풋옵션", "프로그램매매", "프로젝트 파이낸싱",
        "피셔효과", "피용자보수", "핀테크", "필립스곡선", "한계비용", "한계소비성향", "한계효용", "한국은행", "한시적 근로자", "한은금융망(BOK-Wire+)",
        "할당관세제도", "합계출산율", "헤지펀드", "현금자동인출기(CD)공동망", "현시비교우위지수(RCA)", "현지금융", "현지법인", "혼합형결제시스템", "홀로그램", "화폐교환",
        "화폐발행/화폐발행액", "화폐의 액면체계", "화폐환수", "환경계정", "환경권", "환리스크", "환리스크헤지", "환매조건부매매/RP/Repo", "환어음", "환율조작국",
        "환전영업자(환전상)", "환차손/환차익", "황금낙하산", "회사채", "회수의문", "후방연쇄효과", "후순위금융채", "후행종합지수", "Beyond GDP", "BIS 자기자본비율",
        "CAMEL-R시스템/ROCA시스템/CACREL시스템", "CLS은행", "CMO", "DebtRank", "EC방식", "FTSE 지수", "G2(Group of Two)",
        "G20(Group of 20)", "G7(Group of Seven)", "GDP갭",
        "GDP디플레이터", "Herstatt 리스크", "IC 카드", "IMF 스탠드바이협약", "IMF 쿼타", "IMF 포지션", "J커브효과", "KIKO", "LIBOR", "M&A",
        "MSCI 지수", "N-B SRS", "P2P대출", "PF-ABCP", "SWIFT", "TED 스프레드", "Treasury Bill(T/B)", "VAN사업자",
        "VaR(Value at Risk)", "VIX"

        # 투자 맟 자산관리
        "가계부실위험지수(HDRI)", "가계수지", "가계순저축률", "가계신용통계", "가계처분가능소득", "고용률", "고용보조지표",
        "고용유발효과/취업유발효과", "고정이하여신비율", "고정분류여신",
        "고정자본소모", "고정환율제도/자유변동환율제도", "경기동향지수(경기확산지수)", "경기종합지수", "경상수지", "경제성장률", "경제심리지수", "경제협력개발기구(OECD)",
        "경제활동인구/비경제활동인구/경제활동참가율", "경제후생지표",
        "고통지수", "국내총생산(GDP)", "국내총투자율", "국민계정체계(SNA)", "국민대차대조표", "국민부담률", "국민소득", "국민소득 3면 등가의 법칙", "국민처분가능소득",
        "국민총소득(GNI)",
        "국가경쟁력지수", "국가신용등급", "국가채무", "국내공급물가지수", "국내신용", "명목GDP목표제", "명목국내총생산/실질국내총생산", "명목금리/실질금리", "명목소득/실질소득",
        "물가지수",
        "부가가치기준 무역(TiVA)", "부가가치유발계수/부가가치계수", "수출경합도지수", "수출입물가지수", "수출입물량지수", "실업률", "실업률갭", "실질임금", "실효환율", "지니계수",
        "생산자물가지수(PPI)", "서비스수지", "순이자마진(NIM)", "총부채상환비율(DTI)", "총부채원리금상환비율(DSR)", "평균소비성향/평균저축성향", "청년실업률", "통상임금",
        "물가안정목표제", "소비자물가지수(CPI)",
        "생활물가지수", "기대인플레이션", "금융중개지원대출제도", "금리스왑", "금리자유화", "금리평가이론", "금본위제", "금융지주회사", "금융채", "금융통화위원회",
        "금전신탁", "기준금리", "기준환율", "기초가격", "기축통화", "긴축정책", "국제금융시장", "국제금융중심지", "국제산업연관표", "국제수지(BOP)",
        "국제수지표", "국제원유가격", "국제통화기금(IMF)", "국제투자대조표(IIP)", "국제회계기준", "국채", "그린본드", "그림자 금융", "금리선물", "금리스왑",
        "금리자유화", "금리평가이론", "금본위제", "금융제도", "금융지주회사", "금융채", "금융통화위원회", "금전신탁", "기업경기실사지수(BSI)", "기준금리",
        "기준환율", "기초가격", "기축통화", "긴축정책", "자본적정성", "자본적지출", "자산건전성 분류", "자산유동화", "자연독점", "자유무역협정(FTA)",
        "자유재", "작업증명", "잠상", "잠재GDP성장률", "잠재경제활동인구", "장기금융시장(자본시장)", "장기침체", "장내시장", "장단기금리차", "장외시장",
        "재산소득", "재정수지", "재정정책", "재정환율", "저축률/총저축/평균소비성향/평균저축성향", "적기시정조치제도", "전방연쇄효과", "전산업생산지수", "전자금융", "전자금융공동망",
        "전자단기사채", "전자상거래", "전자서명", "전자어음", "전자정보교환제도", "전자지급결제대행", "전자화폐", "전자화폐공동망", "전환사채(CB)", "정규직/비정규직",
        "정보의 비대칭성", "정부당좌예금계정", "정부실패", "정책시차", "정크본드", "제1차 통화조치", "제2차 통화조치", "제로금리정책", "제조업생산능력/가동률지수", "제조업평균가동률갭",
        "조세부담률", "종합금융투자사업자", "죄수의 딜레마", "주가수익비율(PER)", "주가연계증권(ELS)", "주가지수", "주가지수선물거래", "주가지수옵션", "주당순이익(EPS)",
        "주식시장",
        "주택저당증권(MBS)", "중간소비", "중개무역", "중계무역", "중앙거래당사자", "중앙예탁기관", "중앙은행", "중앙은행 여수신제도", "증거금", "증권결제리스크",
        "증권대금동시결제(DVP)", "지급", "지급결제 및 시장인프라 위원회(BIS CPMI)", "지급결제시스템", "지급결제제도 감시", "지급수단", "지급준비자산제도", "지급준비제도",
        "지니계수", "지로(GIRO)",
        "지방은행공동망", "지수기준년", "지역금융협정", "지적소유권", "지정시점처리제도", "지주회사", "직불카드", "직불카드공동망", "직접투자", "진성어음/융통어음",
        "집단대출", "집중도 지수(HHI)", "차액결제선물환(NDF) 거래", "차액결제시스템", "차입매수(LBO)", "채권시가평가", "채권시장", "채권시장안정펀드",
        "채무상환유예(moratorium)", "청산",
        "총고정자본형성", "총산출", "총수입스왑(Total Return Swap)", "총액결제시스템", "최저임금제", "최종대부자 기능", "최종수요/중간수요", "추가경정예산", "추심",
        "추정손실",
        "출구전략", "출금이체", "출자총액제한제도", "치앙마이 이니셔티브(CMI)", "치킨게임", "카르텔", "캐리트레이드", "커버드본드(이중상환청구권부 채권)", "컨트리리스크", "코리보",
        "콜시장", "콜옵션", "크라우드펀딩", "타행환공동망", "탄소배출권", "테이퍼링(tapering)", "테일러 준칙(Taylor's rule)", "텔레뱅킹(폰뱅킹)",
        "토빈세(Tobin tax)", "통합발행제도",
        "통화스왑", "통화승수", "통화안정계정", "통화안정증권", "통화옵션", "통화유통속도", "통화전쟁", "통화정책", "통화정책 운영체제(monetary policy regime)",
        "통화정책 커뮤니케이션",
        "통화정책 파급경로", "통화정책수단", "통화정책체계(monetary policy framework)", "통화지표", "투입계수", "투자율", "투자은행",
        "트리핀 딜레마(Triffin's dilemma)", "특별인출권(SDR)", "특수목적기구(SPV)",
        "파레토최적", "파생금융상품", "펀드", "페더럴펀드", "평가절상", "평가절하", "표면금리", "풋옵션", "프로그램매매", "프로젝트 파이낸싱",
        "피셔효과", "피용자보수", "핀테크", "필립스곡선", "한계비용", "한계소비성향", "한계효용", "한국은행", "한시적 근로자", "한은금융망(BOK-Wire+)",
        "할당관세제도", "합계출산율", "헤지펀드", "현금자동인출기(CD)공동망", "현시비교우위지수(RCA)", "현지금융", "현지법인", "혼합형결제시스템", "홀로그램", "화폐교환",
        "화폐발행/화폐발행액", "화폐의 액면체계", "화폐환수", "환경계정", "환경권", "환리스크", "환리스크헤지", "환매조건부매매/RP/Repo", "환어음", "환율조작국",
        "환전영업자(환전상)", "환차손/환차익", "황금낙하산", "회사채", "회수의문", "후방연쇄효과", "후순위금융채", "후행종합지수", "Beyond GDP", "BIS 자기자본비율",
        "CAMEL-R시스템/ROCA시스템/CACREL시스템", "CLS은행", "CMO", "DebtRank", "EC방식", "FTSE 지수", "G2(Group of Two)",
        "G20(Group of 20)", "G7(Group of Seven)", "GDP갭",
        "GDP디플레이터", "Herstatt 리스크", "IC 카드", "IMF 스탠드바이협약", "IMF 쿼타", "IMF 포지션", "J커브효과", "KIKO", "LIBOR", "M&A",
        "MSCI 지수", "N-B SRS", "P2P대출", "PF-ABCP", "SWIFT", "TED 스프레드", "Treasury Bill(T/B)", "VAN사업자",
        "VaR(Value at Risk)", "VIX"
    ]

    finance_category = random.choice(list(finance_categories))
    return finance_category


def get_finance_level(finance_level=None):
    # 예시
    finance_levels = {1, 2, 3, 4, 5}
    if finance_level is None:
        finance_level = random.choice(list(finance_levels))
    return finance_level


# 두 문장씩 분리
def split_text_two(text):
    # 문장을 온점(.) 기준으로 나누기
    sentences = text.split('.')

    # 결과가 빈 문자 열이 아닌 경우 에만 리스트에 추가
    sentences = [sentence.strip() + '.' for sentence in sentences if sentence.strip()]
    sentence_pairs = []

    for i in range(0, len(sentences), 2):
        if i + 1 < len(sentences):
            sentence_pairs.append(sentences[i] + " " + sentences[i + 1])
        else:
            sentence_pairs.append(sentences[i])
    return sentence_pairs


# 한 문장 분리
def split_text(text):
    # 문장을 온점(.) 기준으로 나누기
    sentences = text.split('.')

    # 결과가 빈 문자열이 아닌 경우에만 리스트에 추가
    sentences = [sentence.strip() + '.' for sentence in sentences if sentence.strip()]
    return sentences
