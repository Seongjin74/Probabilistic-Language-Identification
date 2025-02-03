# Probabilistic Language Identification / 확률적 언어 식별

## English & 한국어 Version

## 1. Introduction / 소개

This project implements a **Bayesian probabilistic language identification system** that determines whether a given text is written in **English or Spanish** using **Bayesian Inference**.

이 프로젝트는 **베이즈 추론(Bayesian Inference)**을 활용하여 주어진 텍스트가 **영어인지 스페인어인지** 확률적으로 판별하는 시스템입니다.

The input consists of a text file along with two prior probability values. The text file contains printable ASCII characters, and the system processes it to compute the **frequency of each letter (A-Z) while ignoring case and non-alphabetic characters**. The prior probability values indicate the likelihood of the text being in English or Spanish before analyzing its content. 

입력 데이터는 텍스트 파일과 두 개의 사전 확률 값으로 구성됩니다. 텍스트 파일은 ASCII 문자로 이루어져 있으며, 시스템은 이를 처리하여 **A-Z까지 각 문자 빈도를 계산하며, 대소문자를 무시하고 비알파벳 문자는 제외**합니다. 

### 1.1 Prior Probability / 사전 확률
The **prior probability** \(P(Y = y)\) represents the likelihood of the text belonging to language \(y\) before analyzing its contents. These probabilities are user-defined inputs:

사전 확률 \(P(Y = y)\)은 텍스트가 특정 언어일 가능성을 분석하기 전에 주어지는 값으로, 사용자 입력을 통해 설정됩니다.

- \(P(Y = 	ext{English})\) : The prior probability of the text being English.
- \(P(Y = 	ext{Spanish}) = 1 - P(Y = 	ext{English})\): The prior probability of the text being Spanish.

These values help guide the Bayesian model when making a final decision.

이 값들은 베이즈 모델이 최종 결정을 내리는 데 중요한 역할을 합니다.

---

## 2. Execution / 실행 방법
The program is executed as follows:

프로그램은 다음 명령어를 사용하여 실행할 수 있습니다:

```bash
python3 hw2.py [letter_file] [english_prior] [spanish_prior]
```

For example / 실행 예제:

```bash
python3 hw2.py samples/letter0.txt 0.6 0.4
```

### Expected Output / 예상 출력
If `samples/letter0.txt` contains:

만약 `samples/letter0.txt`에 다음과 같은 텍스트가 포함되어 있다면:

```
Hello! Let's understand the significance of probability in AI :)
```

Then the output will be / 실행 결과:

```
Q1
A 4
B 2
C 2
D 2
E 5
F 2
G 1
H 2
I 7
J 0
K 0
L 4
M 0
N 5
O 3
P 1
Q 0
R 2
S 3
T 4
U 1
V 0
W 0
X 0
Y 1
Z 0
Q2
-9.9344
-8.4265
Q3
-147.8619
-152.4015
Q4
0.9894

```

---

## 3. Theoretical Background / 이론적 배경

### 3.1 Bayes' Theorem / 베이즈 정리
We use **Bayesian Inference** to compute the probability that the text is written in English (\( Y = \text{English} \)) given the observed letter counts \( X \):

본 시스템은 **베이즈 추론(Bayesian Inference)**을 사용하여 주어진 텍스트가 특정 언어일 확률을 계산합니다.

\[
P(Y = y | X) = \frac{P(X | Y = y) P(Y = y)}{P(X)}
\]

Where:
- \( P(Y = y) \) is the **prior probability** of English or Spanish (**사전 확률**)
- \( P(X | Y = y) \) is the **likelihood** of observing letter frequencies given the language (**우도 함수**)
- \( P(X) \) is the **marginal probability** (normalization constant, **정규화 상수**)

### 3.2 Multinomial Probability Model / 다항 확률 모델
Each letter's probability is stored in `e.txt` (English) and `s.txt` (Spanish). The likelihood is modeled as:

각 문자에 대한 확률은 `e.txt` (영어) 및 `s.txt` (스페인어)에 저장되어 있으며, 가능성(likelihood)은 다음과 같이 모델링됩니다:

\[
P(X | Y = y) = C(X) \prod_{i=1}^{26} p_i^{X_i}
\]

Since directly computing the product of many small probabilities can cause **numerical underflow**, we take the **logarithm**:

작은 확률값들의 곱을 직접 계산할 경우 **수치적 언더플로우(numerical underflow)** 문제가 발생할 수 있으므로, **로그 변환(log transformation)**을 적용합니다.

\[
F(y) = \log P(Y = y) + \sum_{i=1}^{26} X_i \log p_i
\]

Using this transformation, we compute the probability:

이 변환을 사용하여 확률을 계산합니다:

\[
P(Y = \text{English} | X) = \frac{e^{F(\text{English})}}{e^{F(\text{English})} + e^{F(\text{Spanish})}}
\]

To prevent numerical overflow, we further transform:

수치적 오버플로우(numerical overflow)를 방지하기 위해 다음과 같이 변환합니다:

\[
P(Y = \text{English} | X) = \frac{1}{1 + e^{F(\text{Spanish}) - F(\text{English})}}
\]

---

## 4. Implementation Details / 구현 세부 사항

- `shred(filename)`: Reads a text file, converts all characters to uppercase, and counts occurrences of A-Z letters.
- `compute_F(counts, parameter_vector, prior)`: Computes the log-probability \( F(y) \) based on letter counts and given probabilities.
- `main()`: Parses input arguments, loads probability data, executes character counting, and calculates final language probability.

각 함수의 역할:
- `shred(filename)`: 텍스트 파일을 읽어 모든 문자를 대문자로 변환한 후, A-Z 문자 빈도를 계산합니다.
- `compute_F(counts, parameter_vector, prior)`: 문자 빈도를 기반으로 주어진 확률 벡터를 이용해 로그 확률 \( F(y) \)를 계산합니다.
- `main()`: 입력 인수를 해석하고 확률 데이터를 로드한 뒤, 문자 빈도를 분석하고 최종 언어 확률을 계산합니다.

---

## 5. Testing and Validation / 테스트 및 검증

### 5.1 Comparing Output to Expected Results / 출력 비교
Run the following command to compare the output:

출력 결과를 비교하려면 다음 명령을 실행합니다:

```bash
python3 hw2.py samples/letter0.txt 0.6 0.4 > my_output.txt
vimdiff my_output.txt samples/letter0_out.txt
```

### 5.2 Running Unit Tests / 단위 테스트 실행
Unit tests are included in `test_hw2.py`, which can be executed using `pytest`.

본 프로젝트는 `test_hw2.py` 파일에 단위 테스트를 포함하고 있으며, `pytest`를 사용하여 실행할 수 있습니다:

```bash
pytest test_hw2.py
```

---

## 6. Future Work / 향후 연구 방향

- **Extending the model** to classify more languages beyond English and Spanish.
- **Incorporating n-gram analysis** for improved language detection.
- **Applying machine learning techniques** to enhance accuracy.

- **영어와 스페인어 이외의 언어를 분류할 수 있도록 모델 확장**
- **n-그램 분석을 추가하여 정확도를 향상**
- **기계 학습 기법을 적용하여 성능 개선**

