import soundfile as sf
from .validator import validate_wav


# WAV 파일 하나를 검사하고 결과를 반환하는 함수
def process_file(file_path, folder_path, sample_rate, bit_depth):
    # filename = str(file_path.relative_to(folder_path))
    filename = file_path.name #파일 이름 가져오기


    # 검사 결과를 저장할 딕셔너리 초기화
    file_results = {
        "filename": filename,
        "path": str(file_path.relative_to(folder_path)),     # 내부에서 파일을 구분하기 위한 전체 경로
        "status": None,
        "errors": [],
        "Channels": "unknown",
        "Sample Rate": "unknown",
        "Bit Depth": "unknown",
        "Subtype": "unknown"
    }

    try:
        # validator에게 파일 검사를 요청
        # 반환받은 검사 결과와 실제 WAV 정보를 변수에 저장
        result, reason, channels, actual_sample_rate, actual_bit_depth, subtype = validate_wav(file_path, sample_rate, bit_depth)

        # 검사 과정에서 확인한 실제 파일 정보를 결과 딕셔너리에 저장
        file_results["Channels"] = channels
        file_results["Sample Rate"] = actual_sample_rate
        file_results["Bit Depth"] = actual_bit_depth
        file_results["Subtype"] = subtype

        # 검사 결과가 True라면 정상 파일
        if result:
            print(f"{filename} : PASSED")
            file_results["status"] = "PASSED"

        # 검사 결과가 False라면 규격 불일치 파일
        else:
            print(f"{filename} : FAILED")
            file_results["status"] = "FAILED"

            # 실패 이유를 결과 딕셔너리에 저장
            file_results["errors"] = reason

            # 실패 이유를 터미널에도 출력
            for fail in reason:
                print(f"  - {fail}")

    # 파일을 읽는 과정에서 발생한 예외 처리
    except (sf.LibsndfileError, OSError) as e:

        # 예외 내용을 포함한 메시지 생성
        error_message = f"파일 읽기 실패 : {filename} : ERROR - {e}"
        print(error_message)

        # 읽기 오류 상태와 오류 메시지 저장
        file_results["status"] = "ERROR"
        file_results["errors"] = [error_message]

    # 최종 검사 결과 딕셔너리를 반환
    return file_results

# 지정한 폴더와 하위 폴더의 WAV 파일을 모두 검사하는 함수
def scan_folder(folder_path, sample_rate, bit_depth):

    # 개별 파일의 검사 결과를 모을 리스트
    results = []

    # 지정한 폴더 내부를 하위 폴더까지 탐색
    for file_path in folder_path.rglob("*"):

        # WAV 파일이며 실제 파일인 경우에만 검사
        if file_path.suffix.lower() == ".wav" and file_path.is_file():

            # 개별 파일 검사 함수에 전달하고 반환값을 리스트에 추가
            results.append(process_file(file_path, folder_path, sample_rate, bit_depth))

    # 모든 파일의 검사 결과를 반환
    return results