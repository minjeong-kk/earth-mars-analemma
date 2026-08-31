# Earth-Mars Analemma

지구와 화성의 **균시차(Equation of Time)**와 **태양 아날렘마(Solar Analemma)**를
Python으로 계산하고 시각화하는 코드입니다.

행성의 **공전 궤도 이심률(Eccentricity)**과 **자전축 경사(Obliquity)**가
균시차와 아날렘마에 미치는 영향을 각각 계산하고, 두 효과를 합친 결과를
시각화합니다.

---

## 프로젝트 개요

### 균시차 (Equation of Time)

균시차는 **평균 태양시(Mean Solar Time)**와
**실제 태양시(Apparent Solar Time)** 사이의 시간 차이입니다.

균시차가 발생하는 주요 원인은 다음 두 가지입니다.

- **이심률 효과 (Eccentricity Effect)**
  - 행성의 공전 궤도가 완전한 원이 아니기 때문에 발생
  - 공전 속도가 궤도 위치에 따라 달라지는 효과

- **황도경사 효과 (Obliquity Effect)**
  - 행성의 자전축이 공전면에 대해 기울어져 있기 때문에 발생
  - 태양의 겉보기 운동이 천구의 적도 방향과 일치하지 않는 효과

두 효과를 합산하여 전체 균시차를 계산합니다.

```text
Total Equation of Time
        =
Eccentricity Effect
        +
Obliquity Effect
태양 아날렘마 (Solar Analemma)

아날렘마는 같은 장소에서 같은 평균 태양시각에 일정 기간 동안 태양의 위치를
관측했을 때 나타나는 8자 형태의 경로입니다.

본 프로젝트에서는 다음 두 값을 이용하여 아날렘마를 계산합니다.

X축: 균시차 (Equation of Time)
Y축: 태양 고도 (Solar Altitude)

관측자의 위도에 따라 태양 고도가 달라지므로,
지구와 화성 모두 관측 위도 36°를 기준으로 계산합니다.

계산 방법
1. 공전 궤도

행성의 근일점을 기준으로 한 **진근점이각(True Anomaly)**을 사용합니다.

공전 시간은 다음 관계식을 적분하여 계산합니다.

$$ \frac{dt}{d\theta} = \frac{P}{2\pi} \frac{(1-e^2)^{3/2}} {(1+e\cos\theta)^2} $$

여기서:

P: 공전 주기
e: 공전 궤도 이심률
\theta: 진근점이각

계산된 공전 시간을 이용하여 이심률에 의한 균시차를 계산합니다.

2. 계절 기준 변환

진근점이각은 근일점 기준으로 정의되기 때문에,
계절 변화 및 태양 적위를 계산할 때는 이를
**춘분점 기준 태양 황경(Solar Longitude)**으로 변환합니다.

이를 통해 실제 지구의 계절적 위치와 태양 적위의 위상을 일치시킵니다.

3. 태양 적위

태양 황경과 행성의 자전축 경사(황도경사)를 이용하여
태양 적위를 계산합니다.

$$ \delta = \arcsin(\sin\varepsilon\sin\lambda) $$
\delta: 태양 적위
\varepsilon: 자전축 경사
\lambda: 태양 황경
4. 태양 고도

관측자의 위도와 태양 적위를 이용하여 태양 고도를 계산합니다.

$$ \sin h = \sin\phi\sin\delta+ \cos\phi\cos\delta\cos H $$
h: 태양 고도
\phi: 관측자 위도
\delta: 태양 적위
H: 태양 시간각
주요 파라미터
Earth (지구)
항목	값
공전 주기	365일
이심률	0.0167
자전축 경사	23.44°
관측 위도	36°
Mars (화성)
항목	값
공전 주기	668일
이심률	0.0935
자전축 경사	25.19°
관측 위도	36°
Earth (지구)
Equation of Time & Analemma
<img width="700" height="600" alt="Earth Equation of Time" src="https://github.com/user-attachments/assets/3af71df7-2971-4667-814a-5928b531a593" /> <img width="800" height="700" alt="Earth Analemma" src="https://github.com/user-attachments/assets/39747825-d86d-4f65-9a36-91b96c3f7bcd" />
Mars (화성)
Equation of Time & Analemma
<img width="640" height="480" alt="Mars Equation of Time" src="https://github.com/user-attachments/assets/33695a66-50c6-4095-80b3-2b3c821d12ef" /> <img width="800" height="700" alt="Mars Analemma" src="https://github.com/user-attachments/assets/9abee76f-2138-4426-a781-8788b20e28fd" />
관측 기준

지구 계산에서는 위도 36°의 관측자를 기준으로 태양 고도를 계산하여
실제 관측된 아날렘마 데이터와 비교할 수 있도록 구성했습니다.

계산 과정에서는 기존의 이심률 및 황도경사 기반 계산 구조를 유지하면서,
근일점 기준과 춘분점 기준의 각도 체계가 혼용되지 않도록 기준을 정리했습니다.

또한 임의의 위상 이동값 대신 실제 공전 시간축을 사용하여
계산 결과의 계절적 위상을 맞추도록 수정했습니다.

실행 환경
Python 3.x
NumPy
Matplotlib
라이브러리 설치
pip install numpy matplotlib
실행

지구:

python earth.py

화성:

python mars.py

각 프로그램은 다음 두 개의 그래프를 생성합니다.

Equation of Time
Solar Analemma