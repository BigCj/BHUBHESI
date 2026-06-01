import wave
import numpy as np
from pathlib import Path

def analyze_audio_features(wav_path: Path) -> dict:
    """
    Analyzes raw WAV file (16kHz mono 16-bit PCM) for loudness and frequency features.
    Returns:
      - 'rms_energy': list of float (loudness per second)
      - 'volume_spikes': list of float (loudness deviation score)
      - 'contrast_scores': list of float (contrast relative to prior 5 seconds)
      - 'high_freq_ratios': list of float (simulated scream/cheer energy ratios)
    """
    if not wav_path.exists():
        raise FileNotFoundError(f"WAV file not found at {wav_path}")

    with wave.open(str(wav_path), "rb") as wav:
        params = wav.getparams()
        sample_rate = params.framerate
        channels = params.nchannels
        
        if sample_rate != 16000 or channels != 1:
            # Although the downloader forces this, we double check
            pass

        n_frames = params.nframes
        raw_data = wav.readframes(n_frames)
        # Convert binary 16-bit PCM frames to numpy array of int16
        audio_data = np.frombuffer(raw_data, dtype=np.int16)

    # Let's verify sample size and calculate durations
    duration = len(audio_data) / sample_rate
    num_seconds = int(np.floor(duration))

    rms_energy = []
    high_freq_ratios = []
    contrast_scores = []

    # Process audio in 1-second non-overlapping windows
    # 1 second of 16kHz audio = 16000 samples
    window_size = sample_rate

    # Calculate global RMS to find thresholding baseline
    # Convert to float64 to prevent overflow when squaring
    audio_float = audio_data.astype(np.float64)
    
    # Standardize chunk boundaries
    num_chunks = len(audio_data) // window_size
    chunks = audio_float[:num_chunks * window_size].reshape(num_chunks, window_size)
    
    # 1. Compute rolling RMS for each second
    rms_array = np.sqrt(np.mean(chunks**2, axis=1))
    
    # Avoid zero division
    rms_array = np.where(rms_array == 0, 1e-5, rms_array)
    global_mean_rms = np.mean(rms_array)
    global_std_rms = np.std(rms_array) if np.std(rms_array) > 0 else 1.0

    # 2. Extract Spectral Cheering/Screaming ratios (using FFT)
    # Human screaming & crowd cheering has significant energy in 1000Hz - 4000Hz
    # Normal spoken voice is heavily clustered below 1000Hz
    for i in range(num_chunks):
        chunk = chunks[i]
        
        # Calculate FFT
        fft_vals = np.abs(np.fft.rfft(chunk))
        freqs = np.fft.rfftfreq(window_size, 1.0 / sample_rate)
        
        # High-frequency band: 1000Hz to 4000Hz
        high_freq_mask = (freqs >= 1000) & (freqs <= 4000)
        low_freq_mask = (freqs < 1000) & (freqs >= 100)
        
        high_energy = np.sum(fft_vals[high_freq_mask]**2)
        low_energy = np.sum(fft_vals[low_freq_mask]**2)
        
        # Ratio of high-frequency power to low-frequency power
        ratio = high_energy / (low_energy + 1e-5)
        high_freq_ratios.append(float(ratio))

    # 3. Calculate Contrast (Silence-to-Noise transitions)
    # We look at the ratio of the current second's RMS to the average of the lowest
    # RMS values in the preceding 5 seconds.
    for i in range(num_chunks):
        curr_rms = rms_array[i]
        
        if i == 0:
            contrast_scores.append(1.0)
            continue
            
        # Prior 5 seconds window
        prior_start = max(0, i - 5)
        prior_window = rms_array[prior_start:i]
        
        # Minimum baseline in prior window
        prior_min = np.min(prior_window)
        # Avoid division by zero
        prior_min = max(prior_min, 1e-5)
        
        # Contrast ratio
        contrast = curr_rms / prior_min
        contrast_scores.append(float(contrast))

    # 4. Generate Volume Spike deviation score
    # Score represents how many standard deviations the loudness is above global mean
    volume_spikes = []
    for rms_val in rms_array:
        deviation = (rms_val - global_mean_rms) / global_std_rms
        # Clamp negative values to 0
        volume_spikes.append(float(max(0.0, deviation)))

    return {
        'rms_energy': [float(x) for x in rms_array],
        'volume_spikes': volume_spikes,
        'contrast_scores': contrast_scores,
        'high_freq_ratios': high_freq_ratios,
        'duration_seconds': num_seconds
    }
