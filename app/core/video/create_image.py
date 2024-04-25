import os
import urllib
import webbrowser
import openai


def generate_images(prompt_p, api_key_p, clips_info_p):
    client = openai.OpenAI(api_key=api_key_p)

    # 각 프롬프트에 대해 이미지 생성 요청
    for i, prompt in enumerate(prompt_p):
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1792",
            quality="standard"
        )
        # 생성된 이미지 url 열기
        url = response.data[0].url
        webbrowser.open(url)

        # 생성된 이미지 저장
        img_dest = create_image_file_name()

        urllib.request.urlretrieve(url, img_dest)
        clips_info_p.append((img_dest, prompt))


def create_image_file_name():
    """저장할 이미지 파일의 이름을 중복되지 않게 생성"""
    count = 1
    while True:
        image_path = f"./ai_image/ai_image_result_{count}.jpg"
        if not os.path.exists(image_path):
            return image_path
        count += 1


# 2 문장씩 분리
def text_split(text):
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