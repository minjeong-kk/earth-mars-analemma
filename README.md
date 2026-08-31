# Earth–Mars Analemma

지구와 화성의 **균시차(Equation of Time, EoT)** 및 **태양 아날렘마**를 계산하고 시각화하는 Python 프로젝트입니다. 같은 장소에서 같은 **평균 태양시 정오**에 본 태양의 위치를, 균시차와 고도로 나타냅니다.

<p align="center">
  <img width="430" alt="Earth Equation of Time" src="https://github.com/user-attachments/assets/3af71df7-2971-4667-814a-5928b531a593" />
  <img width="480" alt="Earth Analemma" src="https://github.com/user-attachments/assets/39747825-d86d-4f65-9a36-91b96c3f7bcd" />
</p>

## 구성

| 파일 | 설명 |
| --- | --- |
| `Earth_Analemma.py` | 지구의 균시차와 위도 36° 아날렘마 계산 |
| `Mars_Analemma.py` | 화성의 균시차와 위도 36° 아날렘마 계산 |
| `earth_draw_points.py` | 지구 그래프의 계절·근일점·원일점 라벨 |
| `mars_draw_points.py` | 화성 그래프의 계절·근일점·원일점 라벨 |

## 계산 모델

균시차는 다음 두 성분의 합입니다.

```text
전체 균시차 = 이심률 효과 + 황도경사 효과
```

### 1. 이심률 효과

근일점을 원점으로 하는 진근점이각 `theta`를 사용합니다. 공전 시간은 아래 식을 사다리꼴 적분하여 구합니다.

$$
\frac{dt}{d\theta} = \frac{P}{2\pi}
\frac{(1-e^2)^{3/2}}{(1+e\cos\theta)^2}
$$

여기서 `P`는 공전 주기이고 `e`는 이심률입니다. 실제 진근점이각과 평균적으로 균일하게 진행한다고 가정한 각도의 차이가 이심률 EoT 성분이 됩니다.

### 2. 계절 기준과 황도경사 효과

`theta`는 근일점 기준 각도이므로 계절·적위 계산에 직접 사용하지 않습니다. 대신 춘분점 기준의 지심 태양 황경 `solar_longitude`를 사용합니다.

```text
solar_longitude = theta + perihelion_longitude + 180°
```

`perihelion_longitude`는 행성의 근일점 헬리오센트릭 경도이며, `+180°`는 행성에서 본 태양이 행성 위치벡터의 반대편에 있기 때문입니다. 이 기준으로 황도경사 효과와 계절 위상을 같은 좌표계에서 계산합니다.

### 3. 적위와 태양 고도

태양 적위는 다음과 같습니다.

$$
\delta = \arcsin(\sin\varepsilon\sin\lambda)
$$

고도는 관측 위도 `phi = 36°`와 EoT에서 얻은 시간각을 이용해 계산합니다.

$$
\sin h = \sin\phi\sin\delta + \cos\phi\cos\delta\cos H
$$

고정된 평균 정오에서 시간각은 `H = EoT / 4` 도입니다. 즉, 그래프의 세로축은 위도 36°에서 실제 관측과 비교할 수 있는 태양 고도입니다.

## 사용한 파라미터

| 항목 | 지구 | 화성 |
| --- | ---: | ---: |
| 공전 주기 | 365일 | 668 sol |
| 이심률 | 0.0167 | 0.0935 |
| 자전축 경사 | 23.44° | 25.19° |
| 관측자 위도 | 36° | 36° |
| 근일점의 태양 황경 | 약 282.94° | 약 250.99° (`Ls`) |

## 실행

Python 3, NumPy, Matplotlib가 필요합니다.

```bash
pip install numpy matplotlib

python Earth_Analemma.py
python Mars_Analemma.py
```

각 스크립트는 다음을 출력하고 두 개의 그래프를 표시합니다.

1. 이심률·황도경사·합성 균시차
2. 위도 36°의 태양 아날렘마

## 수치 확인값

현재 파라미터에서 지구 계산은 다음 범위를 보입니다.

| 값 | 계산 범위 |
| --- | ---: |
| 합성 EoT | −14.246 ~ +16.419분 |
| 태양 적위 | −23.440° ~ +23.440° |
| 위도 36° 평균 정오 고도 | 30.559° ~ 77.435° |

이는 실제 지구의 균시차 약 ±16분, 적위 ±23.44°, 위도 36°의 정오 고도 범위와 부합합니다.

## 화성 결과

<p align="center">
  <img width="430" alt="Mars Equation of Time" src="https://github.com/user-attachments/assets/33695a66-50c6-4095-80b3-2b3c821d12ef" />
  <img width="480" alt="Mars Analemma" src="https://github.com/user-attachments/assets/9abee76f-2138-4426-a781-8788b20e28fd" />
</p>

화성은 이심률이 지구보다 크므로 이심률 EoT 성분과 아날렘마의 비대칭성이 훨씬 크게 나타납니다.
