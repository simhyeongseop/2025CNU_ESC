# 파일명: spatial_validator.py
# (source: 81-95)

# (가정) 도로망 그래프 G를 다루기 위한 라이브러리
# (예: networkx. 실제 구현 시 OpenStreetMap 데이터 로드 필요)
import networkx as nx

# (가정) 보고서 6페이지 [cite: 86]의 도로망 그래프 G
# 실제로는 OpenStreetMap에서 로드해야 함
G = nx.Graph()
G.add_edge("CCTV1", "IntersectionA", distance=100) # (미터)
G.add_edge("IntersectionA", "CCTV2", distance=150)
G.add_edge("CCTV1", "CCTV3", distance=500)

def get_shortest_path_distance(graph, loc1, loc2):
    """
    (source: 88)
    두 위치 간의 최단 경로 거리를 계산 (미터 단위)
    """
    try:
        path = nx.shortest_path(graph, source=loc1, target=loc2, weight='distance')
        distance = nx.path_weight(graph, path, weight='distance')
        return distance
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return float('inf')

def calculate_time_window(distance_meters):
    """
    (source: 89-91)
    예상 이동 시간 창(time_window)을 계산 (초 단위)
    - 보행 속도 5km/h (약 1.39 m/s) 기준
    """
    MAX_SPEED_MPS = 1.39 # (5km/h) [cite: 90]
    WIGGLE_FACTOR = 1.5  # 우회 고려 [cite: 91]
    
    if distance_meters == float('inf'):
        return 0, float('inf')

    time_min = distance_meters / MAX_SPEED_MPS # [cite: 90]
    time_max = time_min * WIGGLE_FACTOR       # [cite: 91]
    
    return time_min, time_max

def calculate_combined_confidence(c1, c2):
    """
    (source: 93-94)
    베이지안 누적 신뢰도 계산 (보고서 공식 P = 1 - (1-C1)(1-C2))
    """
    return 1 - (1 - c1) * (1 - c2) # [cite: 93, 94]

def verify_detection_pair(detection1, detection2, graph):
    """
    (source: 82-95)
    두 개의 탐지 이벤트를 시공간적으로 검증
    """
    # (source: 83)
    loc1, time1, conf1 = detection1['location'], detection1['time'], detection1['confidence']
    # (source: 84)
    loc2, time2, conf2 = detection2['location'], detection2['time'], detection2['confidence']
    
    # 1. 최단 경로 거리 계산 (source: 88)
    distance = get_shortest_path_distance(graph, loc1, loc2)
    
    # 2. 이동 시간 창 계산 (source: 89)
    time_min, time_max = calculate_time_window(distance)
    
    # 3. 검증 (source: 92)
    time_delta = abs(time2 - time1)
    
    if time_min <= time_delta <= time_max:
        # 시공간적으로 일관됨
        # (source: 93)
        combined_confidence = calculate_combined_confidence(conf1, conf2)
        # (source: 95)
        return True, combined_confidence
    else:
        # 시공간적으로 불일치 (예: 순간이동)
        return False, 0

# --- 테스트 코드 ---
if __name__ == "__main__":
    # (source: 83)
    det1 = {'location': 'CCTV1', 'time': 0, 'confidence': 0.68} 
    # (source: 84)
    det2 = {'location': 'CCTV2', 'time': 180, 'confidence': 0.65} # 3분(180초) 뒤
    
    dist_1_2 = get_shortest_path_distance(G, 'CCTV1', 'CCTV2') # 250m
    t_min, t_max = calculate_time_window(dist_1_2) # 약 180초 ~ 270초
    
    print(f"CCTV1-CCTV2 거리: {dist_1_2}m")
    print(f"예상 시간 창: {t_min:.2f}초 ~ {t_max:.2f}초")

    is_valid, new_confidence = verify_detection_pair(det1, det2, G)
    
    if is_valid:
        print(f"검증 성공: 누적 신뢰도 {new_confidence * 100:.2f}%") # [cite: 94] (89.8%)
    else:
        print("검증 실패: 시공간 불일치")