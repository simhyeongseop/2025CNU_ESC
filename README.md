# 2025CNU_ESC
2025 CNU 창의SW/AI축전 주니어 창의작품경진대회 ESC 코드 정리


# 🏆 ESC: Edge of Securing the City

[cite_start]**팀 Eagle Eye (심형섭, 김종훈) [cite: 3] | [cite_start]2025 CNU 창의SW/AI축전 주니어 창의작품경진대회 [cite: 1]**

[cite_start]본 레포지토리는 'ESC (Edge of Securing the City)' 프로젝트의 아이디어 기획서[cite: 1]와 핵심 알고리즘의 개념 검증(Proof-of-Concept) 코드를 포함합니다.

---

## 🚨 1. 우리가 해결하려는 문제: "놓쳐버린 골든타임"

현재 한국의 실종 사건 대응 시스템은 심각한 '골든타임' 문제를 겪고 있습니다.

* [cite_start]**현황:** 연간 약 5만 건의 실종 신고가 접수되며, 이 중 52%가 아동, 31%가 치매 환자입니다[cite: 3].
* **골든타임:** 실종자 생존율은 1시간 내 발견 시 95% 이상이지만, 6시간이 지나면 50% 이하로 급감합니다[cite: 3].
* [cite_start]**문제:** 현행 시스템은 초동 대응(신고 접수 및 CCTV 수동 검색)에만 **평균 4~8시간이 소요**되어, 이미 골든타임을 놓친 상태에서 수색이 시작됩니다[cite: 3].

### 기존 2세대 (중앙 집중형 AI)의 한계

[cite_start]최근 시도되는 중앙 집중형 AI 솔루션(모든 CCTV 영상을 중앙 서버로 전송) 역시 근본적인 한계가 있습니다[cite: 5].

1.  [cite_start]**네트워크 병목:** 대전시(2,500대) 기준 약 250Gbps의 트래픽이 필요하며, 이는 도시망의 40%를 점유합니다[cite: 5].
2.  [cite_start]**실시간성 실패:** 영상 전송(1-3초) + AI 처리(2-5초) + 응답(1-2초) = **최소 5~10초의 지연**이 발생합니다[cite: 5].
3.  [cite_start]**프라이버시 침해:** 수백만 시민의 영상 원본이 중앙에 저장되어 유출 시 큰 재앙이 될 수 있습니다[cite: 5].
4.  [cite_start]**높은 비용:** 연간 50~100억 원의 막대한 운영비가 발생합니다[cite: 5].

---

## 💡 2. 우리의 솔루션: 3세대 분산 자율 협력망 "ESC"

[cite_start]저희는 '중앙 통제'에서 '엣지(CCTV)의 자율 협력'으로 패러다임을 전환하는 **3세대 분산 자율 협력형 시스템 "ESC"**를 제안합니다[cite: 5].

[cite_start]ESC는 무거운 영상 원본(시간당 2.5GB) 대신, AI가 현장에서 분석한 **초경량 특징 벡터(단 1KB)**만을 CCTV끼리 P2P로 교환합니다[cite: 10].

**핵심 목표:**
* **초기 발견 시간:** 4~8시간 → **30초~1분** (99% 단축) [cite: 5]
* [cite_start]**네트워크 효율:** 99.9% 개선 (중앙 영상 전송 대비) [cite: 11]
* [cite_start]**프라이버시:** 영상 원본을 중앙에 저장하지 않는 **Privacy by Design** 설계 [cite: 183]

---

## 🚀 3. 핵심 기술 (Core Technologies)

ESC는 3가지 핵심 기술로 구성됩니다.

### [cite_start]1. 엣지 자율 에이전트 (Edge Autonomous Agent) [cite: 5]
* [cite_start]**하드웨어:** 저전력 고성능 AI 칩 (NVIDIA Jetson Orin Nano) [cite: 5]
* **소프트웨어:** 실시간 인물 재식별 모델 (OSNet)을 탑재하여 영상 분석을 로컬(엣지)에서 즉시 수행 [cite: 5]

### 2. 분산 협업 네트워크 (Distributed Collaboration Network) [cite: 8]
* [cite_start]**프로토콜:** Gossip Protocol을 사용하여 1KB 특징 벡터를 이웃 CCTV로 전파 [cite: 9, 10]
* [cite_start]**성능:** 대전시 전역(2,500대)에 0.9초 이내로 수색 벡터 전파 완료 (6-Round 기준) [cite: 20, 21]
* **효율화:** Bloom Filter를 사용해 이미 확인한 벡터의 중복 전파를 방지 [cite: 53, 71]

### 3. GNN 기반 이동 경로 예측 [cite: 25]
* [cite_start]**모델:** STGN-IT (시공간 그래프 네트워크) [cite: 26]
* [cite_start]**기능:** CCTV 사각지대로 사라진 실종자의 다음 위치를 확률적으로 예측 [cite: 27]
* **데이터:** OpenStreetMap(도로망) + 합성 보행 데이터로 학습하여 법적 리스크(PIPA)를 원천 차단 [cite: 28, 29, 30]

---

## 📂 4. 레포지토리 구성 (Code)

본 레포지토리는 ESC의 핵심 아이디어를 검증하기 위한 Python 예시 코드를 포함합니다.

### `test_osnet.py`
* [cite_start]OSNet (Re-ID) 모델을 로드하고 양자화한 뒤 [cite: 192, 194][cite_start], 단일 이미지에 대한 추론 시간을 측정하여 Jetson Orin Nano 환경에서의 실행 가능성(목표: 300ms 이내)을 검증합니다[cite: 199, 208].
* 또한 Re-ID 모델이 256차원의 특징 벡터를 출력하는지 확인합니다[cite: 41, 209].

### `gossip_agent.py`
* [cite_start]Gossip Protocol을 구현한 `GossipAgent` 클래스의 기본 구조입니다[cite: 223].
* [cite_start]UDP 소켓 통신을 기반으로 [cite: 239, 245][cite_start], 이웃 노드(Peers)에게 특징 벡터를 전파(Propagate)하고 수신(Receive)합니다[cite: 229, 242].
* [cite_start]Bloom Filter를 사용하여 수신한 적 있는 벡터는 다시 전파하지 않도록 중복을 방지합니다[cite: 228, 252, 253].

---

## 🛠️ 5. 설치 및 실행 방법 (Installation)

1.  레포지토리 복제:
    ```bash
    git clone [본 레포지토리 주소]
    cd [폴더명]
    ```

2.  필요한 Python 라이브러리 설치:
    ```bash
    pip install torch torchvision Pillow osnet-pytorch bloom-filter2
    ```

3.  OSNet 성능 테스트 실행 (테스트용 이미지 `test.jpg` 필요):
    ```bash
    python test_osnet.py
    ```
    *(예상 출력)*
    ```
    추론 시간: XX.XX ms
    특징 벡터: torch.Size([1, 256])
    ```

4.  Gossip Agent 실행 (개념 코드):
    ```bash
    # (본 코드는 P2P 네트워크의 기본 로직을 보여주며,
    # (실제 실행을 위해서는 여러 터미널에서 포트와 이웃 IP를 설정하여 실행해야 함)
    python gossip_agent.py
    ```

## 👥 6. 팀원 (Team Eagle Eye)

* **심형섭:** (컴퓨터융합학부, 202002513) [cite: 3]
* [cite_start]**김종훈:** (컴퓨터융합학부, 202202571) [cite: 3]