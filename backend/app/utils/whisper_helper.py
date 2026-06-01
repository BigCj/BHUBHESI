import re
import json
from pathlib import Path
from faster_whisper import WhisperModel
from backend.app.config import WHISPER_MODEL, WHISPER_DEVICE, TRANSCRIPTS_DIR

_whisper_model_instance = None

def get_whisper_model() -> WhisperModel:
    global _whisper_model_instance
    if _whisper_model_instance is None:
        compute_type = "float32" if WHISPER_DEVICE != "cuda" else "float16"
        _whisper_model_instance = WhisperModel(
            WHISPER_MODEL,
            device=WHISPER_DEVICE,
            compute_type=compute_type
        )
    return _whisper_model_instance

# Standard emotional / hype keyword rules
KEYWORD_RULES = [
    (r'\b(haha|hahaha|hehe|lmao|lol|rofl)\b', 8.0, "laughter", "Laughter detected"),
    (r'\[laughter\]|\[laughs\]|\(laughter\)|\(laughs\)', 9.0, "laughter", "Laughter segment detected"),
    (r'\b(crazy|insane|wild|unbelievable|impossible|huge|insanely)\b', 6.0, "excitement", "Excitement keyword"),
    (r'\b(omg|god|gosh|holy|wtf|what the)\b', 7.0, "excitement", "Shock expression"),
    (r'\b(no way|shut up|get out|let\'s go|lets go|yes|boom|nooo)\b', 8.0, "hype", "Hype reaction"),
    (r'\b(goal|score|touchdown|win|champion|epic)\b', 7.0, "sports", "Sports event keyword"),
]

# Advanced controversy & short-form curiosity hook rules
CONTROVERSY_RULES = [
    (r'\b(secret|secrets|conspiracy|exposed|scam|fraud|fake|lying|lied|dangerous|cover up)\b', 9.0, "Shock controversy statement"),
    (r'\b(never tell you|they hid|what they hid|what they don\'t want you to|exposed|nobody knows|insane secret)\b', 10.0, "Curiosity hook phrase"),
    (r'\b(trust me|shocking|scared|banned|scandal|hiding|conspiracy)\b', 8.0, "Emotional intrigue hook")
]

def transcribe_and_analyze_audio(audio_path: Path, job_id: str, progress_callback=None) -> dict:
    """
    Transcribes the audio file and performs advanced conversational and semantic analysis.
    """
    if progress_callback:
        progress_callback(48)

    model = get_whisper_model()

    if progress_callback:
        progress_callback(52)

    segments_generator, info = model.transcribe(
        str(audio_path),
        beam_size=5,
        word_timestamps=True
    )

    segments = []
    keyword_hits = []
    speech_rates = []
    full_text_list = []

    duration = info.duration
    
    for segment in segments_generator:
        seg_dict = {
            'id': len(segments),
            'start': float(segment.start),
            'end': float(segment.end),
            'text': segment.text.strip(),
            'words': [
                {
                    'word': w.word.strip(),
                    'start': float(w.start),
                    'end': float(w.end)
                } for w in (segment.words or [])
            ]
        }
        segments.append(seg_dict)
        full_text_list.append(segment.text.strip())

        if duration > 0 and progress_callback:
            progress_pct = int(55 + (segment.end / duration) * 25)
            progress_callback(min(progress_pct, 80))

        # 1. Analyze Speech Rate (words per second)
        duration_sec = segment.end - segment.start
        words_count = len(segment.words or [])
        if duration_sec > 0.5 and words_count > 0:
            words_per_sec = words_count / duration_sec
            speech_rates.append({
                'start': float(segment.start),
                'end': float(segment.end),
                'words_per_sec': float(words_per_sec)
            })

        # 2. Semantic Analysis (Hype & Controversy Keywords)
        text_lower = segment.text.lower()
        segment_score = 0.0
        reasons = []

        # Standard emotional / sports triggers
        for pattern, weight, label, desc in KEYWORD_RULES:
            matches = re.findall(pattern, text_lower)
            if matches:
                segment_score += weight * len(matches)
                reasons.append(desc)

        # Controversy and curiosity hooks
        for pattern, weight, desc in CONTROVERSY_RULES:
            matches = re.findall(pattern, text_lower)
            if matches:
                segment_score += weight * len(matches)
                reasons.append(desc)

        # 3. Yelling (ALL CAPS)
        clean_text = re.sub(r'[^\w\s]', '', segment.text)
        words = clean_text.split()
        if len(words) >= 2 and all(w.isupper() for w in words):
            segment_score += 8.0
            reasons.append("ALL-CAPS screaming")

        # 4. Exclamatory emotional emphasis
        exclamations = segment.text.count("!")
        if exclamations > 0:
            segment_score += 3.0 * min(exclamations, 3)
            reasons.append("Exclamatory emphasis")

        if segment_score > 0:
            keyword_hits.append({
                'start': float(segment.start),
                'end': float(segment.end),
                'score': float(segment_score),
                'reason': ", ".join(list(set(reasons)))
            })

    # 5. Advanced Conversation Overlap / Interruption Analyzer
    # A crucial indicator of podcast tension or heated debate
    for i in range(len(segments) - 1):
        segA = segments[i]
        segB = segments[i+1]
        
        # If segment B starts before segment A ends, there is talking over each other
        if segB['start'] < segA['end'] - 0.7:
            overlap_duration = segA['end'] - segB['start']
            overlap_mid = segB['start'] + (overlap_duration / 2.0)
            
            keyword_hits.append({
                'start': float(segB['start']),
                'end': float(min(segA['end'], segB['end'])),
                'score': float(15.0 * min(overlap_duration, 2.5)), # high weight for interruptions
                'reason': "Heated dialogue overlap (speakers talking over each other)"
            })

    transcript_data = {
        'language': info.language,
        'duration': duration,
        'full_text': " ".join(full_text_list),
        'segments': segments,
        'keyword_hits': keyword_hits,
        'speech_rates': speech_rates
    }

    # Save to cache
    json_path = TRANSCRIPTS_DIR / f"{job_id}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(transcript_data, f, ensure_ascii=False, indent=2)

    return transcript_data
