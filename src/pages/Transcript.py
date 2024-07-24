import openai
import streamlit as st 

client = openai.OpenAI()

def transcreve_tab_mic():
    st.markdown('Transcreve microfone')
    
def transcreve_tab_video():
    st.markdown('Transcreve vídeo')

def transcreve_tab_audio():
    prompt = st.text_input("(opcional) Digite o seu prompt", key="input_audio")
    arquivo_audio = st.file_uploader("Adicione um arquivo de áudio .mp3", type=["mp3"])

    if arquivo_audio:
        transcricao = client.audio.transcriptions.create(
            model="whisper-1",
            language="pt",
            response_format="text",
            file=arquivo_audio,
            prompt=prompt,
            
        )
        
        st.write(transcricao)
def main():
    st.header("Bem-vindo ao Transcript🎙️")
    st.markdown("#### Transcreva aúdio do microfone, de vídeos e de arquivos de áudio")
    tab_mic, tab_video, tab_audio = st.tabs(["Microfone", "Vídeo", "Áudio"])
    
    with tab_mic:
        transcreve_tab_mic()
    with tab_video:
        transcreve_tab_video() 
    with tab_audio:
        transcreve_tab_audio()    
    

if __name__ == "__main__":
    main()
# arquivo_audio = open('src/learning/files/original.mp3', mode='rb')
# prompt = 'Olá, seja bem-vindo à Asimov Academy. Meu nome é Rodrigo Soares Tadewald e ensino Python!'

# transcricao = client.audio.transcriptions.create(
#     model='whisper-1',
#     language='pt',
#     response_format='text',
#     file=arquivo_audio,
#     prompt=prompt
# )
# print(transcricao)