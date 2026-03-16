from data_reader import read_data
from normal_equations import form_matrix, form_vector
from gauss_solver import gauss_solve
from polynomial_evaluator import eval_polynomial, compute_variance
from visualizer import plot_variance, plot_approximation, plot_error

def main():
    x, y = read_data("data.csv")
    print("формула дисперсії")
    print("δ = √[ Σ(φ(x_i) - f_i)² / (n+1) ]\n")

    # обчислення для m=1..10
    variances = []  #похибки для кожного степеня
    for m in range(1, 11): #від прямої лінії 1-10
        A = form_matrix(x, m) # передаємо х та степінь полінома
        b = form_vector(x, y, m) # передаємо х, у та степінь полінома
        coef = gauss_solve(A, b) #передаємо матрицю та вектор
        y_approx = [eval_polynomial(xi, coef) for xi in x] #маємо коефіцієнти. проганяємо через поліном, отримуємо список температур
        delta = compute_variance(y, y_approx) #порівняння реальних темпратур
        variances.append(delta)
        print(f"m = {m:2d} → δ = {delta:.6f}")

    optimal_m = variances.index(min(variances)) + 1
    print(f"\n оптимальний степінь m з мін дисперсією = {optimal_m} ")

    # фінальний поліном
    A = form_matrix(x, optimal_m)
    b = form_vector(x, y, optimal_m)
    coef = gauss_solve(A, b)
    y_approx = [eval_polynomial(xi, coef) for xi in x]

    # Графіки
    plot_variance(variances)
    plot_approximation(x, y, y_approx, optimal_m)

    # Таблиця похибки + графік
    error = [y[i] - y_approx[i] for i in range(len(x))]
    print("\nТаблиця похибки апроксимації (оптимальний m):")
    for i in range(len(x)):
        print(f"Місяць {int(x[i]):2d}:  y={y[i]:5.1f}  approx={y_approx[i]:6.2f}  error={error[i]:7.4f}")

    plot_error(x, error, optimal_m)

    # прогноз
    print("\n" + "=" * 40)
    print("ПРОГНОЗ ТЕМПЕРАТУРИ (місяці 25-27)")
    print("=" * 40)

    x_future = [25, 26, 27]

    y_future_overfit = [eval_polynomial(xi, coef) for xi in x_future]
    print(f"\n Прогноз за поліном степеня m={optimal_m}:")
    print("поліноми високих степенів погано екстраполюють періодичні дані.")
    for month, temp in zip(x_future, y_future_overfit):
        print(f"Місяць {month}: {temp:6.2f} °C  ")

    A_trend = form_matrix(x, 1)
    b_trend = form_vector(x, y, 1)
    coef_trend = gauss_solve(A_trend, b_trend)
    y_future_trend = [eval_polynomial(xi, coef_trend) for xi in x_future]

    print(f"\n[+]  прогноз , m=1:")
    print("показує середню очікувану температуру без стрибків")
    for month, temp in zip(x_future, y_future_trend):
        print(f"Місяць {month}: {temp:6.2f} °C  ")

    print("\nвсі графіки збережено!")
if __name__ == "__main__":
    main()