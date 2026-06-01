import unittest
import numpy as np
import wave
from pathlib import Path

# Add project root to path to resolve backend imports
import sys
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.app.utils.audio_analysis import analyze_audio_features
from backend.app.utils.detection_engine import detect_viral_moments

class TestViralMomentDetection(unittest.TestCase):
    def setUp(self):
        self.test_wav_path = Path("test_synthetic_audio.wav")
        self.generate_synthetic_audio(self.test_wav_path)

    def tearDown(self):
        if self.test_wav_path.exists():
            self.test_wav_path.unlink()

    def generate_synthetic_audio(self, path: Path):
        """
        Generates a 15-second synthetic WAV file:
        - 0-5s: Quiet background noise (100Hz)
        - 5-8s: Loud screaming/cheering frequency (3000Hz)
        - 8-15s: Quiet background noise (100Hz)
        """
        # Seed the random generator for 100% deterministic unit tests
        np.random.seed(42)
        
        sample_rate = 16000
        duration = 15
        num_samples = sample_rate * duration
        t = np.linspace(0, duration, num_samples, endpoint=False)
        
        # 1. Quiet baseline background noise
        audio = np.random.normal(0, 100, num_samples)
        
        # 2. Add quiet 100Hz hum throughout
        audio += 200 * np.sin(2 * np.pi * 100 * t)
        
        # 3. Add loud, high-frequency screaming/cheering outburst at 5s to 8s
        outburst_mask = (t >= 5.0) & (t <= 8.0)
        # High frequency 2500Hz wave at large amplitude (15000)
        audio[outburst_mask] += 15000 * np.sin(2 * np.pi * 2500 * t[outburst_mask])
        
        # Clip to 16-bit PCM limits
        audio = np.clip(audio, -32768, 32767).astype(np.int16)
        
        # Write to WAV
        with wave.open(str(path), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2) # 16-bit
            wav.setframerate(sample_rate)
            wav.writeframes(audio.tobytes())

    def test_audio_analysis_extraction(self):
        """
        Asserts that physical audio wave features (RMS, volume spikes, frequency) are extracted correctly.
        """
        features = analyze_audio_features(self.test_wav_path)
        
        self.assertEqual(features['duration_seconds'], 15)
        self.assertEqual(len(features['rms_energy']), 15)
        self.assertEqual(len(features['volume_spikes']), 15)
        self.assertEqual(len(features['high_freq_ratios']), 15)
        
        # Verify that the outburst seconds (5, 6, 7) show a volume spike and higher high-frequency ratio
        outburst_spikes = features['volume_spikes'][5:8]
        quiet_spikes_pre = features['volume_spikes'][0:4]
        quiet_spikes_post = features['volume_spikes'][9:14]
        
        self.assertTrue(all(s > 1.5 for s in outburst_spikes))
        self.assertTrue(all(s < 0.5 for s in quiet_spikes_pre))
        self.assertTrue(all(s < 0.5 for s in quiet_spikes_post))

        # High frequency ratio should be elevated
        outburst_freqs = features['high_freq_ratios'][5:8]
        quiet_freqs = features['high_freq_ratios'][0:4]
        self.assertTrue(np.mean(outburst_freqs) > np.mean(quiet_freqs))

    def test_viral_detection_scoring(self):
        """
        Asserts that the highlight engine correctly aggregates scores and detects the outburst.
        """
        # Run physical audio analysis
        audio_features = analyze_audio_features(self.test_wav_path)
        
        # Generate dummy empty transcript features
        transcript_features = {
            'language': 'en',
            'duration': 15.0,
            'full_text': '',
            'segments': [],
            'keyword_hits': [],
            'speech_rates': []
        }
        
        moments = detect_viral_moments(
            audio_features=audio_features, 
            transcript_features=transcript_features,
            niche="streamer",
            clip_count=5
        )
        
        self.assertTrue(len(moments) > 0)
        
        top_moment = moments[0]
        
        print(f"\n[TEST] Streamer Top Moment Score: {top_moment['viral_score']}")
        print(f"[TEST] Hook: {top_moment['hook_score']}% | Tension: {top_moment['tension_score']}% | Payoff: {top_moment['payoff_score']}% | Resolution: {top_moment['resolution_score']}%")
        
        self.assertTrue(top_moment['viral_score'] >= 45.0)
        
        # The start and end time should cover our synthetic outburst (5s to 8s) with safety buffers
        self.assertAlmostEqual(top_moment['start_time'], 2.0, delta=0.5)
        self.assertAlmostEqual(top_moment['end_time'], 12.0, delta=0.5)
        
        # Verify score breakdowns
        self.assertTrue(top_moment['loudness_score'] > 30.0)
        self.assertTrue(top_moment['contrast_score'] > 50.0)
        self.assertTrue(top_moment['frequency_score'] > 50.0)
        
        # Verify Emotional Arc breakdown
        self.assertTrue(top_moment['hook_score'] >= 0.0)
        self.assertTrue(top_moment['tension_score'] >= 0.0)
        self.assertTrue(top_moment['payoff_score'] > 50.0)
        self.assertTrue(top_moment['resolution_score'] > 40.0)

if __name__ == "__main__":
    unittest.main()
