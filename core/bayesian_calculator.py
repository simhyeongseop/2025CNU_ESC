# 파일명: bayesian_calculator.py
# (source: 174-178)

def calculate_cumulative_confidence(initial_idf1, num_detections):
    """
    (source: 174)
    베이지안 누적 확률 계산 (보고서 9페이지 공식)
    P(same | n_detections) = 1 - (1 - IDF1)^n
    """
    if not (0 <= initial_idf1 <= 1):
        raise ValueError("IDF1 값은 0과 1 사이여야 합니다.")
    if num_detections < 1:
        return 0
        
    p_false_positive_single = 1 - initial_idf1
    p_false_positive_cumulative = p_false_positive_single ** num_detections
    p_cumulative_confidence = 1 - p_false_positive_cumulative
    
    return p_cumulative_confidence

def print_confidence_table(idf1_list, max_detections=5):
    """
    (source: 176)
    보고서 9페이지의 누적 신뢰도 표를 출력
    """
    header = ["IDF1"] + [f"{i}회" for i in range(1, max_detections + 1)]
    print(f"{' | '.join(header)}")
    print("-" * (len(header) * 8))

    for idf1 in idf1_list:
        row = [f"{idf1*100:.0f}%"]
        for n in range(1, max_detections + 1):
            # (source: 174)
            confidence = calculate_cumulative_confidence(idf1, n)
            row.append(f"{confidence*100:.1f}%")
        print(f"{' | '.join(row)}")

# --- 테스트 코드 ---
if __name__ == "__main__":
    # (source: 176)
    idf1_scenarios = [0.55, 0.65, 0.75]
    print("=== 베이지안 누적 신뢰도 시뮬레이션 (보고서 9P) ===")
    print_confidence_table(idf1_scenarios)
    
    print("\n---")
    # (source: 176) (55% IDF1, 3회 누적 시 90.9%)
    idf1 = 0.55
    n = 3
    conf = calculate_cumulative_confidence(idf1, n)
    print(f"IDF1 {idf1*100}%일 때 {n}회 누적 신뢰도: {conf*100:.1f}%") # [cite: 176]