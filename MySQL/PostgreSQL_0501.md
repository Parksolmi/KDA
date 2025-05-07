# 📚 05월 01일 SQL 수업 정리

## ✏️ 목차

- [1. UNION](#1-union)
- [2. INTERSECT](#2-intersect)
- [3. 파티션](#3-파티션)
- [4. Window Function](#4-window-function)
- [5. 비디오 렌탈 데이터 분석](#5-비디오-렌탈-데이터-분석)

---

## 1. UNION

- `UNION`: 서로 다른 두 SELECT 결과를 합치되, **중복은 제거**
- `UNION ALL`: **중복도 포함**하여 합침

```sql
SELECT name FROM customers
UNION
SELECT name FROM employees;

SELECT name FROM customers
UNION ALL
SELECT name FROM employees;
```

---

## 2. INTERSECT

- `INTERSECT`: 두 SELECT 결과에서 **공통되는 행만 반환**
- 일부 DBMS에서는 `INTERSECT` 지원하지 않음 (예: MySQL → JOIN/EXISTS로 대체)

```sql
SELECT customer_id FROM orders
INTERSECT
SELECT customer_id FROM returns;
```

---

## 3. 파티션

- `PARTITION BY`는 그룹핑 기준을 설정하여 **윈도우 함수가 그룹 내에서 작동**하게 함
- 주로 `OVER()` 절과 함께 사용

```sql
-- 각 고객의 월별 구매액과 전월 누적 합계 구하기
SELECT *,
  SUM(totalamount) OVER (
    PARTITION BY customerid
    ORDER BY orderdate
    ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
  ) AS rolling_sum
FROM orders;

-- 대륙별 지역별 인구 순위
SELECT name, continent, region, population,
  RANK() OVER (
    PARTITION BY continent, region
    ORDER BY population DESC
  ) AS rank
FROM country;

-- 대륙별 지역별 인구 1위 국가만 추출
SELECT *
FROM (
  SELECT name, continent, region, population,
    RANK() OVER (
      PARTITION BY continent, region
      ORDER BY population DESC
    ) AS rank
  FROM country
) t
WHERE t.rank = 1;

-- 카테고리별 가격이 가장 높은 항목 조회 (예시 필요)
```

---

## 4. Window Function

- `OVER()` 절을 사용하여 전체 또는 그룹 내에서 순위, 누적합, 평균 등을 계산
- 대표 함수: `RANK()`, `ROW_NUMBER()`, `DENSE_RANK()`, `SUM()`, `AVG()` 등

```sql
-- 직원별 연봉 순위
SELECT emp_no, salary,
  RANK() OVER (ORDER BY salary DESC) AS salary_rank
FROM salaries;

-- 부서별 연봉 순위
SELECT dept_no, emp_no, salary,
  RANK() OVER (PARTITION BY dept_no ORDER BY salary DESC) AS dept_salary_rank
FROM dept_emp
JOIN salaries USING(emp_no);
```

---

## 5. 비디오 렌탈 데이터 분석

```sql
-- 동명이인 영화배우 조회
SELECT first_name, last_name, COUNT(*)
FROM actor
GROUP BY first_name, last_name
HAVING COUNT(*) > 1;

-- 국가별 회원 수
SELECT co.country, co.country_id, COUNT(*)
FROM city c
  INNER JOIN address a USING(city_id)
  INNER JOIN country co ON c.country_id = co.country_id
  INNER JOIN customer USING(address_id)
GROUP BY co.country_id;

-- rating 별 총 매출액 구하기
SELECT f.rating, SUM(p.amount)
FROM film f
  INNER JOIN inventory i USING(film_id)
  INNER JOIN rental r USING(inventory_id)
  INNER JOIN payment p USING(rental_id)
GROUP BY f.rating;

-- 4일 이상 대여 시 연체로 간주 → 전체 연체율 구하기
SELECT ROUND(
  (SELECT COUNT(*) FROM rental WHERE EXTRACT(DAY FROM return_date - rental_date) > 4) * 1.0 /
  (SELECT COUNT(*) FROM rental),
  2
) AS overdue_rate;

-- 월별 비디오 렌탈 횟수가 가장 많은 비디오
SELECT EXTRACT(YEAR FROM r.rental_date) AS year,
       EXTRACT(MONTH FROM r.rental_date) AS month,
       f.title,
       COUNT(*) AS count
FROM rental r
  INNER JOIN inventory i USING(inventory_id)
  INNER JOIN film f USING(film_id)
GROUP BY year, month, f.title;

-- 위 쿼리에 순위 추가
SELECT *, RANK() OVER (PARTITION BY year, month ORDER BY count DESC) AS rank
FROM (
  SELECT EXTRACT(YEAR FROM r.rental_date) AS year,
         EXTRACT(MONTH FROM r.rental_date) AS month,
         f.title,
         COUNT(*) AS count
  FROM rental r
    INNER JOIN inventory i USING(inventory_id)
    INNER JOIN film f USING(film_id)
  GROUP BY year, month, f.title
) sub;

-- CTE (공통 테이블 표현식) 사용
WITH sub_table AS (
  SELECT EXTRACT(YEAR FROM r.rental_date) AS year,
         EXTRACT(MONTH FROM r.rental_date) AS month,
         f.title,
         COUNT(*) AS count
  FROM rental r
    INNER JOIN inventory i USING(inventory_id)
    INNER JOIN film f USING(film_id)
  GROUP BY year, month, f.title
)
SELECT *, RANK() OVER (PARTITION BY year, month ORDER BY count DESC) AS rank
FROM sub_table;

-- 월별 렌탈 횟수 1위인 비디오만 조회
SELECT *
FROM (
  SELECT *, RANK() OVER (PARTITION BY year, month ORDER BY count DESC) AS rank
  FROM sub_table
) ranked
WHERE rank = 1;
```
