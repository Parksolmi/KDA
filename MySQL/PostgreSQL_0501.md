# 📚 05월 01일 SQL 수업 정리

## ✏️ 목차

- [1. SQL 중급 문법 정리](#1-sql-중급-문법-정리)
- [2. JOIN 심화 실습](#2-join-심화-실습)
- [3. Scalar Functions](#3-scalar-functions)
- [4. CASE문](#4-case문)
- [5. 서브쿼리](#5-서브쿼리)
- [6. 에러슈팅](#6-에러슈팅)

---

## 1. SQL 중급 문법 정리

- 카티션 프로덕트: 모든 테이블의 경우의 조합 (R X S)
- JOIN 기준 == 기본키(PK)
  - INNER JOIN: 교접 (없는 값은 무시)
  - OUTER JOIN: 합접
    - LEFT JOIN: 왼쪽 기준 (반복 값과 NULL 값 포함)
    - RIGHT JOIN: 오른쪽 기준

### 원본 테이블

**Table 1**

| A   | B   |
| --- | --- |
| 1   | o   |
| 2   | o   |
| 3   | o   |

**Table 2**

| A   | D   |
| --- | --- |
| 1   | x   |
| 2   | x   |
| 4   | x   |

---

### 교집합 (INNER JOIN)

| A   | B   | D   |
| --- | --- | --- |
| 1   | o   | x   |
| 2   | o   | x   |

---

### 합집합 (FULL OUTER JOIN)

| A   | B    | D    |
| --- | ---- | ---- |
| 1   | o    | x    |
| 2   | o    | x    |
| 3   | o    | null |
| 4   | null | x    |

---

### 한쪽 기준 (LEFT JOIN)

| A   | B   | D    |
| --- | --- | ---- |
| 1   | o   | x    |
| 2   | o   | x    |
| 3   | o   | null |

```sql
SELECT c.name, ct.name
FROM country c INNER JOIN city ct ON c.capital=ct.id;

SELECT e.gender, COUNT(gender)
FROM titles t INNER JOIN employees e USING(emp_no)
WHERE t.to_date='9999-01-01' AND t.title LIKE 'Senior%'
GROUP BY e.gender;

-- 각 파트의 최근 매니저 이름(first_name, last_name) 가져오기
SELECT dm.dept_no, d.dept_name, e.first_name, e.last_name
FROM employees e
INNER JOIN dept_manager dm USING(emp_no)
INNER JOIN departments d USING(dept_no)
WHERE dm.to_date='9999-01-01';

-- 고객별 구입한 상품들에 쓴 총 비용과 평균 비용 구하기
SELECT ol.quantity, p.price, ol.quantity * p.price
FROM orderlines ol
INNER JOIN products p USING(prod_id);
```

- SELF JOIN : 자기 테이블 하나로 조인하는 것.

```sql
SELECT p1.prod_id, p1.title, p1.price,
       p2.prod_id AS common_id,
       p2.title AS common_title,
       p2.price AS common_price
FROM products p1
INNER JOIN products p2 ON p1.common_prod_id = p2.prod_id
WHERE p1.price > p2.price;

-- 매니저 경험이 없는 직원은 몇명인지 구하기
SELECT COUNT(*)
FROM employees e LEFT JOIN dept_manager dm USING(emp_no)
	WHERE dm.dept_no IS null;
	-- WHERE dm.dept_no IS NOT null; --이너조인 한 것과 같은 결과
```

## 2. JOIN 심화 실습

- 3개 테이블 조인

```sql
-- 1. Orderlines 테이블의 각 데이터에 해당 주문을 한 고객명을 붙여 보세요 (에러슈팅)
-- SELECT ol.prod_id, ol.quantity,
-- c.firstname, c.lastname, c.gender, c.age
-- FROM customers c LEFT JOIN(
-- SELECT *
-- FROM orderlines ol LEFT JOIN orders o USING(orderid)) USING(customerid);

SELECT ol.prod_id, ol.quantity, c.firstname, c.lastname, c.gender, c.age
	FROM orderlines ol LEFT JOIN orders o USING(orderid)
						LEFT JOIN customers c USING(customerid);


-- 2. 각 직급에서 성별 평균 연봉을 구하시오.
SELECT t.title, e.gender, AVG(salary) as salary_avg
FROM employees e INNER JOIN titles t USING(emp_no)
				INNER JOIN salaries s USING(emp_no)
WHERE t.to_date='9999-01-01' AND s.to_date='9999-01-01'
GROUP BY t.title, e.gender;

--pivot 적용
SELECT
  t.title,
  ROUND(AVG(CASE WHEN e.gender = 'M' THEN s.salary END), 2) AS male_avg_salary,
  ROUND(AVG(CASE WHEN e.gender = 'F' THEN s.salary END), 2) AS female_avg_salary
FROM employees e
INNER JOIN titles t USING(emp_no)
INNER JOIN salaries s USING(emp_no)
WHERE t.to_date = '9999-01-01'
  AND s.to_date = '9999-01-01'
GROUP BY t.title
ORDER BY t.title;
```

---

## 3. Scalar Functions

- 단일 행 함수: 각 행에 대해 결과 하나 발환

```sql
SELECT CONCAT(first_name, ' ', last_name), first_name || ' ' || last_name
FROM employees;
```

### 시간 관련 함수

```sql
SELECT EXTRACT(quarter FROM CURRENT_TIMESTAMP);
SELECT EXTRACT(DOY FROM CURRENT_TIMESTAMP);
SELECT TO_CHAR(CURRENT_TIMESTAMP, 'ddmmyy');

SELECT orderdate,
       EXTRACT (year from orderdate),
       EXTRACT(month from orderdate)
FROM orders;

SELECT CURRENT_DATE - orderdate FROM orders;
SELECT AGE(CURRENT_DATE, orderdate) FROM orders;
SELECT orderdate, orderdate + INTERVAL '5 days' FROM orders;

-- 나이가 60이상
SELECT CONCAT(first_name, ' ', last_name),
       AGE(CURRENT_TIMESTAMP, birth_date)
FROM employees
WHERE EXTRACT('year' FROM AGE(CURRENT_TIMESTAMP, birth_date)) >= 70;
```

---

## 4. CASE문

```sql
SELECT
  CASE
    WHEN population > 10000000 THEN 'big_country'
    WHEN population > 1000000 THEN 'middle_country'
    ELSE 'small_country'
  END
FROM country;
```

### 실전

```sql
SELECT *,
  CASE
    WHEN to_date = '9999-01-01' THEN CURRENT_DATE
    ELSE to_date
  END
FROM dept_manager;

-- 부서별 남녀 성비
SELECT
  dept_no,
  COUNT(CASE WHEN gender = 'M' THEN 1 END) AS M,
  COUNT(CASE WHEN gender = 'F' THEN 1 END) AS F
FROM employees
JOIN dept_emp USING (emp_no)
GROUP BY dept_no
ORDER BY dept_no;
```

---

## 5. 서브쿼리

```sql
-- 형식
SELECT *
FROM country
	WHERE population > 논리

-- 실전연습
-- 1. SELECT절에 사용
SELECT name, population, (SELECT AVG(population) FROM country)
FROM country



-- 2. WHERE절에 사용
SELECT *
FROM country
	WHERE population > (SELECT AVG(population) FROM country);

SELECT *
FROM country
	WHERE population = (SELECT MAX(population) FROM country);

-- 현재 매니저를 맡고 있는 직원 정보 가져오기
SELECT *
FROM employees
	WHERE emp_no IN (SELECT emp_no FROM dept_manager WHERE to_date='9999-01-01')

-- 현재 시니어인 직원들의 정보 가져오기
SELECT *
FROM employees
WHERE emp_no IN (SELECT emp_no
									FROM titles
									WHERE to_date='9999-01-01' AND title LIKE 'Senior%');

-- 3. FROM절에 사용
SELECT *
FROM employees e INNER JOIN
(SELECT * FROM dept_manager
	WHERE to_date='9999-01-01') t
USING(emp_no);

-- 각 부서의 매니저들의 이름과 입사한지 몇 년이나 지났는지 계산하시오
SELECT
  m.dept_no,
  e.first_name,
  e.last_name,
  AGE(CURRENT_DATE, m.from_date) AS years_worked
FROM (
  SELECT * FROM dept_manager
) m
JOIN employees e USING(emp_no);

-- 근데 사실은 JOIN이 더 효율적..
SELECT dept_no, first_name, last_name, AGE(CURRENT_DATE, from_date)
FROM dept_manager INNER JOIN employees USING(emp_no);

```

---

## 6. 에러슈팅

### 잘못된 예

```sql
SELECT ol.prod_id, ol.quantity,
       c.firstname, c.lastname, c.gender, c.age
FROM customers c
LEFT JOIN (
  SELECT ol.prod_id, ol.quantity, o.customerid
  FROM orderlines ol
  LEFT JOIN orders o USING(orderid)
) ON c.customerid = o.customerid;
```

**에러:** `missing FROM-clause entry for table "o"`

### 수정된 예

```sql
SELECT ol_sub.prod_id, ol_sub.quantity,
       c.firstname, c.lastname, c.gender, c.age
FROM customers c
LEFT JOIN (
  SELECT ol.prod_id, ol.quantity, o.customerid
  FROM orderlines ol
  LEFT JOIN orders o USING(orderid)
) AS ol_sub
ON c.customerid = ol_sub.customerid;
```

**설명:** 서브쿼리에는 반드시 별칭을 붙여야 바깥 쿼리에서 참조 가능하다.
