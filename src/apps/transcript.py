import openai
import streamlit as st
import queue
import time
import pydub
from moviepy.editor import VideoFileClip
from pathlib import Path
from streamlit_webrtc import WebRtcMode, webrtc_streamer

client = openai.OpenAI()

PASTA_TEMP = Path(__file__).parent / "../temp"
PASTA_TEMP.mkdir(exist_ok=True)
ARQUIVO_AUDIO_TEMP = PASTA_TEMP / "audio.mp3"
ARQUIVO_VIDEO_TEMP = PASTA_TEMP / "video.mp4"
ARQUIVO_MIC_TEMP = PASTA_TEMP / "mic.mp3"


def transcreve_audio(caminho_audio, prompt):
    with open(caminho_audio, "rb") as arquivo_audio:
        transcricao = client.audio.transcriptions.create(
            model="whisper-1",
            language="pt",
            response_format="text",
            file=arquivo_audio,
            prompt=prompt,
        )
        return transcricao


def transcreve_tab_mic():
    prompt_mic = st.text_input("(opcional) Digite o seu prompt", key="input_mic")
    webrtx_ctx = webrtc_streamer(
        key="recebe_audio",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        media_stream_constraints={"video": False, "audio": True},
    )

    if not webrtx_ctx.state.playing:
        return

    container = st.empty()
    container.markdown("Comece a falar...")
    chunk_audio = pydub.AudioSegment.empty()
    while True:
        if webrtx_ctx.audio_receiver:
            try:
                frames_de_audio = webrtx_ctx.audio_receiver.get_frames(timeout=1)

            except queue.Empty:
                time.sleep(0.1)
                continue

            for frame in frames_de_audio:
                sound = pydub.AudioSegment(
                    data=frame.to_ndarray().tobytes(),
                    sample_width=frame.format.bytes,
                    frame_rate=frame.sample_rate,
                    channels=len(frame.layout.channels),
                )
                print(f"sound => {sound}")
                chunk_audio += sound

            if len(chunk_audio) > 0:
                container.markdown("Salvando aúdio")
                chunk_audio.export(ARQUIVO_MIC_TEMP)

            container.markdown(f"Frames recebidos {len(frames_de_audio)}")
        else:
            break


def transcreve_tab_video():
    prompt_input = st.text_input("(opcional) Digite o seu prompt", key="input_video")
    arquivo_video = st.file_uploader("Adicione um arquivo de vídeo .mp4", type=["mp4"])

    if not arquivo_video is None:
        with open(ARQUIVO_VIDEO_TEMP, mode="wb") as video_f:
            video_f.write(arquivo_video.read())
        moviepy_video = VideoFileClip(str(ARQUIVO_VIDEO_TEMP))
        moviepy_video.audio.write_audiofile(str(ARQUIVO_AUDIO_TEMP))

        transcricao = transcreve_audio(ARQUIVO_AUDIO_TEMP, prompt_input)
        st.write(transcricao)


def transcreve_tab_audio():
    prompt = st.text_input("(opcional) Digite o seu prompt", key="input_audio")
    arquivo_audio = st.file_uploader("Adicione um arquivo de áudio .mp3", type=["mp3"])

    if not arquivo_audio is None:
        transcricao = transcreve_audio(ARQUIVO_AUDIO_TEMP, prompt)
        st.write(transcricao)


def main():
    st.header("Bem-vindo ao Transcript🎙️")
    st.markdown("#### Transcreva aúdio do microfone, vídeos e áudios.")
    tab_mic, tab_video, tab_audio = st.tabs(["Microfone", "Vídeo", "Áudio"])

    with tab_mic:
        transcreve_tab_mic()
    with tab_video:
        transcreve_tab_video()
    with tab_audio:
        transcreve_tab_audio()


if __name__ == "__main__":
    main()
