import matplotlib.pyplot as plt

def plot_variance(variances):
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(variances) + 1), variances, "o-", label="Дисперсія δ")
    plt.xlabel("Степінь полінома m")
    plt.ylabel("Дисперсія")
    plt.title("Залежність дисперсії від степеня")
    plt.grid(True)
    plt.legend()
    plt.savefig("variance_vs_m.png", dpi=300)
    plt.close()

def plot_approximation(x, y, y_approx, m):
    plt.figure(figsize=(12, 6))
    plt.scatter(x, y, color="red", label="Реальні дані")
    plt.plot(x, y_approx, "b-", linewidth=2, label=f"Поліном степеня {m}")
    plt.xlabel("Місяць")
    plt.ylabel("Температура (°C)")
    plt.title("Апроксимація та реальні дані")
    plt.legend()
    plt.grid(True)
    plt.savefig("approximation.png", dpi=300)
    plt.close()

def plot_error(x, error, m):
    plt.figure(figsize=(12, 6))
    plt.plot(x, error, "r-", linewidth=2, label="Похибка")
    plt.scatter(x, error, color="red", s=30)
    plt.axhline(0, color="gray", linestyle="--", linewidth=1.5)
    plt.xlabel("Місяць")
    plt.ylabel("Похибка (y - φ(x))")
    plt.title(f"Графік похибки апроксимації (m={m})")
    plt.grid(True)
    plt.legend()
    plt.savefig("error.png", dpi=300)
    plt.close()