import streamlit as st
import math

# --- ページ設定 ---
st.set_page_config(page_title="W ⇄ dBμV 変換アプリ", layout="centered")

# --- 見た目の設定（CSS） ---
st.markdown("""
    <style>
    /* クレジット表示用のCSS */
    .credit {
        text-align: right;
        font-size: 14px;
        color: #666;
        margin-bottom: -20px;
    }
    /* 入力欄のラベルスタイル */
    .stNumberInput label {
        font-size: 28px !important;
        color: #22c55e !important;
        font-weight: 800 !important;
        line-height: 1.5;
    }
    /* 入力枠のスタイル */
    div[data-baseweb="input"] {
        height: 60px !important;
        font-size: 28px !important;
        border: 3px solid #22c55e !important;
        border-radius: 10px;
    }
    /* 結果表示ボックス */
    .result-box {
        background-color: #f0fff4;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #22c55e;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 右上にクレジットを表示
st.markdown('<p class="credit">開発/制作：緒方</p>', unsafe_allow_html=True)

st.title('📡 W ⇄ dBμV 相互変換アプリ')
st.markdown("---")

# --- 入力切替セクション ---
mode = st.radio("入力する単位を選択してください", ["W (ワット) を入力", "dBμV を入力"], horizontal=True)

w_val = 0.0
dbuv_val = 0.0

if mode == "W (ワット) を入力":
    # 入力は小数点4桁まで受け入れ
    w_in = st.number_input("電力 (W)", value=1.000, format="%.4f", step=0.001)
    w_val = w_in
    # W -> V -> dBμV (50Ω)
    v_val = math.sqrt(w_in * 50)
    if v_val > 0:
        dbuv_val = 20 * math.log10(v_val * 10**6)
    else:
        dbuv_val = -float('inf')
else:
    dbuv_in = st.number_input("電圧レベル (dBμV)", value=120.0, format="%.2f", step=1.0)
    dbuv_val = dbuv_in
    # dBμV -> V -> W (50Ω)
    v_val = 10 ** ((dbuv_in - 120) / 20)
    w_val = (v_val ** 2) / 50

# --- 共通計算 (dBmなど) ---
mw_val = w_val * 1000
if mw_val > 0:
    dbm_val = 10 * math.log10(mw_val)
else:
    dbm_val = -float('inf')

# --- 表示セクション ---
st.markdown('<div class="result-box">', unsafe_allow_html=True)
st.subheader("📊 変換結果 (50Ω系)")

col1, col2 = st.columns(2)
with col1:
    # 電力をW単位で小数点以下3桁表示
    st.metric("電力 (W)", f"{w_val:.3f} W")
    # 電圧をV単位で小数点以下3桁表示
    st.metric("電圧 (V)", f"{v_val:.3f} V")

with col2:
    st.metric("電圧レベル (dBμV)", f"{dbuv_val:.2f} dBμV")
    st.metric("電力 (dBm)", f"{dbm_val:.2f} dBm")

st.write(f"（参考）電力 (mW): **{mw_val:,.2f} mW**")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("💡 表示設定: 電力(W)および電圧(V)は小数点以下3桁で表示しています。")
