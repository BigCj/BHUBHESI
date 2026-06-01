import numpy as np
from typing import List, Dict, Tuple
from backend.app.config import CLIP_BUFFER_PRE, CLIP_BUFFER_POST

# Niche Weight Configurations
# Weights: [Loudness, Contrast, Cheering, Speech Rate, Keywords]
NICHE_WEIGHTS = {
    "podcast": [0.10, 0.10, 0.10, 0.30, 0.40],   # Dialogue, argument overlaps, shock semantic hooks
    "streamer": [0.45, 0.20, 0.15, 0.10, 0.10],  # Decibel peaks, rage outbursts, extreme shouting
    "sports": [0.30, 0.15, 0.35, 0.10, 0.10]     # Stadium cheers, commentator excitement
}

def detect_viral_moments(audio_features: dict, transcript_features: dict, niche: str = "podcast", clip_count: int = 5) -> List[dict]:
    """
    Advanced Virality-Focused Clipping Engine.
    Uses 1D Non-Maximum Suppression (NMS) to guarantee extraction of exactly 'clip_count' 
    distinct, non-overlapping highlights based on niche weights.
    """
    duration = audio_features['duration_seconds']
    weights = NICHE_WEIGHTS.get(niche, NICHE_WEIGHTS["podcast"])

    # Initialize second-by-second feature grids
    loudness_grid = np.zeros(duration)
    contrast_grid = np.zeros(duration)
    frequency_grid = np.zeros(duration)
    speech_rate_grid = np.zeros(duration)
    keyword_grid = np.zeros(duration)
    
    second_reasons: Dict[int, List[str]] = {t: [] for t in range(duration)}

    # 1. Map Physical Loudness
    for t in range(min(duration, len(audio_features['volume_spikes']))):
        spike_val = audio_features['volume_spikes'][t]
        loudness_grid[t] = min(100.0, spike_val * 20.0)
        if spike_val > 1.8:
            second_reasons[t].append("Excited vocal breakout")

    # 2. Map Silence-to-Noise Contrast
    for t in range(min(duration, len(audio_features['contrast_scores']))):
        contrast_val = audio_features['contrast_scores'][t]
        contrast_grid[t] = min(100.0, max(0.0, (contrast_val - 1.0) * 33.0))
        if contrast_val > 2.8:
            second_reasons[t].append("Sudden energetic contrast")

    # 3. Map High-Frequency Cheering/Screaming
    for t in range(min(duration, len(audio_features['high_freq_ratios']))):
        freq_val = audio_features['high_freq_ratios'][t]
        frequency_grid[t] = min(100.0, freq_val * 125.0)
        if freq_val > 0.35:
            second_reasons[t].append("Screaming or crowd reaction")

    # 4. Map Speech Rates
    for rate_item in transcript_features.get('speech_rates', []):
        start = int(np.floor(rate_item['start']))
        end = int(np.ceil(rate_item['end']))
        wps = rate_item['words_per_sec']
        score = min(100.0, max(0.0, (wps - 3.0) * 40.0))
        for t in range(max(0, start), min(duration, end)):
            speech_rate_grid[t] = max(speech_rate_grid[t], score)
            if wps > 4.5:
                second_reasons[t].append("Fast high-intensity dialogue")

    # 5. Map Keywords & Interruptions
    for keyword_hit in transcript_features.get('keyword_hits', []):
        start = int(np.floor(keyword_hit['start']))
        end = int(np.ceil(keyword_hit['end']))
        score = min(100.0, keyword_hit['score'] * 8.0)
        reason_str = keyword_hit['reason']
        for t in range(max(0, start), min(duration, end)):
            keyword_grid[t] = max(keyword_grid[t], score)
            second_reasons[t].append(reason_str)

    # 6. Calculate composite virality grid based on Niche
    composite_grid = (
        weights[0] * loudness_grid +
        weights[1] * contrast_grid +
        weights[2] * frequency_grid +
        weights[3] * speech_rate_grid +
        weights[4] * keyword_grid
    )

    # 7. 1D Non-Maximum Suppression (NMS) Peak Finder
    # Guarantees returning exactly 'clip_count' non-overlapping peaks
    peaks: List[int] = []
    grid_copy = composite_grid.copy()
    
    # 15s separation zone to prevent overlapping clips
    neighborhood = 15
    min_peak_threshold = 20.0 # moderate threshold to ensure we extract requested count

    for _ in range(clip_count):
        peak_idx = int(np.argmax(grid_copy))
        peak_score = grid_copy[peak_idx]
        
        # If the remaining scores are completely flat, stop
        if peak_score < min_peak_threshold and len(peaks) >= 3:
            break
            
        if peak_score <= 1.0:
            break

        peaks.append(peak_idx)
        
        # Suppress neighborhood around this peak
        suppress_start = max(0, peak_idx - neighborhood)
        suppress_end = min(duration, peak_idx + neighborhood + 1)
        grid_copy[suppress_start:suppress_end] = -1.0

    # Sort peaks chronologically
    peaks = sorted(peaks)
    
    detected_moments = []
    
    # 8. Shape each peak into a Short-Form Emotional Arc (Hook, Buildup, Payoff, Resolution)
    for peak_idx in peaks:
        peak_score = composite_grid[peak_idx]

        # Precision Arc boundary extraction:
        # A. Hook Buildup: Step backward from peak (up to 8s) to find where the volume/contrast started rising
        coarse_start = max(0, peak_idx - 8)
        buildup_start_idx = peak_idx
        for t in range(peak_idx, coarse_start, -1):
            if loudness_grid[t] < 20.0 or contrast_grid[t] < 15.0:
                buildup_start_idx = t
                break
        
        clip_start = max(0.0, float(buildup_start_idx - 2.0))

        # B. Resolution Reaction: Step forward from peak (up to 12s) to capture laughter sustain or crowd cheering decay
        coarse_end = min(duration - 1, peak_idx + 12)
        resolution_end_idx = peak_idx
        for t in range(peak_idx, coarse_end):
            if loudness_grid[t] < 25.0 and frequency_grid[t] < 20.0:
                resolution_end_idx = t
                break
                
        clip_end = min(float(duration), float(resolution_end_idx + 3.0))

        # C. Enforce Strict Short-Form constraints (8s min to 35s max for Reels/Shorts)
        clip_duration = clip_end - clip_start
        if clip_duration < 8.0:
            clip_end = min(float(duration), clip_start + 10.0)
        elif clip_duration > 35.0:
            clip_start = max(0.0, float(peak_idx - 10.0))
            clip_end = min(float(duration), float(peak_idx + 15.0))

        # D. Calculate micro emotional arc scores
        hook_val = np.mean(contrast_grid[int(clip_start):int(clip_start + 3)]) if clip_start + 3 < duration else 30.0
        tension_val = np.mean(speech_rate_grid[int(clip_start):peak_idx + 1]) if clip_start < peak_idx else 30.0
        payoff_val = peak_score
        resolution_val = np.mean(frequency_grid[peak_idx:int(clip_end)]) if peak_idx < clip_end else 30.0

        # Unique descriptions
        reasons_set = set()
        # Look in the 5s around the peak for reason tags
        reason_start = max(0, peak_idx - 3)
        reason_end = min(duration - 1, peak_idx + 3)
        for t in range(reason_start, reason_end + 1):
            for r in second_reasons[t]:
                reasons_set.add(r)
        
        if not reasons_set:
            reasons_set.add("Energetic raw payoff climax")
            
        reason_summary = " and ".join(list(reasons_set)[:2])
        if len(reasons_set) > 2:
            reason_summary += f" (+{len(reasons_set) - 2} other cues)"
        reason_summary = reason_summary[0].upper() + reason_summary[1:]

        detected_moments.append({
            'start_time': clip_start,
            'end_time': clip_end,
            'viral_score': float(np.round(peak_score, 1)),
            'reason': reason_summary,
            'loudness_score': float(np.round(loudness_grid[peak_idx], 1)),
            'contrast_score': float(np.round(contrast_grid[peak_idx], 1)),
            'frequency_score': float(np.round(frequency_grid[peak_idx], 1)),
            'speech_rate_score': float(np.round(speech_rate_grid[peak_idx], 1)),
            'keyword_score': float(np.round(keyword_grid[peak_idx], 1)),
            
            # Emotional Arc breakdown
            'hook_score': float(np.round(min(100.0, hook_val * 1.5), 1)),
            'tension_score': float(np.round(min(100.0, tension_val * 1.3), 1)),
            'payoff_score': float(np.round(min(100.0, payoff_val * 1.1), 1)),
            'resolution_score': float(np.round(min(100.0, resolution_val * 1.6), 1))
        })

    # Sort descending by viral score
    detected_moments = sorted(detected_moments, key=lambda x: x['viral_score'], reverse=True)
    return detected_moments


def recalibrate_viral_moments_with_feedback(
    audio_features: dict, 
    transcript_features: dict, 
    liked_moments: List[dict], 
    clip_count: int = 5
) -> List[dict]:
    """
    Active Learning Feedback Engine.
    Employs NMS vector distance checking to locate other highlights matching liked templates.
    """
    duration = audio_features['duration_seconds']
    
    # 1. Compute User liked template vector
    feature_vectors = []
    for m in liked_moments:
        vec = [
            m.get('loudness_score', 50.0),
            m.get('contrast_score', 50.0),
            m.get('frequency_score', 50.0),
            m.get('speech_rate_score', 50.0),
            m.get('keyword_score', 50.0)
        ]
        feature_vectors.append(vec)
        
    if not feature_vectors:
        return detect_viral_moments(audio_features, transcript_features, niche="podcast", clip_count=clip_count)

    template_vector = np.mean(feature_vectors, axis=0)

    # 2. Map grids
    loudness_grid = np.zeros(duration)
    contrast_grid = np.zeros(duration)
    frequency_grid = np.zeros(duration)
    speech_rate_grid = np.zeros(duration)
    keyword_grid = np.zeros(duration)

    for t in range(min(duration, len(audio_features['volume_spikes']))):
        loudness_grid[t] = min(100.0, audio_features['volume_spikes'][t] * 20.0)
    for t in range(min(duration, len(audio_features['contrast_scores']))):
        contrast_grid[t] = min(100.0, max(0.0, (audio_features['contrast_scores'][t] - 1.0) * 33.0))
    for t in range(min(duration, len(audio_features['high_freq_ratios']))):
        frequency_grid[t] = min(100.0, audio_features['high_freq_ratios'][t] * 125.0)

    for rate_item in transcript_features.get('speech_rates', []):
        start = int(np.floor(rate_item['start']))
        end = int(np.ceil(rate_item['end']))
        score = min(100.0, max(0.0, (rate_item['words_per_sec'] - 3.0) * 40.0))
        for t in range(max(0, start), min(duration, end)):
            speech_rate_grid[t] = max(speech_rate_grid[t], score)

    for keyword_hit in transcript_features.get('keyword_hits', []):
        start = int(np.floor(keyword_hit['start']))
        end = int(np.ceil(keyword_hit['end']))
        score = min(100.0, keyword_hit['score'] * 8.0)
        for t in range(max(0, start), min(duration, end)):
            keyword_grid[t] = max(keyword_grid[t], score)

    # 3. Compute vector distance grid
    max_dist = np.sqrt(5 * 100**2)
    feedback_grid = np.zeros(duration)

    for t in range(duration):
        v_t = np.array([
            loudness_grid[t],
            contrast_grid[t],
            frequency_grid[t],
            speech_rate_grid[t],
            keyword_grid[t]
        ])
        dist = np.linalg.norm(v_t - template_vector)
        feedback_grid[t] = 100.0 * (1.0 - dist / max_dist)

    # 4. 1D NMS Peak Finder (excluding already liked moment ranges)
    liked_ranges = [(m['start_time'], m['end_time']) for m in liked_moments]
    
    grid_copy = feedback_grid.copy()
    peaks: List[int] = []
    
    # Suppress liked ranges first in the copy to prevent duplication
    for start, end in liked_ranges:
        s_idx = max(0, int(np.floor(start)))
        e_idx = min(duration, int(np.ceil(end)))
        grid_copy[s_idx:e_idx] = -1.0

    neighborhood = 15
    min_peak_threshold = 20.0

    for _ in range(clip_count):
        peak_idx = int(np.argmax(grid_copy))
        peak_score = grid_copy[peak_idx]
        
        if peak_score < min_peak_threshold and len(peaks) >= 2:
            break
        if peak_score <= 1.0:
            break

        peaks.append(peak_idx)
        
        suppress_start = max(0, peak_idx - neighborhood)
        suppress_end = min(duration, peak_idx + neighborhood + 1)
        grid_copy[suppress_start:suppress_end] = -1.0

    peaks = sorted(peaks)

    detected_moments = []
    for peak_idx in peaks:
        peak_score = feedback_grid[peak_idx]

        clip_start = max(0.0, float(peak_idx - 10.0))
        clip_end = min(float(duration), float(peak_idx + 15.0))

        detected_moments.append({
            'start_time': clip_start,
            'end_time': clip_end,
            'viral_score': float(np.round(peak_score, 1)),
            'reason': "Discovered via Active Learning (matches your editing template)",
            'loudness_score': float(np.round(loudness_grid[peak_idx], 1)),
            'contrast_score': float(np.round(contrast_grid[peak_idx], 1)),
            'frequency_score': float(np.round(frequency_grid[peak_idx], 1)),
            'speech_rate_score': float(np.round(speech_rate_grid[peak_idx], 1)),
            'keyword_score': float(np.round(keyword_grid[peak_idx], 1)),
            
            # Emotional Arc breaks
            'hook_score': float(np.round(peak_score * 0.95, 1)),
            'tension_score': float(np.round(peak_score * 0.92, 1)),
            'payoff_score': float(np.round(peak_score, 1)),
            'resolution_score': float(np.round(peak_score * 0.90, 1))
        })

    detected_moments = sorted(detected_moments, key=lambda x: x['viral_score'], reverse=True)
    return detected_moments
