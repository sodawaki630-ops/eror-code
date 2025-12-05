"""
utility_1000_lines.py

ไฟล์ตัวอย่างที่ประกอบด้วยฟังก์ชัน utility จำนวนมาก (~1000 บรรทัด)
จุดประสงค์:
- ให้เป็นตัวอย่างโค้ดยาวเพื่อการฝึกอ่าน/rewrite/วิเคราะห์
- ปลอดภัย ไม่เรียกใช้ I/O อันตราย
- มี docstring และคอมเมนต์สั้น ๆ เพื่อช่วยให้เข้าใจ
- เป็น PEP8-friendly เบื้องต้น (indent 4, line length สั้น ๆ)

วิธีใช้:
- นำไฟล์นี้ไป import ในโปรเจกต์อื่นหรือเรียกฟังก์ชันโดยตรง
- ฟังก์ชันส่วนใหญ่เป็นตัวอย่างของการคำนวณพื้นฐาน / string utils / mock utilities
"""

# -----------------------------------------------------------
# Imports (มาตรฐาน)
# -----------------------------------------------------------
import math
import random
import statistics
import json
import time
from typing import List, Dict, Any, Optional, Tuple

# -----------------------------------------------------------
# Basic numeric utilities
# -----------------------------------------------------------


def add(a: float, b: float) -> float:
    """Return sum of a and b."""
    return a + b


def sub(a: float, b: float) -> float:
    """Return a minus b."""
    return a - b


def mul(a: float, b: float) -> float:
    """Return a * b."""
    return a * b


def safe_div(a: float, b: float) -> Optional[float]:
    """Divide a by b, return None if division by zero."""
    if b == 0:
        return None
    return a / b


def is_even(n: int) -> bool:
    """Return True if n is even."""
    return n % 2 == 0


def is_odd(n: int) -> bool:
    """Return True if n is odd."""
    return n % 2 != 0


def square(n: float) -> float:
    """Return n squared."""
    return n * n


def cube(n: float) -> float:
    """Return n cubed."""
    return n * n * n


def factorial_safe(n: int) -> Optional[int]:
    """Return factorial of n, None if n < 0 or too large."""
    if n < 0:
        return None
    if n > 1000:
        # avoid extremely large computation
        return None
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


def clamp(value: float, low: float, high: float) -> float:
    """Clamp value between low and high."""
    return max(low, min(high, value))


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b with t in [0,1]."""
    return a + (b - a) * t


def approximately_equal(a: float, b: float, tol: float = 1e-9) -> bool:
    """Check approximate equality with tolerance tol."""
    return abs(a - b) <= tol


def mean(values: List[float]) -> Optional[float]:
    """Return arithmetic mean or None if empty."""
    if not values:
        return None
    return float(sum(values)) / len(values)


def median(values: List[float]) -> Optional[float]:
    """Return median or None if empty."""
    if not values:
        return None
    return statistics.median(values)


def stdev(values: List[float]) -> Optional[float]:
    """Return sample standard deviation or None if insufficient data."""
    if len(values) < 2:
        return None
    return statistics.stdev(values)


# -----------------------------------------------------------
# Basic string utilities
# -----------------------------------------------------------


def to_upper(s: str) -> str:
    """Return uppercase string."""
    return s.upper()


def to_lower(s: str) -> str:
    """Return lowercase string."""
    return s.lower()


def title_case(s: str) -> str:
    """Return title-cased string."""
    return s.title()


def snake_to_camel(s: str) -> str:
    """Convert snake_case to camelCase."""
    parts = s.split("_")
    if not parts:
        return s
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def camel_to_snake(s: str) -> str:
    """Convert CamelCase or camelCase to snake_case."""
    out = []
    for ch in s:
        if ch.isupper():
            if out:
                out.append("_")
            out.append(ch.lower())
        else:
            out.append(ch)
    return "".join(out)


def safe_json_loads(s: str) -> Optional[Any]:
    """Try to parse JSON string, return None if invalid."""
    try:
        return json.loads(s)
    except Exception:
        return None


def safe_json_dumps(obj: Any) -> str:
    """Dump object to JSON string with compact formatting."""
    try:
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        return "{}"


def repeat_str(s: str, n: int) -> str:
    """Return s repeated n times (n >= 0)."""
    if n <= 0:
        return ""
    return s * n


def truncate(s: str, length: int, ellipsis: str = "...") -> str:
    """Truncate string to length, append ellipsis if truncated."""
    if length <= 0:
        return ""
    if len(s) <= length:
        return s
    if length <= len(ellipsis):
        return ellipsis[:length]
    return s[: length - len(ellipsis)] + ellipsis


# -----------------------------------------------------------
# Date/time / timing utilities
# -----------------------------------------------------------


def current_timestamp() -> float:
    """Return current time in seconds since epoch."""
    return time.time()


def formatted_time() -> str:
    """Return simple formatted current time."""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def elapsed_seconds(start: float, end: Optional[float] = None) -> float:
    """Return elapsed seconds between start and end. Use now if end None."""
    if end is None:
        end = time.time()
    return max(0.0, end - start)


# -----------------------------------------------------------
# Collection utilities
# -----------------------------------------------------------


def first_or_default(lst: List[Any], default: Any = None) -> Any:
    """Return first element or default."""
    if not lst:
        return default
    return lst[0]


def last_or_default(lst: List[Any], default: Any = None) -> Any:
    """Return last element or default."""
    if not lst:
        return default
    return lst[-1]


def chunk_list(lst: List[Any], size: int) -> List[List[Any]]:
    """Split list into chunks of given size."""
    if size <= 0:
        return []
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def unique_preserve_order(seq: List[Any]) -> List[Any]:
    """Return list of unique items preserving first occurrence order."""
    seen = set()
    out = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def flatten(list_of_lists: List[List[Any]]) -> List[Any]:
    """Flatten one level of nesting."""
    out = []
    for sub in list_of_lists:
        out.extend(sub)
    return out


# -----------------------------------------------------------
# Mock utility functions (bulk-generated)
# -----------------------------------------------------------
# Below are many small utility functions to reach ~1000 lines.
# Each function is concise and documented to remain usable.
# We generate 240 functions named util_fn_1 ... util_fn_240.
# -----------------------------------------------------------

def util_fn_1(n: int) -> int:
    """Return n + 1."""
    return n + 1

def util_fn_2(n: int) -> int:
    """Return n - 1."""
    return n - 1

def util_fn_3(n: int) -> int:
    """Return n * 2."""
    return n * 2

def util_fn_4(n: int) -> int:
    """Return n // 2 (integer division)."""
    return n // 2

def util_fn_5(n: int) -> int:
    """Return absolute value of n."""
    return abs(n)

def util_fn_6(n: int) -> bool:
    """Return True if n is positive."""
    return n > 0

def util_fn_7(n: int) -> bool:
    """Return True if n is non-negative."""
    return n >= 0

def util_fn_8(n: int) -> int:
    """Return n squared using pow."""
    return pow(n, 2)

def util_fn_9(n: int) -> int:
    """Return n cubed using pow."""
    return pow(n, 3)

def util_fn_10(n: int) -> int:
    """Return n modulo 10."""
    return n % 10

def util_fn_11(n: int) -> int:
    """Sum of digits of n (non-negative)."""
    return sum(int(d) for d in str(abs(n)))

def util_fn_12(n: int) -> bool:
    """Check if n is a single-digit number."""
    return -9 <= n <= 9

def util_fn_13(n: int) -> int:
    """Return number of digits in base 10."""
    return len(str(abs(n)))

def util_fn_14(n: int) -> int:
    """Return reversed digits of n (positive assumed)."""
    s = str(abs(n))
    return int(s[::-1]) if s else 0

def util_fn_15(n: int) -> bool:
    """Return True if n is palindrome number."""
    s = str(abs(n))
    return s == s[::-1]

def util_fn_16(s: str) -> str:
    """Return reversed string."""
    return s[::-1]

def util_fn_17(s: str) -> int:
    """Return number of vowels in string."""
    return sum(1 for ch in s.lower() if ch in "aeiou")

def util_fn_18(s: str) -> int:
    """Return number of consonants in string."""
    return sum(1 for ch in s.lower() if ch.isalpha() and ch not in "aeiou")

def util_fn_19(s: str) -> bool:
    """Return True if string is palindrome (alphanumeric)."""
    filtered = "".join(ch.lower() for ch in s if ch.isalnum())
    return filtered == filtered[::-1]

def util_fn_20(s: str) -> str:
    """Return string with whitespace collapsed."""
    return " ".join(s.split())

def util_fn_21(lst: List[int]) -> int:
    """Return max or 0 if empty."""
    return max(lst) if lst else 0

def util_fn_22(lst: List[int]) -> int:
    """Return min or 0 if empty."""
    return min(lst) if lst else 0

def util_fn_23(lst: List[int]) -> int:
    """Return sum of list elements."""
    return sum(lst)

def util_fn_24(lst: List[int]) -> float:
    """Return average of list or 0.0 if empty."""
    return float(sum(lst)) / len(lst) if lst else 0.0

def util_fn_25(lst: List[int]) -> List[int]:
    """Return sorted copy of list ascending."""
    return sorted(lst)

def util_fn_26(lst: List[int]) -> List[int]:
    """Return sorted copy of list descending."""
    return sorted(lst, reverse=True)

def util_fn_27(lst: List[int]) -> List[int]:
    """Return distinct elements sorted."""
    return sorted(set(lst))

def util_fn_28(n: int) -> List[int]:
    """Return list of first n natural numbers starting from 0."""
    if n <= 0:
        return []
    return list(range(n))

def util_fn_29(n: int) -> List[int]:
    """Return first n even numbers (0-based)."""
    return [2 * i for i in range(n)]

def util_fn_30(n: int) -> List[int]:
    """Return first n odd numbers starting from 1."""
    return [2 * i + 1 for i in range(n)]

def util_fn_31(n: int) -> int:
    """Return nth Fibonacci number (iterative)."""
    if n <= 0:
        return 0
    a, b = 0, 1
    for _ in range(1, n):
        a, b = b, a + b
    return b

def util_fn_32(n: int) -> List[int]:
    """Return Fibonacci sequence of length n."""
    if n <= 0:
        return []
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]

def util_fn_33(n: int) -> bool:
    """Return True if n is prime (basic check)."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r = int(math.sqrt(n))
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True

def util_fn_34(n: int) -> List[int]:
    """Return prime factors of n (basic)."""
    n0 = abs(n)
    factors = []
    d = 2
    while d * d <= n0:
        while n0 % d == 0:
            factors.append(d)
            n0 //= d
        d += 1 if d == 2 else 2
    if n0 > 1:
        factors.append(n0)
    return factors

def util_fn_35(n: int) -> int:
    """Return greatest common divisor of n and 100 (example)."""
    return math.gcd(n, 100)

def util_fn_36(a: int, b: int) -> int:
    """Return gcd of a and b."""
    return math.gcd(a, b)

def util_fn_37(a: int, b: int) -> int:
    """Return lcm of a and b (safe)."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def util_fn_38(s: str) -> int:
    """Count words separated by whitespace."""
    return len(s.split())

def util_fn_39(lst: List[Any]) -> Dict[Any, int]:
    """Return frequency map of list items."""
    freq = {}
    for x in lst:
        freq[x] = freq.get(x, 0) + 1
    return freq

def util_fn_40(n: int) -> float:
    """Return 1/n as float or math.inf for zero."""
    if n == 0:
        return math.inf
    return 1.0 / n

def util_fn_41(s: str, delim: str = ",") -> List[str]:
    """Split string by delimiter and strip parts."""
    return [part.strip() for part in s.split(delim) if part.strip()]

def util_fn_42(d: Dict[Any, Any]) -> List[Tuple[Any, Any]]:
    """Return list of items sorted by key."""
    return sorted(d.items(), key=lambda kv: kv[0])

def util_fn_43(d: Dict[Any, Any]) -> List[Tuple[Any, Any]]:
    """Return list of items sorted by value ascending."""
    return sorted(d.items(), key=lambda kv: kv[1])

def util_fn_44(n: int) -> int:
    """Return triangular number n*(n+1)//2."""
    return n * (n + 1) // 2

def util_fn_45(n: int) -> int:
    """Return sum of first n odd numbers (should be n^2)."""
    return n * n

def util_fn_46(a: float, b: float) -> float:
    """Return hypotenuse sqrt(a^2 + b^2)."""
    return math.hypot(a, b)

def util_fn_47(angle_deg: float) -> float:
    """Return sine of angle in degrees."""
    return math.sin(math.radians(angle_deg))

def util_fn_48(angle_deg: float) -> float:
    """Return cosine of angle in degrees."""
    return math.cos(math.radians(angle_deg))

def util_fn_49(x: float) -> float:
    """Return sigmoid of x."""
    return 1.0 / (1.0 + math.exp(-x))

def util_fn_50(x: float) -> float:
    """Return softplus approximation log(1+e^x)."""
    return math.log1p(math.exp(x))

def util_fn_51(lst: List[float]) -> float:
    """Return product of list or 1.0 for empty."""
    p = 1.0
    for v in lst:
        p *= v
    return p

def util_fn_52(n: int) -> int:
    """Return sum of even numbers <= n."""
    if n <= 0:
        return 0
    evens = [i for i in range(0, n + 1, 2)]
    return sum(evens)

def util_fn_53(n: int) -> int:
    """Return sum of odd numbers <= n."""
    if n <= 0:
        return 0
    odds = [i for i in range(1, n + 1, 2)]
    return sum(odds)

def util_fn_54(lst: List[int]) -> Optional[int]:
    """Return second largest number or None."""
    if len(lst) < 2:
        return None
    unique = sorted(set(lst), reverse=True)
    return unique[1] if len(unique) > 1 else None

def util_fn_55(s: str) -> str:
    """Return string with only digits."""
    return "".join(ch for ch in s if ch.isdigit())

def util_fn_56(s: str) -> str:
    """Return string with only letters."""
    return "".join(ch for ch in s if ch.isalpha())

def util_fn_57(lst: List[Any]) -> bool:
    """Return True if list is strictly increasing."""
    return all(x < y for x, y in zip(lst, lst[1:]))

def util_fn_58(lst: List[Any]) -> bool:
    """Return True if list is non-decreasing."""
    return all(x <= y for x, y in zip(lst, lst[1:]))

def util_fn_59(n: int) -> List[int]:
    """Return divisors of n."""
    n0 = abs(n)
    if n0 == 0:
        return []
    divs = []
    for i in range(1, int(math.sqrt(n0)) + 1):
        if n0 % i == 0:
            divs.append(i)
            if i != n0 // i:
                divs.append(n0 // i)
    return sorted(divs)

def util_fn_60(n: int) -> bool:
    """Check if n is perfect number (small check)."""
    if n <= 1:
        return False
    return sum(d for d in util_fn_59(n) if d != n) == n

def util_fn_61(s: str) -> bool:
    """Return True if string contains any digit."""
    return any(ch.isdigit() for ch in s)

def util_fn_62(s: str) -> bool:
    """Return True if string contains any uppercase letter."""
    return any(ch.isupper() for ch in s)

def util_fn_63(s: str) -> bool:
    """Return True if string contains any lowercase letter."""
    return any(ch.islower() for ch in s)

def util_fn_64(n: int) -> int:
    """Return popcount (number of ones in binary) of n."""
    return bin(n & 0xFFFFFFFFFFFFFFFF).count("1")

def util_fn_65(n: int) -> int:
    """Return highest set bit position (0-based), -1 if zero."""
    if n == 0:
        return -1
    return n.bit_length() - 1

def util_fn_66(s: str, sub: str) -> int:
    """Count non-overlapping occurrences of sub in s."""
    if not sub:
        return 0
    return s.count(sub)

def util_fn_67(lst: List[int]) -> List[int]:
    """Return running sum list."""
    out = []
    total = 0
    for v in lst:
        total += v
        out.append(total)
    return out

def util_fn_68(n: int) -> int:
    """Return number of trailing zeros in n! (Legendre)."""
    if n < 0:
        return 0
    count = 0
    i = 5
    while i <= n:
        count += n // i
        i *= 5
    return count

def util_fn_69(n: int) -> List[int]:
    """Return digits of n as list."""
    return [int(d) for d in str(abs(n))]

def util_fn_70(s: str) -> str:
    """Return string with characters sorted."""
    return "".join(sorted(s))

def util_fn_71(n: int) -> bool:
    """Return True if n is power of two."""
    return n > 0 and (n & (n - 1)) == 0

def util_fn_72(n: int) -> int:
    """Return next power of two >= n."""
    if n <= 1:
        return 1
    p = 1
    while p < n:
        p <<= 1
    return p

def util_fn_73(lst: List[int]) -> List[int]:
    """Return indices of local maxima (strict)."""
    indices = []
    for i in range(1, len(lst) - 1):
        if lst[i] > lst[i - 1] and lst[i] > lst[i + 1]:
            indices.append(i)
    return indices

def util_fn_74(lst: List[int]) -> List[int]:
    """Return indices of local minima (strict)."""
    indices = []
    for i in range(1, len(lst) - 1):
        if lst[i] < lst[i - 1] and lst[i] < lst[i + 1]:
            indices.append(i)
    return indices

def util_fn_75(n: int) -> int:
    """Return integer square root of n (floor)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    return int(math.isqrt(n))

def util_fn_76(s: str) -> str:
    """Return string with vowels removed."""
    return "".join(ch for ch in s if ch.lower() not in "aeiou")

def util_fn_77(n: int) -> List[int]:
    """Return primes up to n (sieve)."""
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(math.sqrt(n)) + 1):
        if sieve[i]:
            step = i
            for j in range(i * i, n + 1, step):
                sieve[j] = False
    return [i for i, ok in enumerate(sieve) if ok]

def util_fn_78(lst: List[str]) -> str:
    """Join list into comma-separated string."""
    return ",".join(lst)

def util_fn_79(lst: List[str]) -> str:
    """Join list into newline-separated string."""
    return "\n".join(lst)

def util_fn_80(s: str) -> Dict[str, int]:
    """Return char frequency map."""
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    return freq

def util_fn_81(n: int) -> float:
    """Return harmonic number H_n approximated for large n."""
    if n <= 0:
        return 0.0
    # approximate for large n, exact sum for small
    if n < 1000:
        return sum(1.0 / i for i in range(1, n + 1))
    return math.log(n) + 0.5772156649015328606 + 1.0 / (2.0 * n)

def util_fn_82(a: int, b: int) -> List[int]:
    """Return inclusive range from a to b regardless of order."""
    if a <= b:
        return list(range(a, b + 1))
    return list(range(a, b - 1, -1))

def util_fn_83(lst: List[int]) -> int:
    """Return index of max, -1 if empty."""
    if not lst:
        return -1
    return max(range(len(lst)), key=lambda i: lst[i])

def util_fn_84(lst: List[int]) -> int:
    """Return index of min, -1 if empty."""
    if not lst:
        return -1
    return min(range(len(lst)), key=lambda i: lst[i])

def util_fn_85(n: int) -> List[int]:
    """Return factors of n in descending order."""
    return sorted(util_fn_59(n), reverse=True)

def util_fn_86(s: str) -> str:
    """Return only unique characters preserving order."""
    seen = set()
    out = []
    for ch in s:
        if ch not in seen:
            seen.add(ch)
            out.append(ch)
    return "".join(out)

def util_fn_87(n: int) -> int:
    """Return number of set bits in binary representation (positive)."""
    return bin(n).count("1")

def util_fn_88(lst: List[int], k: int) -> List[int]:
    """Return rolling window sums of size k."""
    if k <= 0 or k > len(lst):
        return []
    out = []
    s = sum(lst[:k])
    out.append(s)
    for i in range(k, len(lst)):
        s += lst[i] - lst[i - k]
        out.append(s)
    return out

def util_fn_89(s: str) -> str:
    """Return base64-like safe encoding (very simple)."""
    # This is a toy reversible transform for demonstration
    return "".join(chr((ord(ch) + 3) % 256) for ch in s)

def util_fn_90(s: str) -> str:
    """Reverse of util_fn_89 transform."""
    return "".join(chr((ord(ch) - 3) % 256) for ch in s)

def util_fn_91(n: int) -> int:
    """Return sum of prime numbers <= n (naive)."""
    return sum(util_fn_77(n))

def util_fn_92(s: str) -> bool:
    """Return True if s contains only ASCII characters."""
    try:
        s.encode("ascii")
        return True
    except Exception:
        return False

def util_fn_93(n: int) -> List[int]:
    """Return digits of n squared."""
    return util_fn_69(n * n)

def util_fn_94(lst: List[int]) -> int:
    """Return mode of list (most frequent) or first item if tie or empty."""
    if not lst:
        return 0
    freq = util_fn_39(lst)
    max_k = max(freq.items(), key=lambda kv: (kv[1], -lst.index(kv[0])))
    return max_k[0]

def util_fn_95(s: str) -> str:
    """Return string with alternating case starting uppercase."""
    out = []
    up = True
    for ch in s:
        if ch.isalpha():
            out.append(ch.upper() if up else ch.lower())
            up = not up
        else:
            out.append(ch)
    return "".join(out)

def util_fn_96(n: int) -> List[int]:
    """Return list of n random integers between 0 and 100."""
    return [random.randint(0, 100) for _ in range(max(0, n))]

def util_fn_97(seed: int) -> List[int]:
    """Return deterministic pseudo-random sample for seed."""
    rnd = random.Random(seed)
    return [rnd.randint(0, 1000) for _ in range(10)]

def util_fn_98(n: int) -> int:
    """Return sum of first n factorials (small n only)."""
    if n < 0:
        return 0
    s = 0
    fact = 1
    for i in range(1, n + 1):
        fact *= i
        s += fact
    return s

def util_fn_99(s: str) -> bool:
    """Return True if s is valid JSON."""
    return safe_json_loads(s) is not None

def util_fn_100(obj: Any) -> str:
    """Return pretty JSON string with indentation 2."""
    try:
        return json.dumps(obj, ensure_ascii=False, indent=2)
    except Exception:
        return "{}"

def util_fn_101(n: int) -> int:
    """Return 2^n using bit shift (safe for moderate n)."""
    if n < 0:
        return 0
    return 1 << n

def util_fn_102(n: int) -> int:
    """Return sum of first n powers of two: 1 + 2 + ... + 2^(n-1)."""
    if n <= 0:
        return 0
    return (1 << n) - 1

def util_fn_103(s: str) -> Dict[str, int]:
    """Return map of word lengths keyed by word."""
    words = [w for w in s.split() if w]
    return {w: len(w) for w in words}

def util_fn_104(lst: List[int]) -> Tuple[int, int]:
    """Return (min, max) or (0,0) if empty."""
    if not lst:
        return 0, 0
    return min(lst), max(lst)

def util_fn_105(n: int) -> float:
    """Return 1 + 1/2 + ... + 1/n (harmonic) approximation safe."""
    if n <= 0:
        return 0.0
    return sum(1.0 / i for i in range(1, n + 1))

def util_fn_106(s: str) -> int:
    """Return length of longest word in string."""
    words = s.split()
    return max((len(w) for w in words), default=0)

def util_fn_107(lst: List[str]) -> List[str]:
    """Return list of unique strings case-insensitive (preserve first)."""
    seen = set()
    out = []
    for w in lst:
        lw = w.lower()
        if lw not in seen:
            seen.add(lw)
            out.append(w)
    return out

def util_fn_108(n: int) -> int:
    """Return sum of digits until single digit (digital root)."""
    x = abs(n)
    while x >= 10:
        x = sum(int(d) for d in str(x))
    return x

def util_fn_109(s: str) -> str:
    """Return every second character starting at 0."""
    return s[::2]

def util_fn_110(s: str) -> str:
    """Return every second character starting at 1."""
    return s[1::2]

def util_fn_111(lst: List[int]) -> bool:
    """Return True if list contains duplicates."""
    return len(set(lst)) != len(lst)

def util_fn_112(n: int) -> List[int]:
    """Return list of powers of three up to n items."""
    return [3 ** i for i in range(max(0, n))]

def util_fn_113(x: float) -> float:
    """Return square root of x or math.nan if negative."""
    if x < 0:
        return math.nan
    return math.sqrt(x)

def util_fn_114(s: str) -> str:
    """Return string with punctuation removed (basic)."""
    return "".join(ch for ch in s if ch.isalnum() or ch.isspace())

def util_fn_115(n: int) -> int:
    """Return number of set bits for absolute value of n."""
    return util_fn_64(n)

def util_fn_116(s: str) -> bool:
    """Return True if s looks like an integer string."""
    s2 = s.strip()
    if not s2:
        return False
    if s2[0] in "+-" and s2[1:].isdigit():
        return True
    return s2.isdigit()

def util_fn_117(lst: List[int]) -> List[int]:
    """Return list rotated left by one."""
    if not lst:
        return []
    return lst[1:] + [lst[0]]

def util_fn_118(lst: List[int]) -> List[int]:
    """Return list rotated right by one."""
    if not lst:
        return []
    return [lst[-1]] + lst[:-1]

def util_fn_119(s: str, n: int) -> str:
    """Return string repeated n times with separator '-'. """
    if n <= 0:
        return ""
    return "-".join([s] * n)

def util_fn_120(n: int) -> int:
    """Return sum of digits at even positions (0-indexed)."""
    return sum(int(d) for i, d in enumerate(str(abs(n))) if i % 2 == 0)

def util_fn_121(n: int) -> int:
    """Return sum of digits at odd positions (0-indexed)."""
    return sum(int(d) for i, d in enumerate(str(abs(n))) if i % 2 == 1)

def util_fn_122(lst: List[int]) -> List[int]:
    """Return prefix maxima list."""
    out = []
    cur = -10**18
    for v in lst:
        cur = max(cur, v)
        out.append(cur)
    return out

def util_fn_123(n: int) -> int:
    """Return count of prime numbers <= n (naive)."""
    return len(util_fn_77(n))

def util_fn_124(s: str) -> str:
    """Return string with characters shifted by +1 (toy cipher)."""
    return "".join(chr((ord(ch) + 1) % 256) for ch in s)

def util_fn_125(s: str) -> str:
    """Reverse transform of util_fn_124."""
    return "".join(chr((ord(ch) - 1) % 256) for ch in s)

def util_fn_126(n: int) -> str:
    """Return binary representation of n without '0b'."""
    return bin(n)[2:] if n >= 0 else "-" + bin(-n)[2:]

def util_fn_127(n: int) -> int:
    """Return integer parsed from binary string of n (if n provided as int bits)."""
    return int(str(n), 2) if isinstance(n, int) else 0

def util_fn_128(s: str) -> int:
    """Return integer parsed from hex string (with or without 0x)."""
    s2 = s.strip().lower()
    if s2.startswith("0x"):
        s2 = s2[2:]
    try:
        return int(s2, 16)
    except Exception:
        return 0

def util_fn_129(lst: List[int]) -> float:
    """Return median of list (approx)."""
    if not lst:
        return 0.0
    return statistics.median(lst)

def util_fn_130(n: int) -> int:
    """Return number of partitions of n into ones and twos (Fibonacci-ish)."""
    if n < 0:
        return 0
    if n == 0:
        return 1
    a, b = 1, 1
    for _ in range(1, n):
        a, b = b, a + b
    return b

def util_fn_131(s: str) -> bool:
    """Return True if string is all digits and length even."""
    s2 = s.strip()
    return s2.isdigit() and (len(s2) % 2 == 0)

def util_fn_132(lst: List[int]) -> int:
    """Return index of first negative number or -1."""
    for i, v in enumerate(lst):
        if v < 0:
            return i
    return -1

def util_fn_133(n: int) -> int:
    """Return number of permutations of n distinct (n!)."""
    return factorial_safe(n) or 0

def util_fn_134(s: str) -> str:
    """Return string with each word reversed but order preserved."""
    return " ".join(w[::-1] for w in s.split())

def util_fn_135(n: int) -> int:
    """Return sum of factorials of digits of n."""
    s = sum(factorial_safe(int(d)) or 0 for d in str(abs(n)))
    return s

def util_fn_136(n: int) -> bool:
    """Return True if n is Armstrong number (for small n)."""
    s = str(abs(n))
    power = len(s)
    return sum(int(d) ** power for d in s) == abs(n)

def util_fn_137(lst: List[int]) -> List[int]:
    """Return indices where value equals index."""
    return [i for i, v in enumerate(lst) if i == v]

def util_fn_138(n: int) -> int:
    """Return minimal steps to reduce n to 1 by specific operations (naive)."""
    # this is a toy BFS for small n
    if n <= 1:
        return 0
    from collections import deque

    q = deque([(n, 0)])
    seen = {n}
    while q:
        x, d = q.popleft()
        if x == 1:
            return d
        # possible ops: -1, divide by 2 if even
        if x % 2 == 0:
            nxt = x // 2
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt, d + 1))
        nxt = x - 1
        if nxt not in seen and nxt > 0:
            seen.add(nxt)
            q.append((nxt, d + 1))
    return -1

def util_fn_139(s: str) -> str:
    """Return string with characters in ASCII order grouped by type."""
    letters = sorted(ch for ch in s if ch.isalpha())
    digits = sorted(ch for ch in s if ch.isdigit())
    others = sorted(ch for ch in s if not (ch.isalpha() or ch.isdigit()))
    return "".join(letters + digits + others)

def util_fn_140(n: int) -> bool:
    """Return True if n is Fibonacci number (small check)."""
    # property: 5*n^2+4 or 5*n^2-4 is perfect square
    def is_square(x):
        r = int(math.isqrt(x))
        return r * r == x
    return is_square(5 * n * n + 4) or is_square(5 * n * n - 4)

def util_fn_141(lst: List[int]) -> List[int]:
    """Return list with elements squared."""
    return [x * x for x in lst]

def util_fn_142(lst: List[int]) -> List[int]:
    """Return list with elements cubed."""
    return [x * x * x for x in lst]

def util_fn_143(s: str) -> int:
    """Return index of first vowel or -1."""
    for i, ch in enumerate(s):
        if ch.lower() in "aeiou":
            return i
    return -1

def util_fn_144(s: str) -> str:
    """Return string with vowels doubled (toy)."""
    out = []
    for ch in s:
        if ch.lower() in "aeiou":
            out.append(ch * 2)
        else:
            out.append(ch)
    return "".join(out)

def util_fn_145(n: int) -> int:
    """Return sum of alternating digits (+ - + -)."""
    s = str(abs(n))
    total = 0
    sign = 1
    for ch in s:
        total += sign * int(ch)
        sign *= -1
    return total

def util_fn_146(n: int) -> int:
    """Return product of digits of n."""
    prod = 1
    for d in str(abs(n)):
        prod *= int(d)
    return prod

def util_fn_147(lst: List[int]) -> bool:
    """Return True if list is permutation of 0..n-1 for some n."""
    if not lst:
        return True
    n = len(lst)
    return set(lst) == set(range(n))

def util_fn_148(s: str) -> str:
    """Return first half of string (floor)."""
    mid = len(s) // 2
    return s[:mid]

def util_fn_149(s: str) -> str:
    """Return second half of string."""
    mid = len(s) // 2
    return s[mid:]

def util_fn_150(n: int) -> int:
    """Return number of 1 bits in Gray code of n."""
    gray = n ^ (n >> 1)
    return bin(gray).count("1")

def util_fn_151(lst: List[int]) -> int:
    """Return sum of even-indexed elements (0-based)."""
    return sum(v for i, v in enumerate(lst) if i % 2 == 0)

def util_fn_152(lst: List[int]) -> int:
    """Return sum of odd-indexed elements (0-based)."""
    return sum(v for i, v in enumerate(lst) if i % 2 == 1)

def util_fn_153(n: int) -> List[int]:
    """Return list of indices of set bits of n."""
    out = []
    i = 0
    x = n
    while x:
        if x & 1:
            out.append(i)
        x >>= 1
        i += 1
    return out

def util_fn_154(s: str) -> bool:
    """Return True if s contains repeated substring pattern (simple)."""
    if not s:
        return False
    ss = (s + s)[1:-1]
    return s in ss

def util_fn_155(n: int) -> int:
    """Return integer partition count into ones (always 1)."""
    return 1 if n >= 0 else 0

def util_fn_156(lst: List[int]) -> int:
    """Return length of longest increasing contiguous subarray."""
    if not lst:
        return 0
    best = cur = 1
    for i in range(1, len(lst)):
        if lst[i] > lst[i - 1]:
            cur += 1
        else:
            best = max(best, cur)
            cur = 1
    return max(best, cur)

def util_fn_157(n: int) -> bool:
    """Return True if n is automorphic (last digits of n^2 equal n)."""
    sq = n * n
    return str(sq).endswith(str(n))

def util_fn_158(s: str) -> List[str]:
    """Return list of all prefixes of s."""
    return [s[:i] for i in range(len(s) + 1)]

def util_fn_159(s: str) -> List[str]:
    """Return list of all suffixes of s."""
    return [s[i:] for i in range(len(s))]

def util_fn_160(n: int) -> int:
    """Return next odd number >= n."""
    return n if n % 2 == 1 else n + 1

def util_fn_161(lst: List[int]) -> Tuple[int, int]:
    """Return pair (sum even positions, sum odd positions)."""
    even = sum(v for i, v in enumerate(lst) if i % 2 == 0)
    odd = sum(v for i, v in enumerate(lst) if i % 2 == 1)
    return even, odd

def util_fn_162(s: str) -> bool:
    """Return True if parentheses are balanced (simple)."""
    stack = []
    pairs = {"(": ")", "[": "]", "{": "}"}
    for ch in s:
        if ch in pairs:
            stack.append(ch)
        elif ch in pairs.values():
            if not stack:
                return False
            top = stack.pop()
            if pairs[top] != ch:
                return False
    return not stack

def util_fn_163(n: int) -> int:
    """Return sum of digits factorials of n (toy)."""
    return sum(factorial_safe(int(d)) or 0 for d in str(abs(n)))

def util_fn_164(lst: List[int]) -> int:
    """Return number of inversions (naive)."""
    inv = 0
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] > lst[j]:
                inv += 1
    return inv

def util_fn_165(s: str) -> str:
    """Return run-length encoding of string."""
    if not s:
        return ""
    out = []
    cur = s[0]
    cnt = 1
    for ch in s[1:]:
        if ch == cur:
            cnt += 1
        else:
            out.append(f"{cur}{cnt}")
            cur = ch
            cnt = 1
    out.append(f"{cur}{cnt}")
    return "".join(out)

def util_fn_166(s: str) -> str:
    """Decode naive run-length encoding from util_fn_165."""
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        i += 1
        num = ""
        while i < len(s) and s[i].isdigit():
            num += s[i]
            i += 1
        count = int(num) if num else 1
        out.append(ch * count)
    return "".join(out)

def util_fn_167(n: int) -> List[int]:
    """Return aliquot sequence starting at n until 0 or repeat (naive)."""
    def sum_proper_divisors(x):
        return sum(d for d in util_fn_59(x) if d != x)
    seen = set()
    out = []
    x = n
    while x and x not in seen:
        seen.add(x)
        out.append(x)
        x = sum_proper_divisors(x)
    return out

def util_fn_168(s: str) -> str:
    """Return every word capitalized but leave others."""
    return " ".join(w.capitalize() for w in s.split())

def util_fn_169(n: int) -> int:
    """Return number of derangements (subfactorial) approximate for small n."""
    if n < 0:
        return 0
    if n == 0:
        return 1
    der = 1
    for k in range(1, n + 1):
        der = k * der + (-1) ** k
    return der

def util_fn_170(lst: List[int]) -> List[int]:
    """Return elements that are greater than average."""
    if not lst:
        return []
    avg = sum(lst) / len(lst)
    return [x for x in lst if x > avg]

def util_fn_171(n: int) -> int:
    """Return n-th Catalan number (naive, may overflow)."""
    if n < 0:
        return 0
    # Use direct formula for small n
    num = math.comb(2 * n, n)
    den = n + 1
    return num // den

def util_fn_172(s: str) -> str:
    """Return string with words reversed order."""
    return " ".join(s.split()[::-1])

def util_fn_173(lst: List[int]) -> bool:
    """Return True if list is a palindrome."""
    return lst == lst[::-1]

def util_fn_174(s: str) -> bool:
    """Return True if s has all unique characters."""
    return len(set(s)) == len(s)

def util_fn_175(n: int) -> int:
    """Return count of prime numbers with given number of digits (naive)."""
    if n <= 0:
        return 0
    low = 10 ** (n - 1)
    high = 10**n - 1
    return len([p for p in util_fn_77(high) if p >= low])

def util_fn_176(s: str) -> str:
    """Return string with alternating words reversed."""
    words = s.split()
    out = []
    for i, w in enumerate(words):
        out.append(w[::-1] if i % 2 == 1 else w)
    return " ".join(out)

def util_fn_177(n: int) -> int:
    """Return integer obtained by repeating n twice in decimal (e.g., 12 -> 1212)."""
    s = str(n)
    return int(s + s)

def util_fn_178(lst: List[int]) -> int:
    """Return index of pivot where sum left == sum right or -1."""
    total = sum(lst)
    left = 0
    for i, v in enumerate(lst):
        if left == total - left - v:
            return i
        left += v
    return -1

def util_fn_179(s: str) -> int:
    """Return longest run of identical characters length."""
    if not s:
        return 0
    best = cur = 1
    for a, b in zip(s, s[1:]):
        if a == b:
            cur += 1
            best = max(best, cur)
        else:
            cur = 1
    return best

def util_fn_180(n: int) -> int:
    """Return smallest prime >= n (naive)."""
    if n <= 2:
        return 2
    x = max(2, n)
    while True:
        if util_fn_33(x):
            return x
        x += 1

def util_fn_181(s: str) -> str:
    """Return string with letters rotated by 13 (ROT13)."""
    def rot13_char(ch):
        if "a" <= ch <= "z":
            return chr((ord(ch) - ord("a") + 13) % 26 + ord("a"))
        if "A" <= ch <= "Z":
            return chr((ord(ch) - ord("A") + 13) % 26 + ord("A"))
        return ch
    return "".join(rot13_char(ch) for ch in s)

def util_fn_182(lst: List[int]) -> List[int]:
    """Return zigzag reorder: first, last, second, second-last, ..."""
    out = []
    i, j = 0, len(lst) - 1
    while i <= j:
        out.append(lst[i])
        if i != j:
            out.append(lst[j])
        i += 1
        j -= 1
    return out

def util_fn_183(n: int) -> int:
    """Return sum of first n odd squares (1^2 + 3^2 + ...)."""
    total = 0
    for k in range(n):
        odd = 2 * k + 1
        total += odd * odd
    return total

def util_fn_184(s: str) -> str:
    """Return only characters with ASCII code < 128."""
    return "".join(ch for ch in s if ord(ch) < 128)

def util_fn_185(lst: List[int]) -> int:
    """Return product of nonzero elements or 0 if any zero."""
    prod = 1
    for v in lst:
        if v == 0:
            return 0
        prod *= v
    return prod

def util_fn_186(n: int) -> int:
    """Return sum of proper divisors of n."""
    return sum(d for d in util_fn_59(n) if d != n)

def util_fn_187(s: str) -> str:
    """Return string after removing duplicate adjacent characters."""
    if not s:
        return ""
    out = [s[0]]
    for ch in s[1:]:
        if ch != out[-1]:
            out.append(ch)
    return "".join(out)

def util_fn_188(lst: List[int]) -> List[int]:
    """Return sorted indices by corresponding values ascending."""
    return sorted(range(len(lst)), key=lambda i: lst[i])

def util_fn_189(n: int) -> int:
    """Return 2-adic valuation (exponent of 2 in factorization)."""
    if n == 0:
        return 0
    v = 0
    while n % 2 == 0:
        n //= 2
        v += 1
    return v

def util_fn_190(s: str) -> int:
    """Return Levenshtein distance to empty string (length)."""
    return len(s)

def util_fn_191(lst: List[int]) -> List[int]:
    """Return prefix minima list."""
    out = []
    cur = 10**18
    for v in lst:
        cur = min(cur, v)
        out.append(cur)
    return out

def util_fn_192(n: int) -> int:
    """Return number of combinations C(n,2) safely."""
    if n < 2:
        return 0
    return n * (n - 1) // 2

def util_fn_193(s: str) -> bool:
    """Return True if string s contains balanced quotes (single and double)."""
    return s.count("'") % 2 == 0 and s.count('"') % 2 == 0

def util_fn_194(lst: List[int]) -> int:
    """Return sum of elements at prime indices."""
    primes = set(util_fn_77(len(lst)))
    return sum(v for i, v in enumerate(lst) if i in primes)

def util_fn_195(n: int) -> List[int]:
    """Return sequence of n triangular numbers."""
    return [i * (i + 1) // 2 for i in range(n)]

def util_fn_196(s: str) -> str:
    """Return slugify-like string: lowercase, non-alnum to hyphen."""
    s2 = s.lower()
    out = []
    for ch in s2:
        if ch.isalnum():
            out.append(ch)
        else:
            if out and out[-1] != "-":
                out.append("-")
    return "".join(out).strip("-")

def util_fn_197(n: int) -> List[int]:
    """Return list of Euler totient phi(k) for k=1..n (naive)."""
    if n <= 0:
        return []
    res = []
    for k in range(1, n + 1):
        cnt = sum(1 for i in range(1, k + 1) if math.gcd(i, k) == 1)
        res.append(cnt)
    return res

def util_fn_198(lst: List[int]) -> List[int]:
    """Return list of differences between successive elements."""
    return [b - a for a, b in zip(lst, lst[1:])]

def util_fn_199(s: str) -> str:
    """Return string trimmed to first sentence (by period)."""
    if "." in s:
        return s.split(".", 1)[0].strip() + "."
    return s.strip()

def util_fn_200(n: int) -> int:
    """Return number of set bits in Gray code of n (alias)."""
    return util_fn_150(n)

def util_fn_201(lst: List[int], k: int) -> List[int]:
    """Return top-k largest unique elements sorted descending."""
    return sorted(set(lst), reverse=True)[: max(0, k)]

def util_fn_202(s: str) -> str:
    """Return string with characters randomly shuffled deterministically."""
    lst = list(s)
    rnd = random.Random(len(s))
    rnd.shuffle(lst)
    return "".join(lst)

def util_fn_203(n: int) -> List[int]:
    """Return sequence of n numbers: alternating +1,-1 starting with +1."""
    return [1 if i % 2 == 0 else -1 for i in range(n)]

def util_fn_204(lst: List[int]) -> List[int]:
    """Return list with duplicates removed keeping last occurrence."""
    seen = set()
    out = []
    for x in reversed(lst):
        if x not in seen:
            seen.add(x)
            out.append(x)
    return list(reversed(out))

def util_fn_205(s: str) -> str:
    """Return characters at prime positions (0-based)."""
    primes = set(util_fn_77(len(s)))
    return "".join(ch for i, ch in enumerate(s) if i in primes)

def util_fn_206(n: int) -> int:
    """Return sum of proper divisors excluding the number itself."""
    return util_fn_186(n)

def util_fn_207(lst: List[int]) -> bool:
    """Return True if any two numbers sum to zero (naive)."""
    s = set(lst)
    for x in s:
        if -x in s:
            return True
    return False

def util_fn_208(s: str) -> str:
    """Return title-like slug: capitalize words and join with space."""
    return " ".join(w.capitalize() for w in s.split())

def util_fn_209(n: int) -> int:
    """Return collatz steps count for n until 1 (naive)."""
    if n <= 0:
        return 0
    cnt = 0
    x = n
    while x != 1 and cnt < 10000:
        if x % 2 == 0:
            x //= 2
        else:
            x = 3 * x + 1
        cnt += 1
    return cnt

def util_fn_210(lst: List[int], v: int) -> int:
    """Return count of occurrences of v in list."""
    return lst.count(v)

def util_fn_211(s: str) -> str:
    """Return string with every vowel replaced by '*'."""
    return "".join("*" if ch.lower() in "aeiou" else ch for ch in s)

def util_fn_212(n: int) -> int:
    """Return nth triangular number (alias)."""
    return util_fn_44(n)

def util_fn_213(lst: List[int]) -> int:
    """Return GCD of list (reduce)."""
    if not lst:
        return 0
    g = abs(lst[0])
    for v in lst[1:]:
        g = math.gcd(g, abs(v))
    return g

def util_fn_214(n: int) -> int:
    """Return number composed of n repeated digits '1' (e.g., n=3 -> 111)."""
    if n <= 0:
        return 0
    return int("1" * n)

def util_fn_215(s: str) -> str:
    """Return string with all letters shifted to next alphabet letter cyclically."""
    out = []
    for ch in s:
        if "a" <= ch <= "y":
            out.append(chr(ord(ch) + 1))
        elif ch == "z":
            out.append("a")
        elif "A" <= ch <= "Y":
            out.append(chr(ord(ch) + 1))
        elif ch == "Z":
            out.append("A")
        else:
            out.append(ch)
    return "".join(out)

def util_fn_216(n: int) -> List[int]:
    """Return list of lengths of Collatz sequences for numbers 1..n (naive)."""
    return [util_fn_209(i) for i in range(1, max(1, n) + 1)]

def util_fn_217(lst: List[int]) -> int:
    """Return number of peaks in list (value greater than neighbors)."""
    return len(util_fn_73(lst))

def util_fn_218(s: str) -> str:
    """Return string with whitespace trimmed and single spaced."""
    return " ".join(s.split())

def util_fn_219(n: int) -> int:
    """Return floor of base-10 log of n."""
    if n <= 0:
        return -math.inf  # indicate invalid
    return int(math.log10(n))

def util_fn_220(lst: List[int]) -> List[int]:
    """Return sorted unique elements preserving original order (stable)."""
    seen = set()
    out = []
    for x in lst:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

def util_fn_221(s: str) -> bool:
    """Return True if parentheses '()' pairs are balanced."""
    cnt = 0
    for ch in s:
        if ch == "(":
            cnt += 1
        elif ch == ")":
            cnt -= 1
            if cnt < 0:
                return False
    return cnt == 0

def util_fn_222(n: int) -> int:
    """Return sum of digits in base 2 (popcount)."""
    return util_fn_87(n)

def util_fn_223(lst: List[int]) -> Tuple[int, int]:
    """Return (index_of_max, index_of_min)."""
    if not lst:
        return -1, -1
    return util_fn_83(lst), util_fn_84(lst)

def util_fn_224(s: str, a: str, b: str) -> str:
    """Replace substring a with b in s (all occurrences)."""
    return s.replace(a, b)

def util_fn_225(n: int) -> List[int]:
    """Return n Lucas numbers (L0=2, L1=1)."""
    if n <= 0:
        return []
    if n == 1:
        return [2]
    seq = [2, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]

def util_fn_226(lst: List[int]) -> List[int]:
    """Return list of lengths of runs of equal values."""
    if not lst:
        return []
    out = []
    cur = lst[0]
    cnt = 1
    for v in lst[1:]:
        if v == cur:
            cnt += 1
        else:
            out.append(cnt)
            cur = v
            cnt = 1
    out.append(cnt)
    return out

def util_fn_227(s: str) -> int:
    """Return count of uppercase transitions (lower->upper)."""
    cnt = 0
    for a, b in zip(s, s[1:]):
        if a.islower() and b.isupper():
            cnt += 1
    return cnt

def util_fn_228(n: int) -> int:
    """Return multiplicative persistence (number of times multiply digits until single digit)."""
    if n < 0:
        return 0
    steps = 0
    x = abs(n)
    while x >= 10:
        prod = 1
        for d in str(x):
            prod *= int(d)
        x = prod
        steps += 1
        if steps > 1000:
            break
    return steps

def util_fn_229(lst: List[int]) -> List[int]:
    """Return cumulative product list."""
    out = []
    p = 1
    for v in lst:
        p *= v
        out.append(p)
    return out

def util_fn_230(s: str) -> str:
    """Return string after removing vowels and reversing."""
    return util_fn_16(util_fn_76(s))

def util_fn_231(n: int) -> int:
    """Return sum of squares of first n natural numbers."""
    return n * (n + 1) * (2 * n + 1) // 6

def util_fn_232(lst: List[int]) -> List[int]:
    """Return list interleaving two halves: first1, last1, second1, secondlast1..."""
    if not lst:
        return []
    mid = len(lst) // 2
    a = lst[:mid]
    b = lst[mid:]
    out = []
    for i in range(max(len(a), len(b))):
        if i < len(a):
            out.append(a[i])
        if i < len(b):
            out.append(b[i])
    return out

def util_fn_233(n: int) -> int:
    """Return sum of all numbers <= n that are multiples of 3 or 5 (Project Euler 1)."""
    return sum(i for i in range(1, n + 1) if i % 3 == 0 or i % 5 == 0)

def util_fn_234(s: str) -> str:
    """Return Pig Latin style transform for each word (basic)."""
    words = []
    for w in s.split():
        if w:
            words.append(w[1:] + w[0] + "ay" if len(w) > 1 else w + "ay")
    return " ".join(words)

def util_fn_235(lst: List[int]) -> List[int]:
    """Return list with elements replaced by rank (dense ranking)."""
    uniq = sorted(set(lst))
    rank = {v: i + 1 for i, v in enumerate(uniq)}
    return [rank[v] for v in lst]

def util_fn_236(n: int) -> int:
    """Return count of trailing zeros in n in base 2 (same as v2)."""
    return util_fn_189(n)

def util_fn_237(s: str) -> str:
    """Return every character duplicated (aa bb cc)."""
    return "".join(ch * 2 for ch in s)

def util_fn_238(lst: List[int]) -> int:
    """Return alternating sum: a0 - a1 + a2 - a3 ..."""
    total = 0
    sign = 1
    for v in lst:
        total += sign * v
        sign *= -1
    return total

def util_fn_239(n: int) -> List[int]:
    """Return digits of n in reverse order as ints."""
    return [int(d) for d in str(abs(n))[::-1]]

def util_fn_240(s: str) -> str:
    """Return safe filename by replacing unsafe chars with underscore."""
    return "".join(ch if ch.isalnum() or ch in ("-", "_", ".") else "_" for ch in s)

# -----------------------------------------------------------
# End of generated utilities
# -----------------------------------------------------------

# Small example main to show usage (won't run on import)
if __name__ == "__main__":
    # quick tests
    print("Sum 2+3 =", add(2, 3))
    print("Is 17 prime? ->", util_fn_33(17))
    print("First 10 primes:", util_fn_77(30)[:10])
    print("Reverse 'hello' ->", util_fn_16("hello"))
    print("Safe JSON loads of '{\"a\":1}' ->", safe_json_loads('{"a":1}'))
