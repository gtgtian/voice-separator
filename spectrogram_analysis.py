import numpy as np
import matplotlib.pyplot as plt
import librosa.display

def analyze_spectrogram(input_audio):
    """
    Analyze the spectrogram of an input audio file.

    Args:
        input_audio (str): Path to the input audio file.
    """
    # Load the input audio
    audio, sample_rate = librosa.load(input_audio)

    # Compute the Short-Time Fourier Transform (STFT)
    stft = librosa.stft(audio)

    # Compute the magnitude spectrogram
    magnitude = np.abs(stft)

    # Display the spectrogram
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa.amplitude_to_db(magnitude, ref=np.max), sr=sample_rate, x_axis='time', y_axis='hz')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.savefig('static/spectrogram.png')  # Save the spectrogram as a PNG file
    plt.close()
