import streamlit as st
import datetime

def format_timestamp(milliseconds):
    """ミリ秒をSRT形式のタイムスタンプ(HH:MM:SS,mmm)に変換する"""
    td = datetime.timedelta(milliseconds=milliseconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    millis = int(milliseconds % 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"

def generate_srt(lines, duration_sec):
    srt_content = []
    current_time_ms = 0
    duration_ms = int(duration_sec * 1000)
    
    for i, line in enumerate(lines):
        if i > 0:
            start_ms = current_time_ms + 1
        else:
            start_ms = current_time_ms
            
        end_ms = start_ms + duration_ms if i == 0 else current_time_ms + duration_ms
        
        start_str = format_timestamp(start_ms)
        end_str = format_timestamp(end_ms)
        
        srt_content.append(str(i + 1))
        srt_content.append(f"{start_str} --> {end_str}")
        srt_content.append(line)
        srt_content.append("")
        
        current_time_ms = end_ms
        
    return "\n".join(srt_content)

def main():
    st.set_page_config(page_title="軽量SRTジェネレーター", page_icon="📝", layout="centered")
    
    st.title("📝 軽量SRTジェネレーター")
    st.markdown("""
    テキストエリアに改行区切りで文章を入力すると、指定した秒数間隔のSRT字幕ファイルを生成します。  
    音声処理を行わないため、**一瞬で生成・ダウンロードが可能**な超軽量ツールです。
    """)
    
    st.markdown("---")
    
    duration_sec = st.slider(
        "⏱️ 1行あたりの表示時間 (秒)", 
        min_value=0.5, 
        max_value=10.0, 
        value=1.3, 
        step=0.1
    )
    
    text_input = st.text_area(
        "✍️ 字幕テキストを入力してください (1回の改行 = 1つの字幕ブロック)", 
        height=300,
        placeholder="ここに入力・貼り付けしてください。\n（例）\nこんにちは！\n今日は良い天気ですね。\nそれでは始めていきましょう。"
    )
    
    if text_input:
        lines = [line.strip() for line in text_input.splitlines() if line.strip()]
        
        if lines:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📊 読み込んだ行数 (字幕数)", f"{len(lines)} 行")
            with col2:
                total_chars = sum(len(line) for line in lines)
                st.metric("🔤 総文字数", f"{total_chars} 文字")
                
            srt_output = generate_srt(lines, duration_sec)
            
            st.markdown("---")
            
            # ファイル名に使えない文字を置換し、1行目をファイル名にする
            safe_filename = lines[0].replace("/", "_").replace("\\", "_")[:50] + ".srt"
            
            st.download_button(
                label="📥 SRTファイルをダウンロード",
                data=srt_output,
                file_name=safe_filename,
                mime="text/plain",
                use_container_width=True
            )
            
            st.subheader("👀 SRT プレビュー")
            st.code(srt_output, language="markdown")

if __name__ == "__main__":
    main()
