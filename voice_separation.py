import numpy as np
from pydub import AudioSegment
import librosa

def separate_voices(input_audio, output_audio):
    """
    Separate voices from the input audio by removing one of the background sounds.

    Args:
        input_audio (str): Path to the input audio file.
        output_audio (str): Path to save the output audio file.
    """
    # Load the input audio
    audio = AudioSegment.from_file(input_audio)

    # Convert audio to numpy array
    audio_array = np.array(audio.get_array_of_samples(), dtype=np.float32)  # Convert to floating-point format

    # Get the sample rate
    sample_rate = audio.frame_rate

    # Compute the Short-Time Fourier Transform (STFT)
    stft = librosa.stft(audio_array, n_fft=2048)

    # Compute the magnitude spectrogram
    magnitude = np.abs(stft)

    # Assume the Super Mario background sound has higher frequencies
    # We'll create a simple mask to remove frequencies above a certain threshold
    # You may need to adjust the threshold based on your specific audio
    frequency_threshold = 3000  # Adjust as needed
    mask = np.ones_like(magnitude)
    mask[magnitude > frequency_threshold] = 0

    # Apply the mask to the magnitude spectrogram
    processed_magnitude = magnitude * mask

    # Invert the STFT to obtain the processed audio
    processed_audio_array = librosa.istft(processed_magnitude)

    # Convert the processed audio array back to AudioSegment
    processed_audio = AudioSegment(
        processed_audio_array.tobytes(),
        frame_rate=sample_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )

    # Save the processed audio
    processed_audio.export(output_audio, format="wav")
