# 파일명: gossip_agent.py
# (source: 220, 221, 200, 222)
import socket
import json
import time
from bloom_filter2 import BloomFilter # (source: 222)

# Gossip Protocol 기본 구조 예시 코드
# 
class GossipAgent:
    # 
    def __init__(self, peer_id, neighbors):
        # 
        self.peer_id = peer_id
        # 
        self.neighbors = neighbors # 이웃 5개 CCTV IP 주소
        # 
        # (capacity와 error_rate는 을 따름)
        self.seen = BloomFilter(capacity=10000, error_rate=0.001)

    # 
    def propagate_vector(self, feature_vector):
        """Gossip Protocol으로 벡터 전파"""
        
        # 
        # 참고: 원본 보고서의 은 여기서 self.seen.add()를 실행합니다.
        # 하지만 에서 'not in self.seen'을 확인하면 논리적 모순이 발생합니다.
        # 의 수신부 로직(수신 후 add -> 전파)을 따르는 것이 합리적입니다.
        #
        # 여기서는 보고서 의 코드를 *주석 처리*하고 의 의도를 살립니다.
        # self.seen.add(str(feature_vector)) # (논리적 모순 가능성)
        
        # 
        for neighbor in self.neighbors:
            # 
            # (만약 을 활성화했다면, 이 if문은 항상 False가 됩니다)
            if str(feature_vector) not in self.seen:
                # 
                message = {
                    'type': 'FEATURE_VECTOR',       # 
                    'vector': feature_vector,       # (tolist()는 수신측에서 이미 list로 옴)
                    'timestamp': time.time()      # 
                } # 
                
                try:
                    # 
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    # (포트 5000은 에서 가져옴)
                    sock.sendto(json.dumps(message).encode(), (neighbor, 5000))
                    # 
                    sock.close()
                except Exception as e:
                    print(f"Send Error to {neighbor}: {e}")

    # 
    def receive_vector(self):
        # 
        """다른 에이전트로부터 벡터 수신"""
        # 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 
        sock.bind(('0.0.0.0', 5000))
        print(f"Gossip Agent (ID: {self.peer_id}) listening on port 5000...")
        
        # 
        while True:
            try:
                # (버퍼 크기 1024 예시)
                data, addr = sock.recvfrom(1024) 
                # 
                msg = json.loads(data.decode())
                
                # 에서 .tolist()로 전송된 벡터는 list 타입
                vector_str = str(msg['vector'])

                # 
                if vector_str not in self.seen:
                    # 
                    self.seen.add(vector_str)
                    print(f"Received new vector from {addr}")

                    # # 다시 다른 이웃들에게 전파
                    self.propagate_vector(msg['vector'])
            except Exception as e:
                print(f"Receive Error: {e}")

# --- 테스트용 코드 ---
# 이 파일을 직접 실행할 경우, 간단한 P2P 네트워크 테스트
if __name__ == '__main__':
    import threading

    # 3개의 에이전트가 로컬에서 서로 통신하는 것을 시뮬레이션
    # Agent 1 (Port 5000) -> 5001, 5002
    # Agent 2 (Port 5001) -> 5000, 5002
    # Agent 3 (Port 5002) -> 5000, 5001
    
    # 이 테스트 코드는 보고서에 없으나, 위 클래스의 동작을 검증하기 위함입니다.
    # 실제 IP 주소와 포트 매핑이 필요합니다.
    # 본 예시 코드는 단일 머신에서 포트로 구분하는 예시입니다.
    # (참고: 위 코드는 모든 에이전트가 5000번 포트에 바인딩되려 하므로
    # 실제 테스트 시에는 포트를 분리해야 합니다.)

    print("Gossip Agent 로직입니다.")
    print("실제 P2P 테스트를 위해서는 각 에이전트를 별도 프로세스/스레드에서")
    print("서로 다른 수신 포트(예: 5001, 5002, 5003)로 실행해야 합니다.")