const speech = require('@google-cloud/speech');
const fs = require('fs');

async function transcribeAudio(audioPath) {
    const client = new speech.SpeechClient();

    const audio = {
        content: fs.readFileSync(`${__dirname}/${audioPath}`).toString('base64'),
    };

    const request = {
        audio: audio,
        config: {
            encoding: 'LINEAR16',
            sampleRateHertz: 16000,
            languageCode: 'en-US',
        },
    };

    const [response] = await client.recognize(request);
    const transcription = response.results
        .map(result => result.alternatives[0].transcript)
        .join('\n');
    console.log('Transcription:', transcription);
}

const audioFilePath = 'audio.wav';
transcribeAudio(audioFilePath);

// console.log({__dirname}/{})
