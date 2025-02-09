import binascii
import random
import time
import hashlib
import matplotlib.pyplot as plt

class HashTable:
    def __init__(self, size, probing, hash_func='default', c1=1, c2=1, c3=1):
        self.size = size
        self.table = [None] * size
        self.probing = probing
        self.c1, self.c2, self.c3 = c1, c2, c3
        self.hash_func = hash_func

    def _hash(self, key):
        """
        Внутренняя хеш-функция.
        Поддерживает разные типы хеш-функций.
        """
        if self.hash_func == 'md5':
            return int(hashlib.md5(str(key).encode()).hexdigest(), 16) % self.size
        elif self.hash_func == 'sha1':
            return int(hashlib.sha1(str(key).encode()).hexdigest(), 16) % self.size
        elif self.hash_func == 'crc32':
            return binascii.crc32(str(key).encode()) % self.size
        else:
            return key % self.size  # Простая хеш-функция по умолчанию

    def hash(self, key, i):
        """
        Вычисляет индекс с учётом пробирования.
        """
        if self.probing == 'linear':
            return (self._hash(key) + i) % self.size
        elif self.probing == 'quadratic':
            return (self._hash(key) + self.c1 * i + self.c2 * i**2) % self.size
        elif self.probing == 'cubic':
            return (self._hash(key) + self.c1 * i + self.c2 * i**2 + self.c3 * i**3) % self.size
        else:
            raise ValueError("Неизвестный тип пробирования")

    def insert(self, key):
        """
        Вставляет ключ в таблицу и возвращает количество коллизий.
        """
        i = 0
        while True:
            index = self.hash(key, i)
            if self.table[index] is None:
                self.table[index] = key
                return i  # Возвращаем количество попыток (коллизий)
            i += 1
            if i >= self.size:
                raise Exception("Таблица заполнена")

def simulate(probing, size, num_keys, hash_func='default'):
    """
    Симуляция вставки ключей в хеш-таблицу.
    Возвращает общее количество коллизий и время выполнения.
    """
    collisions = 0
    ht = HashTable(size, probing, hash_func)
    start_time = time.time()

    for _ in range(num_keys):
        key = random.randint(0, 10**6)  # Случайные ключи
        collisions += ht.insert(key)

    execution_time = time.time() - start_time
    return collisions, execution_time

def run_experiment(size, load_factor, n_runs, hash_func='default'):
    """
    Запуск эксперимента для всех типов пробирования.
    Возвращает среднее количество коллизий и время выполнения для каждого метода.
    """
    num_keys = int(size * load_factor)  # Количество ключей на основе коэффициента заполнения
    results = {
        'linear': {'collisions': [], 'time': []},
        'quadratic': {'collisions': [], 'time': []},
        'cubic': {'collisions': [], 'time': []},
    }

    for _ in range(n_runs):
        # Линейное пробирование
        col, t = simulate('linear', size, num_keys, hash_func)
        results['linear']['collisions'].append(col)
        results['linear']['time'].append(t)

        # Квадратичное пробирование
        col, t = simulate('quadratic', size, num_keys, hash_func)
        results['quadratic']['collisions'].append(col)
        results['quadratic']['time'].append(t)

        # Кубическое пробирование
        col, t = simulate('cubic', size, num_keys, hash_func)
        results['cubic']['collisions'].append(col)
        results['cubic']['time'].append(t)

    # Вычисляем средние значения
    avg_results = {
        'linear': {
            'collisions': sum(results['linear']['collisions']) / n_runs,
            'time': sum(results['linear']['time']) / n_runs,
        },
        'quadratic': {
            'collisions': sum(results['quadratic']['collisions']) / n_runs,
            'time': sum(results['quadratic']['time']) / n_runs,
        },
        'cubic': {
            'collisions': sum(results['cubic']['collisions']) / n_runs,
            'time': sum(results['cubic']['time']) / n_runs,
        },
    }
    return avg_results

def plot_results(avg_results):
    """
    Визуализация результатов эксперимента.
    """
    methods = list(avg_results.keys())
    collisions = [avg_results[m]['collisions'] for m in methods]
    times = [avg_results[m]['time'] for m in methods]

    # График коллизий
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.bar(methods, collisions, color=['blue', 'green', 'red'])
    plt.xlabel('Метод пробирования')
    plt.ylabel('Среднее количество коллизий')
    plt.title('Сравнение коллизий')

    # График времени выполнения
    plt.subplot(1, 2, 2)
    plt.bar(methods, times, color=['blue', 'green', 'red'])
    plt.xlabel('Метод пробирования')
    plt.ylabel('Среднее время выполнения (сек)')
    plt.title('Сравнение времени выполнения')

    plt.tight_layout()
    plt.show()

# Параметры эксперимента
size = 10000  # Размер хеш-таблицы
load_factor = 0.8  # Коэффициент заполнения (80%)
n_runs = 20  # Количество запусков эксперимента
hash_func = 'md5'  # Тип хеш-функции (default, md5, sha1, crc32)

# Запуск эксперимента
avg_results = run_experiment(size, load_factor, n_runs, hash_func)

# Вывод результатов
print("===================================================")
print("Результаты:")
for method, data in avg_results.items():
    print(f"{method.capitalize()} пробирование:")
    print(f"  Среднее количество коллизий: {data['collisions']:.2f}")
    print(f"  Среднее время выполнения: {data['time']:.4f} сек")
print("===================================================")

# Визуализация результатов
plot_results(avg_results)