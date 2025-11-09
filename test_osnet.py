# (source: 187, 188, 189, 190, 200)
import torch
from torchvision import transforms
from PIL import Image
import time
# 'osnet' 라이브러리가 설치되어 있어야 합니다. (예: pip install osnet-pytorch)
# (source: 188)
from osnet import osnet_x1_0 

# 모델 로드
# 
model = osnet_x1_0(pretrained=True)

# 모델 양자화 (보고서의 'TensorRT 양자화' 예시)
# 참고: torch.quantization.quantize_dynamic은 CPU 양자화이며,
# TensorRT를 위해서는 다른 변환 과정(예: ONNX)이 필요할 수 있습니다.
model = torch.quantization.quantize_dynamic(model) 
model.eval() # 추론 모드 설정

# 성능 측정
# (테스트를 위해 'test.jpg' 파일이 필요합니다)
input_img = Image.open('test.jpg').resize((256, 128))
# 
transform = transforms.ToTensor()
# 
x = transform(input_img).unsqueeze(0)

# 추론 시간 측정
# 
start = time.time()
# 
with torch.no_grad():
    # 256차원 벡터 출력
    feature = model(x) 
# 
elapsed = time.time() - start

# 
print(f"추론 시간: {elapsed*1000:.2f} ms") # 목표: < 300ms
# 
print(f"특징 벡터: {feature.shape}") # (1, 256)