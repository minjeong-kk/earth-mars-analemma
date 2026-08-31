import numpy as np
import matplotlib.pyplot as plt
import earth_draw_points

dtor = np.pi/180. #각도를 라디안으로 변환하기 위한 상수임
Porb = 365. #지구의 공전 주기
delt = 23.44*dtor #지구의 자전축 기울기(라디안)
latitude = 36.*dtor #관측자의 위도(라디안)

theta = np.linspace(0, 360, 360001)*dtor
dtheta = np.gradient(theta)

# theta is Earth's true anomaly measured from perihelion.  The Earth is at
# heliocentric longitude 102.9372 deg at perihelion, so the geocentric Sun is
# 180 deg opposite that direction.
perihelion_longitude = 102.9372*dtor
solar_longitude = theta + perihelion_longitude + np.pi

e = 0.0167
t0 = theta/np.max(theta)*Porb 

# numerical integration of dt/dtheta (trapezoidal rule)
dt_dtheta = Porb*pow(1.-e**2, 1.5)/(2*np.pi)/pow(1 + e*np.cos(theta),2.)
t2 = np.concatenate(([0.], np.cumsum(
    0.5*(dt_dtheta[1:] + dt_dtheta[:-1])*np.diff(theta)
)))
theta2 = np.interp(t0, t2, theta)
delay1 = -(theta2 - theta)*180/np.pi*1440/360.

dpdt = np.cos(delt)/(1. - pow(np.sin(delt)*np.sin(solar_longitude), 2)) ### ratio between projected (phi) and original sun angles (thetax)
### this ratio is the same for time: delay per mean solar time
orbtimedelay = dpdt - 1 ### projected-angle delay per radian of ecliptic longitude
diff = orbtimedelay/dtor/360.*1440 ### convert to spin minutes per radian

# lambda - right ascension at perihelion fixes the integration constant.  This
# makes delay2 the obliquity contribution in the same equinox reference as
# delay1, rather than an arbitrarily shifted curve.
sun_right_ascension = np.arctan2(
    np.cos(delt)*np.sin(solar_longitude), np.cos(solar_longitude)
)
obliquity_offset = np.arctan2(
    np.sin(solar_longitude[0] - sun_right_ascension[0]),
    np.cos(solar_longitude[0] - sun_right_ascension[0])
) / dtor*1440/360.
delay2 = obliquity_offset - np.concatenate(([0.], np.cumsum(
    0.5*(diff[1:] + diff[:-1])*np.diff(theta)
)))
delay2_shifted = np.interp(t0, t2, delay2)

total_delay = delay1 + delay2_shifted

### altitude
solar_longitude2 = theta2 + perihelion_longitude + np.pi
decl = np.arcsin(np.sin(delt)*np.sin(solar_longitude2)) / dtor

phi = latitude
delta = decl * dtor

# At local mean noon, the apparent-Sun hour angle is the Equation of Time
# converted at 1 degree per 4 minutes.  Positive H is afternoon.
H = total_delay*dtor/4.

# 태양 고도
alt = np.arcsin(
    np.sin(phi) * np.sin(delta)
    
    + np.cos(phi) * np.cos(delta) * np.cos(H)
) / dtor

# Numerical checks for the Earth model (days are measured from perihelion).
print(f"이심률 EoT 최소/최대 (분): {delay1.min():.3f}, {delay1.max():.3f}")
print(f"황도경사 EoT 최소/최대 (분): {delay2_shifted.min():.3f}, {delay2_shifted.max():.3f}")
print(f"합성 EoT 최소/최대 (분): {total_delay.min():.3f}, {total_delay.max():.3f}")
print(f"적위 최소/최대 (도): {decl.min():.3f}, {decl.max():.3f}")
print(f"위도 36도 평균 정오 고도 최소/최대 (도): {alt.min():.3f}, {alt.max():.3f}")
for day, label in [(0, '근일점 (1월 4일)'), (75, '3월 춘분'),
                   (168, '6월 하지'), (261, '9월 추분'),
                   (351, '12월 동지')]:
    index = np.argmin(np.abs(t0 - day))
    print(f"{label:26s} 일수={t0[index]:6.1f}: "
          f"EoT={total_delay[index]:7.3f}분, "
          f"적위={decl[index]:7.3f}도, 고도={alt[index]:7.3f}도")
#----------- plot
plt.figure(figsize=(7, 6))

earth_draw_points.add_eot_labels(t0, delay1, delay2_shifted, total_delay)

plt.plot(t0, delay1, label='Eccentricity Effect', color='red', linewidth=1, linestyle='--')
plt.plot(t0, delay2_shifted, label='Obliquity Effect', color='blue', linewidth=1, linestyle='--')
plt.plot(t0, total_delay, label='Total Equation of Time', color='black', linewidth=1.5)

plt.xlim(0, 365)
plt.ylim(-20, 20)
plt.xlabel('Days since Perihelion (days)')
plt.ylabel('Equation of Time (min)')
plt.title('Earth\'s Equation of Time')
plt.axhline(0, color='gray', linewidth=0.8)

plt.legend()
plt.grid(True)

#----------- plot  
plt.figure(figsize=(8, 7))

earth_draw_points.add_analemma_labels(delay1, delay2_shifted, total_delay, alt)
plt.plot(delay1, alt, color='red', linewidth=1, label='Eccentricity', linestyle='--')
plt.plot(delay2_shifted, alt, color='blue', linewidth=1, label='Obliquity', linestyle='--')
plt.plot(total_delay, alt, color='black', linewidth=1.5, label='Total Analemma')

plt.xlim(-20, 20)     # Equation of Time 범위 (분)
plt.ylim(25, 85)      # 태양 고도 범위 (도)
plt.xlabel('Equation of Time (min)')
plt.ylabel('Altitude (deg)')
plt.title('Earth\'s Analemma')

plt.legend()
plt.grid(True)
plt.show()
