import soundfile as sf

# 허용할 채널 수
ALLOWED_CHANNELS = [1, 2]

# WAV Subtype을 우리가 사용할 Bit Depth 숫자로 변환하기 위한 매핑
BIT_DEPTH_MAP = {
    "PCM_16": 16,
    "PCM_24": 24,
    "PCM_32": 32,
    "FLOAT": 32,
    "DOUBLE": 64,
}

# WAV 파일의 규격을 검사하는 함수
def validate_wav(file_path, sample_rate, bit_depth):
    # WAV 파일의 실제 메타데이터 읽기
    info = sf.info(file_path)

    # 모든 검사 항목이 통과한다고 가정하고 시작
    is_valid = True

    # 검사 실패 이유를 저장할 리스트
    errors = []

    # WAV 파일에서 실제 정보 추출
    channels = info.channels
    actual_sample_rate = info.samplerate
    subtype = info.subtype

    # Subtype을 숫자 형태의 Bit Depth로 변환
    actual_bit_depth = BIT_DEPTH_MAP.get(subtype)

    # Sample Rate 검사
    if actual_sample_rate != sample_rate:
        is_valid = False
        errors.append("Sample Rate : Error")

    # Channels 검사
    if channels not in ALLOWED_CHANNELS:
        is_valid = False
        errors.append("Channels : Error")

    # 지원하지 않는 Subtype인지 검사
    if actual_bit_depth is None:
        is_valid = False
        errors.append("Unsupported Subtype")

    # 실제 Bit Depth와 설정한 Bit Depth 비교
    elif actual_bit_depth != bit_depth:
        is_valid = False
        errors.append("Bit Depth : Error")
    
    # 검사 결과와 실제 WAV 정보를 반환
    return is_valid, errors, channels, actual_sample_rate, actual_bit_depth, subtype