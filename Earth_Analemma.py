import numpy as np
import matplotlib.pyplot as plt
import earth_draw_points

dtor = np.pi/180. #각도를 라디안으로 변환하기 위한 상수임
Porb = 365. #지구의 공전 주기
delt = 23.44*dtor #지구의 자전축 기울기(라디안)
latitude = 36.*dtor #관측자의 위도(라디안)

theta = np.linspace(0, 360, 360001)*dtor 
dtheta = np.gradient(theta)

e = 0.0167
t0 = theta/np.max(theta)*Porb 

# numerical integration
t2 = np.cumsum(Porb*pow(1.-e**2, 1.5)/(2*np.pi)/pow(1 + e*np.cos(theta),2.)*dtheta)
theta2 = np.interp(t0, t2, theta)
delay1 = -(theta2 - theta)*180/np.pi*1440/360. 

tdiff = 76.

dtx = dtheta/dtor ### degree

dpdt = np.cos(delt)/(1. - pow(np.sin(delt)*np.sin(theta), 2)) ### ratio between projected (phi) and original sun angles (thetax)
### this ratio is the same for time: delay per mean solar time
orbtimedelay = (dpdt - 1)*dtx ### delay per step converted in units of orbital day
diff = orbtimedelay/360.*1440 ### convert spin minutes

delay2 = -np.cumsum(diff)

t0_double = np.concatenate([t0, t0 + Porb])
delay2_double = np.concatenate([delay2, delay2])

t0_new = t0_double - Porb + tdiff
delay2_shifted = np.interp(t0, t0_new, delay2_double)

total_delay = delay1 + delay2_shifted

### altitude
zang = np.arccos(np.sin(delt)*np.sin(theta)) ### from vernal equinox
zang_double = np.concatenate([zang, zang])
zang_shifted = np.interp(t0, t0_new, zang_double)

decl = 90. - zang_shifted/dtor ### degree
alt = 180. - latitude/dtor - zang_shifted/dtor

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
plt.show()

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