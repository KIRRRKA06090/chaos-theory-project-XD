import numpy as np

print("--- ЗАПУСК ПРОВЕРКИ КОДА (ОПЫТ 0) ---")

# ==========================================
# Проверка 1. Две станции (N = 2)
# ==========================================
def step_n2(theta, omega, K, dt):
    # Для двух станций связь - это просто разность фаз друг друга
    pull = K * np.sin(np.array([theta[1] - theta[0], theta[0] - theta[1]]))
    return theta + (omega + pull) * dt

print("\n1. Проверка двух станций:")
omega_2 = np.array([1.0, -1.0]) # Разные ритмы (разница 2.0)
dt = 0.05

# Слабая связь (K = 0.5, меньше разницы ритмов)
theta_slab = np.array([0.0, 0.0])
for _ in range(1000):
    theta_slab = step_n2(theta_slab, omega_2, K=0.5, dt=dt)
diff_slab = theta_slab[1] - theta_slab[0]
print(f"   Слабая связь (K=0.5): разность фаз = {diff_slab:.2f} (должна дрейфовать, не застывать)")

# Сильная связь (K = 5.0, больше разницы ритмов)
theta_strong = np.array([0.0, 0.0])
for _ in range(1000):
    theta_strong = step_n2(theta_strong, omega_2, K=5.0, dt=dt)
diff_strong = theta_strong[1] - theta_strong[0]
print(f"   Сильная связь (K=5.0): разность фаз = {diff_strong:.2f} (должна застыть)")

# ==========================================
# Проверка 2 и 3. Шаг и Seed (Воспроизводимость)
# ==========================================
N = 100
sigma = 1.0
K = 2.0

def run_simulation(dt, seed):
    rng = np.random.default_rng(seed=seed)
    omega = rng.normal(0, sigma, N)
    theta = rng.uniform(0, 2*np.pi, N)
    
    # Функция шага (как в твоем physics.ipynb)
    def step(th):
        pull = K * np.mean(np.sin(th[None, :] - th[:, None]), axis=1)
        return th + (omega + pull) * dt

    def order_param(th):
        return np.sqrt(np.mean(np.cos(th))**2 + np.mean(np.sin(th))**2)

    # Считаем 200 шагов по времени (первую половину можно отбросить)
    for _ in range(200):
        theta = step(theta)
        
    return order_param(theta)

print("\n2. Проверка шага по времени (dt):")
r_dt1 = run_simulation(dt=0.05, seed=42)
r_dt2 = run_simulation(dt=0.025, seed=42)
print(f"   r при шаге 0.05:  {r_dt1:.4f}")
print(f"   r при шаге 0.025: {r_dt2:.4f}")
print("   (Числа должны быть очень близки друг к другу)")

print("\n3. Проверка воспроизводимости (Seed):")
r_seed1 = run_simulation(dt=0.05, seed=42)
r_seed2 = run_simulation(dt=0.05, seed=42)
print(f"   Первый запуск с seed=42:  r = {r_seed1:.5f}")
print(f"   Второй запуск с seed=42:  r = {r_seed2:.5f}")
print("   (Числа должны совпасть до последней цифры!)")

print("\n--- ПРОВЕРКА ЗАВЕРШЕНА ---")