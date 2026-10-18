import streamlit as st

# ------------------------------------------------------------
# 基本設定
# ------------------------------------------------------------
st.set_page_config(
    page_title="適性検査 再現アプリ",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed",
)

TITLE = "通過率6%の適性検査を突破したのに、面接で落ちたあの企業の試験を再現してみた"

# スマホ対応CSS
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 720px;
    }
    h1 { font-size: 1.35rem !important; line-height: 1.5 !important; }
    h2, h3 { font-size: 1.1rem !important; }
    .q-card {
        background: rgba(128,128,128,0.08);
        border-left: 5px solid #4f8bf9;
        border-radius: 8px;
        padding: 0.9rem 1rem;
        margin: 0.5rem 0 1rem 0;
        font-size: 1.02rem;
        line-height: 1.7;
        word-break: break-word;
    }
    .badge {
        display: inline-block;
        background: #4f8bf9;
        color: #fff;
        border-radius: 999px;
        padding: 2px 12px;
        font-size: 0.8rem;
        margin-bottom: 0.4rem;
    }
    .badge.multi { background: #e8590c; }
    .comment-box {
        background: rgba(255,193,7,0.15);
        border-radius: 10px;
        padding: 1rem;
        line-height: 1.8;
        margin-top: 0.5rem;
    }
    div[data-testid="stRadio"] label, div[data-testid="stCheckbox"] label {
        font-size: 1rem;
        line-height: 1.6;
    }
    .stButton > button {
        width: 100%;
        padding: 0.7rem 1rem;
        font-size: 1.05rem;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# 問題データ（すべてオリジナル作成。実在の試験問題ではありません）
# type: "single"=4択 / "multi"=複数選択
# answer: single→正解の添字(int) / multi→正解の添字の集合(set)
# ------------------------------------------------------------
SECTIONS = {
    1: "大問1：リリース前レビュー・品質保証",
    2: "大問2：ビジネス・開発現場のメール構成",
}

QUESTIONS = [
    # ---------------- 大問1 ----------------
    {
        "section": 1,
        "type": "single",
        "text": (
            "会員登録フォームの「氏名」欄に、<code>&lt;script&gt;alert(1)&lt;/script&gt;</code> や "
            "<code>' OR '1'='1</code> のような特殊文字列を入力するテストを行います。"
            "期待される正しい挙動はどれですか。"
        ),
        "options": [
            "入力値をそのまま保存し、確認画面にも加工せず表示する",
            "入力値を無害な文字列として扱い（エスケープ等）、スクリプトや命令として実行されない。必要なら分かりやすい入力エラーを表示する",
            "原因不明のシステムエラー画面（500）が表示されても、異常入力なので問題ない",
            "何も表示せず、入力内容を黙って破棄して登録完了にする",
        ],
        "answer": 1,
        "explain": "特殊文字は「実行されない」「データが壊れない」「ユーザーに状況が伝わる」の3点が基本。黙って破棄や500エラーは不具合として扱います。",
    },
    {
        "section": 1,
        "type": "single",
        "text": "レスポンシブデザインの崩れやリンク切れを確認する観点として、<b>不適切</b>なものはどれですか。",
        "options": [
            "主要な画面幅（スマホ・タブレット・PC）で、横スクロールや要素の重なりがないか確認する",
            "主要なOS・ブラウザの組み合わせで表示を確認する",
            "内部リンク・外部リンクのHTTPステータスを一括チェックし、404などがないか確認する",
            "開発者のPC1台・最新ブラウザ1種類で崩れなければ、全端末で問題ないとみなす",
        ],
        "answer": 3,
        "explain": "環境差異こそ崩れの主因。1環境だけの確認で全端末OKとみなすのは典型的な抜け漏れです。",
    },
    {
        "section": 1,
        "type": "multi",
        "text": "ログイン機能のテストケースとして、<b>優先して含めるべきもの</b>をすべて選んでください。",
        "options": [
            "正しいID・パスワードでログインでき、期待する画面に遷移する（正常系）",
            "誤ったパスワードで失敗し、エラー文言からIDの存在有無が推測できない",
            "ログインボタンの色がブランドカラーと一致しているかのみを確認する",
            "連続して失敗した場合に、アカウントロックや待機などの制限が働く",
            "仕様書に書かれていないので、ログイン失敗時の挙動は確認不要とする",
        ],
        "answer": {0, 1, 3},
        "explain": "正常系・異常系・セキュリティ観点（情報を漏らさない、総当たり対策）の3軸を押さえるのが基本です。",
    },
    {
        "section": 1,
        "type": "single",
        "text": (
            "仕様書に「パスワードは8文字以上20文字以下」とあります。"
            "<b>境界値分析</b>の観点で、優先して確認すべき入力文字数の組み合わせはどれですか。"
        ),
        "options": [
            "7文字、8文字、20文字、21文字",
            "1文字、5文字、10文字、15文字",
            "8文字のみ",
            "0文字と100文字のみ",
        ],
        "answer": 0,
        "explain": "境界値は「境界の内側と外側」。下限（7/8）と上限（20/21）を押さえるのが定石です。",
    },
    {
        "section": 1,
        "type": "multi",
        "text": (
            "ECサイトに「注文キャンセル機能」を追加します。仕様書に書かれていない可能性が高く、"
            "リリース前に<b>仕様の確認・追加テストが必要な観点</b>をすべて選んでください。"
        ),
        "options": [
            "発送処理が始まった後でもキャンセルできるのか、できないのか",
            "キャンセル時の返金処理と在庫の戻し処理が正しく連動するか",
            "キャンセルボタンの文言を担当者の好みに合わせるべきか",
            "ボタンの二重クリックや通信断が起きても、二重キャンセル・二重返金にならないか",
            "仕様書に書いていない動作は、すべて「起きない」ものとして扱う",
        ],
        "answer": {0, 1, 3},
        "explain": "状態遷移（発送後）、他機能との連動（返金・在庫）、異常系（二重操作・通信断）は抜け漏れの定番です。",
    },
    # ---------------- 大問2 ----------------
    {
        "section": 2,
        "type": "multi",
        "text": (
            "クライアントから「システムが落ちている」と報告を受けましたが、原因は不明です。"
            "最初に送る<b>第一報メールに必ず盛り込むべき内容</b>をすべて選んでください。"
        ),
        "options": [
            "確認できている事実（いつから・何が起きているか）と、現時点で把握している影響範囲",
            "原因が判明するまで連絡は控えるため、メールは送らない",
            "現在の対応状況と、次回報告を行う予定時刻",
            "原因は「おそらく○○」という仮説を、確定事項のように書いて安心してもらう",
            "原因が不明な場合は「調査中」と明記し、推測を断定しない",
        ],
        "answer": {0, 2, 4},
        "explain": "第一報は「事実・影響・対応状況・次の報告時刻」。分からないことは分からないと書き、推測を断定しないのが信頼につながります。",
    },
    {
        "section": 2,
        "type": "single",
        "text": "納期遅延のお詫びとリスケジュール打診のメールで、信頼を損ねないために最も適切な構成はどれですか。",
        "options": [
            "お詫びの一文のみ送り、詳細は電話で説明する",
            "遅延の事実・原因・影響を簡潔に伝え、新しい納期案、再発防止策、相手に相談・判断してほしい点を示す",
            "外部要因が原因であることを強調し、お詫びは最小限にとどめる",
            "新しい納期は「なるべく早く」とし、具体的な日付は確定してから連絡する",
        ],
        "answer": 1,
        "explain": "お詫び＋事実＋代替案＋再発防止＋相手への相談点。具体的な日付案がないと、相手は計画を立て直せません。",
    },
    {
        "section": 2,
        "type": "single",
        "text": "開発チームのチャットでバグを報告します。最も的確に伝わる構成はどれですか。",
        "options": [
            "「ログインできません。至急見てください」",
            "結論（何が起きたか）→再現手順→期待結果と実際の結果→発生環境→影響度・緊急度→ログやスクリーンショット",
            "発見までの経緯を、時系列で詳細に長文で書く",
            "「前に言ったやつと同じです」",
        ],
        "answer": 1,
        "explain": "受け手が追加質問なしで再現・判断できることがゴール。結論ファースト＋再現情報＋影響度の順が基本です。",
    },
    {
        "section": 2,
        "type": "multi",
        "text": (
            "進行中の案件で仕様変更が決まり、クライアントへ通知メールを送ります。"
            "<b>盛り込むべき内容</b>をすべて選んでください。"
        ),
        "options": [
            "変更内容（変更前と変更後の違い）",
            "変更に至った理由・背景",
            "スケジュール・費用・他機能への影響範囲",
            "変更は決定事項であり、異論は受け付けない旨",
            "確認や承認をお願いしたい期限と、その返答方法",
            "社内での議論の経緯を、議事録をそのまま全文貼り付けて共有する",
        ],
        "answer": {0, 1, 2, 4},
        "explain": "「何が・なぜ・どんな影響が・相手に何をしてほしいか」を整理して伝えるのが基本。議事録の全文転載や一方的な通告は不適切です。",
    },
    {
        "section": 2,
        "type": "single",
        "text": "他部署のメンバーに、タスクを依頼するメールを送ります。相手が迷わず動けるものとして最も適切なのはどれですか。",
        "options": [
            "「お時間あるときに、確認をお願いします」",
            "依頼内容と目的、期限（日時）、必要な成果物や判断、参考資料、間に合わない場合の連絡依頼を明記する",
            "「至急対応をお願いします」とだけ書く",
            "関係者全員をCCに入れ、「対応状況の共有をお願いします」と書く",
        ],
        "answer": 1,
        "explain": "目的・期限・成果物・資料・例外時の連絡。この5点が揃うと相手が自走できます。",
    },
]

TOTAL = len(QUESTIONS)

# ------------------------------------------------------------
# セッション状態
# ------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "start"  # start / quiz / result
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}  # {問題index: 回答}


def reset_all():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def is_correct(q, ans):
    if ans is None:
        return False
    if q["type"] == "single":
        return ans == q["answer"]
    return set(ans) == q["answer"]


def section_scores():
    scores = {1: 0, 2: 0}
    for i, q in enumerate(QUESTIONS):
        if is_correct(q, st.session_state.answers.get(i)):
            scores[q["section"]] += 1
    return scores


def make_comment(s1, s2):
    total = s1 + s2
    if total == 10:
        return (
            "🏆 満点です。もはやテストの出題者より仕様を理解しています。"
            "これで面接に落ちたなら、原因はスキルではなく『相性』か『採用枠』。気にしすぎず次へ行きましょう。"
        )
    if s1 >= 4 and s2 <= 2:
        return (
            "🤔 テストの点数は優秀ですが、メール問題での取りこぼしが目立ちます。"
            "面接落ちの原因は、文章から漂う『コミュ力不安』だった可能性があります。"
            "技術は通過、報連相で不通過。実務ではよくある話です。"
        )
    if s1 <= 2 and s2 >= 4:
        return (
            "📧 メールは丁寧で好印象。ただ、テスト観点の抜け漏れが多めです。"
            "『感じは良いが、リリースすると本番でバグる人』と判定された恐れがあります。"
        )
    if total >= 8:
        return (
            "👍 かなりの高得点です。通過率6%に入る実力は十分。"
            "それでも落ちたなら、面接官との相性という名のガチャに負けただけかもしれません。"
        )
    if total >= 5:
        return (
            "😐 平均的な出来です。通過率6%の壁は、この『あと一歩の詰めの甘さ』で決まります。"
            "仕様の抜け漏れとメールの結論ファーストを意識すれば一段上に行けます。"
        )
    return (
        "😇 正直、このまま実務に出ると障害対応で胃が痛くなるタイプです。"
        "ただ、気づけたのは収穫。解説を読んで、境界値と第一報の型だけでも持ち帰ってください。"
    )


def rank_label(total):
    if total >= 9:
        return "S"
    if total >= 7:
        return "A"
    if total >= 5:
        return "B"
    if total >= 3:
        return "C"
    return "D"


# ------------------------------------------------------------
# 画面：スタート
# ------------------------------------------------------------
def show_start():
    st.title("📝 " + TITLE)
    st.write(
        "ロジカルシンキングと実務対応力を問う、少し難解な適性検査の雰囲気を再現した全10問です。"
    )
    st.markdown(
        """
- **大問1**：リリース前レビュー・品質保証（5問）
- **大問2**：ビジネス・開発現場のメール構成（5問）
- 単一選択と**複数選択**があります（複数選択は完全一致で正解）
        """
    )
    st.info(
        "⚠️ 本アプリの問題はすべて完全オリジナルです。実在する企業・試験・ツールとは一切関係ありません。"
    )
    if st.button("▶ テストを始める", type="primary"):
        st.session_state.page = "quiz"
        st.session_state.idx = 0
        st.session_state.answers = {}
        st.rerun()


# ------------------------------------------------------------
# 画面：出題
# ------------------------------------------------------------
def show_quiz():
    i = st.session_state.idx
    q = QUESTIONS[i]

    st.progress((i) / TOTAL, text=f"{i + 1} / {TOTAL} 問")
    st.caption(SECTIONS[q["section"]])

    if q["type"] == "multi":
        st.markdown('<span class="badge multi">複数選択</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge">単一選択</span>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="q-card"><b>Q{i + 1}.</b> {q["text"]}</div>',
        unsafe_allow_html=True,
    )

    answer = None
    if q["type"] == "single":
        answer = st.radio(
            "選択肢",
            options=list(range(len(q["options"]))),
            format_func=lambda k: f'{"ABCDEF"[k]}. {q["options"][k]}',
            index=None,
            key=f"ans_{i}",
            label_visibility="collapsed",
        )
        answered = answer is not None
    else:
        st.caption("当てはまるものをすべて選んでください")
        selected = []
        for k, opt in enumerate(q["options"]):
            if st.checkbox(f'{"ABCDEF"[k]}. {opt}', key=f"ans_{i}_{k}"):
                selected.append(k)
        answer = selected
        answered = len(selected) > 0

    is_last = i == TOTAL - 1
    label = "結果を見る ▶" if is_last else "次の問題へ ▶"

    if st.button(label, type="primary", disabled=not answered):
        st.session_state.answers[i] = answer
        if is_last:
            st.session_state.page = "result"
        else:
            st.session_state.idx += 1
        st.rerun()


# ------------------------------------------------------------
# 画面：結果
# ------------------------------------------------------------
def show_result():
    scores = section_scores()
    s1, s2 = scores[1], scores[2]
    total = s1 + s2

    st.title("📊 結果発表")
    st.markdown(f"### 総合スコア：**{total} / {TOTAL}**　ランク **{rank_label(total)}**")
    st.progress(total / TOTAL)

    st.markdown("#### 大問ごとのスコア")
    st.write(f"{SECTIONS[1]}：**{s1} / 5**")
    st.progress(s1 / 5)
    st.write(f"{SECTIONS[2]}：**{s2} / 5**")
    st.progress(s2 / 5)

    st.markdown("#### 総合評価コメント")
    st.markdown(
        f'<div class="comment-box">{make_comment(s1, s2)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("#### 解答と解説")
    for i, q in enumerate(QUESTIONS):
        ans = st.session_state.answers.get(i)
        ok = is_correct(q, ans)
        mark = "✅" if ok else "❌"
        with st.expander(f"{mark} Q{i + 1}（{SECTIONS[q['section']].split('：')[0]}）"):
            st.markdown(q["text"], unsafe_allow_html=True)
            if q["type"] == "single":
                right = [q["answer"]]
                mine = [] if ans is None else [ans]
            else:
                right = sorted(q["answer"])
                mine = sorted(ans) if ans else []
            st.markdown(
                "**あなたの回答：** "
                + (", ".join("ABCDEF"[k] for k in mine) if mine else "未回答")
            )
            st.markdown("**正解：** " + ", ".join("ABCDEF"[k] for k in right))
            for k in right:
                st.markdown(f'- {"ABCDEF"[k]}. {q["options"][k]}')
            st.info(q["explain"])

    if st.button("🔁 もう一度挑戦する"):
        reset_all()
        st.rerun()


# ------------------------------------------------------------
# ルーティング
# ------------------------------------------------------------
page = st.session_state.page
if page == "start":
    show_start()
elif page == "quiz":
    show_quiz()
else:
    show_result()
