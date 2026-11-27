import csv
from pathlib import Path

# 중복파일 검사
# def print_report(results, name_paths):
#     duple = []

#     print(f"\nTotal Files : {len(results)}")
#     # 중복 파일 찾기 (파일 이름 기준)
#     # duple: (중복 경로, 원본 경로) 쌍

#     for name, paths in name_paths.items():
#         if len(paths) > 1:      # 같은 이름이 2개 이상인 경우만
#             duple.append(name)  # 중복 파일 이름 추가

#     passed = [item for item in results if item["status"] == "PASSED"]
#     failed = [item for item in results if item["status"] == "FAILED"]
#     error_files = [item for item in results if item["status"] == "ERROR"]

#     print(f"Passed : {len(passed)}")
#     print(f"Failed : {len(failed)}")
#     print(f"Error Files : {len(error_files)}")
#     print(f"Duplicated Files : {len(duple)}")

#     print("\n--- PASSED FILES ---")
#     for item in passed:
#         print(item["filename"])

#     print("\n--- FAILED FILES ---")
#     for item in failed:
#         print(item["filename"])

#     print("\n--- ERROR FILES ---")
#     for item in error_files:
#         print(item["filename"])

#     print("\n--- DUPLICATED FILES ---")
#     for name, paths in name_paths.items():
#         if len(paths) > 1:
#             print(f"\n파일 이름 : {name}")
#             print("--- LOCATION ---")
#             print(paths[0])
#             for path in paths[1:]:
#                 print(path)

def export_csv(results, name_paths, csv_path):

    # path를 Key로, 해당 파일의 검사 결과 딕셔너리를 Value로 구성
    # 상대 경로를 통해 각 파일의 검사 결과를 정확하게 찾아갈 수 있도록 재구성
    path_to_item = {item["path"]: item for item in results}
    
    # CSV 파일을 저장할 폴더가 없으면 생성
    # 상위 폴더까지 생성하고, 이미 폴더가 존재해도 오류 발생하지 않음
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    # 해당 경로에 CSV 파일이 이미 존재하는지 확인
    if csv_path.exists():

        # CSV가 이미 존재하면 예외를 발생시켜 작성 중단
        raise FileExistsError("CSV 파일이 존재합니다.")

    else :
        # 지정한 경로에 파일을 쓰기 모드로 열기
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as file:

            # 딕셔너리 형태의 검사 결과를 CSV 행으로 작성할 도구 생성
            # file : 앞에서 열어둔 CSV 파일
            # fieldnames : CSV 열 이름과 기록 순서 지정
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "filename",
                    "path",
                    "status", 
                    "errors", 
                    "Channels", 
                    "Sample Rate", 
                    "Bit Depth", 
                    "Subtype"
                ],
            )

            # fieldnames에 지정된 열 이름을 CSV 첫 번째 행에 기록
            writer.writeheader()

            # name_paths의 Key(파일 이름)를 정렬된 순서로 하나씩 가져옴
            for name in sorted(name_paths):

                # 현재 파일 이름에 해당하는 경로 목록을 가져옴
                paths = name_paths[name]

                # 경로 깊이순으로 정렬하고, 깊이가 같으면 경로 문자열순으로 정렬
                for path in sorted(paths, key=lambda p: (len(Path(p).parts), p)):

                    # 검사 결과 딕셔너리를 복사해서 CSV 작성용 데이터 생성
                    row = path_to_item[path].copy()

                    # errors 리스트의 메시지들을 쉼표로 연결해 하나의 문자열로 변환
                    row["errors"] = ", ".join(row["errors"])

                    # 변환된 딕셔너리를 CSV 한 행으로 기록
                    writer.writerow(row)

    # 저장된 CSV 파일의 경로 반환
    return csv_path