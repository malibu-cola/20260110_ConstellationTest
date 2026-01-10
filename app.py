import streamlit as st
import json
import random
from pathlib import Path

# データ読み込み
@st.cache_data
def load_constellations():
    data_path = Path(__file__).parent / "data" / "constellations.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def init_session_state():
    if "mode" not in st.session_state:
        st.session_state.mode = "home"
    if "card_index" not in st.session_state:
        st.session_state.card_index = 0
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False
    if "shuffled_data" not in st.session_state:
        st.session_state.shuffled_data = []
    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "quiz_answered" not in st.session_state:
        st.session_state.quiz_answered = False
    if "quiz_type" not in st.session_state:
        st.session_state.quiz_type = "japanese_to_latin"
    if "answer_mode" not in st.session_state:
        st.session_state.answer_mode = "choice"
    if "choices" not in st.session_state:
        st.session_state.choices = []
    if "user_answer" not in st.session_state:
        st.session_state.user_answer = ""
    if "is_correct" not in st.session_state:
        st.session_state.is_correct = None

def reset_quiz():
    st.session_state.quiz_index = 0
    st.session_state.score = 0
    st.session_state.quiz_answered = False
    st.session_state.is_correct = None
    st.session_state.user_answer = ""
    st.session_state.choices = []

def shuffle_data(data):
    shuffled = data.copy()
    random.shuffle(shuffled)
    return shuffled

def get_question_and_answer(constellation, quiz_type):
    if quiz_type == "japanese_to_latin":
        return constellation["japanese"], constellation["latin"]
    elif quiz_type == "japanese_to_abbr":
        return constellation["japanese"], constellation["abbr"]
    elif quiz_type == "abbr_to_japanese":
        return constellation["abbr"], constellation["japanese"]

def generate_choices(correct_answer, all_data, quiz_type):
    if quiz_type == "japanese_to_latin":
        all_answers = [c["latin"] for c in all_data]
    elif quiz_type == "japanese_to_abbr":
        all_answers = [c["abbr"] for c in all_data]
    elif quiz_type == "abbr_to_japanese":
        all_answers = [c["japanese"] for c in all_data]

    wrong_answers = [a for a in all_answers if a != correct_answer]
    choices = random.sample(wrong_answers, min(3, len(wrong_answers)))
    choices.append(correct_answer)
    random.shuffle(choices)
    return choices

def home_page():
    st.title("88星座テスト")
    st.markdown("IAUが定める88星座の名称を学習・テストするアプリです")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("フラッシュカード")
        st.write("カードをめくって星座を学習します")
        if st.button("フラッシュカードを始める", use_container_width=True):
            data = load_constellations()
            st.session_state.shuffled_data = shuffle_data(data)
            st.session_state.card_index = 0
            st.session_state.show_answer = False
            st.session_state.mode = "flashcard"
            st.rerun()

    with col2:
        st.subheader("クイズ")
        st.write("問題に答えて理解度をチェック")
        if st.button("クイズを始める", use_container_width=True):
            st.session_state.mode = "quiz_setup"
            st.rerun()

def flashcard_page():
    st.title("フラッシュカード")

    if st.button("← ホームに戻る"):
        st.session_state.mode = "home"
        st.rerun()

    data = st.session_state.shuffled_data
    index = st.session_state.card_index

    st.progress((index + 1) / len(data))
    st.write(f"カード {index + 1} / {len(data)}")

    constellation = data[index]

    st.markdown("---")

    # カード表示
    st.markdown(f"### {constellation['japanese']}")

    if st.session_state.show_answer:
        st.success(f"**学名:** {constellation['latin']}")
        st.info(f"**略称:** {constellation['abbr']}")
    else:
        st.markdown("*クリックして答えを表示*")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if index > 0:
            if st.button("← 前へ", use_container_width=True):
                st.session_state.card_index -= 1
                st.session_state.show_answer = False
                st.rerun()

    with col2:
        if st.session_state.show_answer:
            if st.button("隠す", use_container_width=True):
                st.session_state.show_answer = False
                st.rerun()
        else:
            if st.button("答えを見る", use_container_width=True):
                st.session_state.show_answer = True
                st.rerun()

    with col3:
        if index < len(data) - 1:
            if st.button("次へ →", use_container_width=True):
                st.session_state.card_index += 1
                st.session_state.show_answer = False
                st.rerun()
        else:
            if st.button("シャッフル", use_container_width=True):
                st.session_state.shuffled_data = shuffle_data(data)
                st.session_state.card_index = 0
                st.session_state.show_answer = False
                st.rerun()

def quiz_setup_page():
    st.title("クイズ設定")

    if st.button("← ホームに戻る"):
        st.session_state.mode = "home"
        st.rerun()

    st.markdown("---")

    st.subheader("出題形式")
    quiz_type = st.radio(
        "問題の種類を選んでください",
        options=["japanese_to_latin", "japanese_to_abbr", "abbr_to_japanese"],
        format_func=lambda x: {
            "japanese_to_latin": "日本語 → 学名",
            "japanese_to_abbr": "日本語 → 略称",
            "abbr_to_japanese": "略称 → 日本語"
        }[x]
    )

    st.subheader("回答方式")
    answer_mode = st.radio(
        "回答方式を選んでください",
        options=["choice", "input"],
        format_func=lambda x: {
            "choice": "選択式（4択）",
            "input": "入力式"
        }[x]
    )

    st.markdown("---")

    if st.button("クイズ開始", type="primary", use_container_width=True):
        data = load_constellations()
        st.session_state.shuffled_data = shuffle_data(data)
        st.session_state.quiz_type = quiz_type
        st.session_state.answer_mode = answer_mode
        reset_quiz()
        st.session_state.mode = "quiz"
        st.rerun()

def quiz_page():
    st.title("クイズ")

    data = st.session_state.shuffled_data
    index = st.session_state.quiz_index
    quiz_type = st.session_state.quiz_type
    answer_mode = st.session_state.answer_mode

    # 全問終了
    if index >= len(data):
        st.balloons()
        st.success(f"クイズ終了！ スコア: {st.session_state.score} / {len(data)}")

        percentage = (st.session_state.score / len(data)) * 100
        st.progress(percentage / 100)
        st.write(f"正答率: {percentage:.1f}%")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("もう一度", use_container_width=True):
                st.session_state.shuffled_data = shuffle_data(data)
                reset_quiz()
                st.rerun()
        with col2:
            if st.button("ホームに戻る", use_container_width=True):
                st.session_state.mode = "home"
                st.rerun()
        return

    st.progress((index + 1) / len(data))
    st.write(f"問題 {index + 1} / {len(data)} | スコア: {st.session_state.score}")

    constellation = data[index]
    question, correct_answer = get_question_and_answer(constellation, quiz_type)

    st.markdown("---")

    # 問題タイプの表示
    type_label = {
        "japanese_to_latin": "学名を答えてください",
        "japanese_to_abbr": "略称（3文字）を答えてください",
        "abbr_to_japanese": "日本語名を答えてください"
    }[quiz_type]

    st.write(type_label)
    st.markdown(f"## {question}")

    st.markdown("---")

    if answer_mode == "choice":
        # 選択式
        if not st.session_state.quiz_answered:
            if not st.session_state.choices:
                st.session_state.choices = generate_choices(correct_answer, data, quiz_type)

            for choice in st.session_state.choices:
                if st.button(choice, use_container_width=True, key=f"choice_{choice}"):
                    st.session_state.quiz_answered = True
                    st.session_state.user_answer = choice
                    if choice == correct_answer:
                        st.session_state.score += 1
                        st.session_state.is_correct = True
                    else:
                        st.session_state.is_correct = False
                    st.rerun()
        else:
            if st.session_state.is_correct:
                st.success(f"正解！ 答え: {correct_answer}")
            else:
                st.error(f"不正解... 正解は: {correct_answer}")
                st.write(f"あなたの回答: {st.session_state.user_answer}")

            if st.button("次の問題へ →", use_container_width=True):
                st.session_state.quiz_index += 1
                st.session_state.quiz_answered = False
                st.session_state.is_correct = None
                st.session_state.choices = []
                st.session_state.user_answer = ""
                st.rerun()

    else:
        # 入力式
        if not st.session_state.quiz_answered:
            user_input = st.text_input("回答を入力してください", key="quiz_input")

            if st.button("回答する", use_container_width=True):
                st.session_state.quiz_answered = True
                st.session_state.user_answer = user_input.strip()

                # 大文字小文字を無視して比較
                if user_input.strip().lower() == correct_answer.lower():
                    st.session_state.score += 1
                    st.session_state.is_correct = True
                else:
                    st.session_state.is_correct = False
                st.rerun()
        else:
            if st.session_state.is_correct:
                st.success(f"正解！ 答え: {correct_answer}")
            else:
                st.error(f"不正解... 正解は: {correct_answer}")
                st.write(f"あなたの回答: {st.session_state.user_answer}")

            if st.button("次の問題へ →", use_container_width=True):
                st.session_state.quiz_index += 1
                st.session_state.quiz_answered = False
                st.session_state.is_correct = None
                st.session_state.user_answer = ""
                st.rerun()

    st.markdown("---")
    if st.button("クイズを終了"):
        st.session_state.mode = "home"
        st.rerun()

def main():
    st.set_page_config(
        page_title="88星座テスト",
        page_icon="⭐",
        layout="centered"
    )

    init_session_state()

    if st.session_state.mode == "home":
        home_page()
    elif st.session_state.mode == "flashcard":
        flashcard_page()
    elif st.session_state.mode == "quiz_setup":
        quiz_setup_page()
    elif st.session_state.mode == "quiz":
        quiz_page()

if __name__ == "__main__":
    main()
