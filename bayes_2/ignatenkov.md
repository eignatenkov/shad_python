---
title: "Байесовские методы, практика 2"
geometry: top=0.4in, bottom=0.8in, left=1in, right=1.in
author: "Егор Игнатенков"
output: pdf_document
header-includes:
- \usepackage{amsmath}
- \usepackage[russian]{babel}
- \usepackage{graphicx}
- \usepackage{float}
---

\newcommand{\E}{\mathbb{E}}
\newcommand{\D}{\mathrm{D}}
\let\oldtheta\theta
\renewcommand{\theta}{\boldsymbol{\oldtheta}}
\newcommand{\A}{\boldsymbol{A}}
\newcommand{\X}{\boldsymbol{X}}
\let\old\d
\renewcommand{\d}{\boldsymbol{d}}
\newcommand{\F}{\boldsymbol{F}}
\newcommand{\B}{\boldsymbol{B}}

#Теория

##1. Вывод формулы апостериорного распределения на координаты лица.

$$p(\d_k|\X_k, \theta, \A) = \frac{p(\X_k|\d_k, \theta)p(\d_k|\A)}{\sum\limits_{i,j} p(\X_k|(i,j), \theta) \A_{ij}}.$$

##2. Вывод точечных оценок для параметров на М-шаге.

Обозначим $p((i,j)|X_k, \theta, \A)$ за $q_{ijk}$. 
 
###Оценим $\A$.

$E_{q(\d)}\log p(\X,\d|\theta,\A) = \sum\limits_k \sum\limits_{i,j} q_{ijk} \log(p(X_k|(i,j), \theta)\A_{ij}) = C + \sum\limits_k\sum\limits_{i,j} q_{ijk}\log \A_{ij} = C + \sum\limits_{i,j}\log \A_{ij}\sum\limits_k q_{ijk} = C + \sum\limits_{i,j}\alpha_{ij}\log \A_{ij}$, где $\alpha_{ij} = \sum\limits_k q_{ijk}$, а $C$ не зависит от $\A$. Таким образом, нам нужно максимизировать $\sum\limits_{i,j}\alpha_{ij}\log \A_{ij}$ при условии, что $\sum\limits_{i,j}\A_{ij} = 1$.

Запишем лагранжиан. 

$L(\A, \lambda) = \sum\limits_{i,j}\alpha_{ij}\log \A_{ij} + \lambda(\sum\limits_{i,j}\A_{ij} - 1)$.

Приравняем к нулю частные производные, получим:

$\begin{cases}
\sum\limits_{i,j}\A_{ij} = 1,\\
\frac{\alpha_{ij}}{\A_{ij}} + \lambda = 0
\end{cases}$

Решаем, получаем, что $\A_{ij} = \frac{\alpha_{ij}}{\sum\limits_{i,j}\alpha_{ij}} = \frac{\sum\limits_k q_{ijk}}{\sum\limits_{i,j,k} q_{ijk}} = \frac{\sum\limits_k q_{ijk}}{K}$

###Оценка $\F$

$E_{q(\d)}\log p(\X,\d|\theta,\A) = \sum\limits_{i,j,k} q_{ijk} \log(p(X_k|(i,j), \theta)) + C_1 = \\ = \sum\limits_{i,j,k} q_{ijk}\sum\limits_{l=0}^{h-1}\sum\limits_{m=0}^{w-1}\log\mathcal{N}(X_k(i+l, j+m)|\F(l,m), s^2) + C_2$, где $C_1$ и $C_2$ не зависят от $\F$. 

Разные пиксели лица $\F(l,m)$ не зависят друг от друга, их можно оценивать по отдельности. Для конкретного $\F(l,m)$ нужно максимизировать следующее выражение:

$$\sum\limits_{i,j,k} q_{ijk}\log (\frac{1}{s\sqrt{2\pi}}e^{-\frac{(\X_k(i+l, j+m) - \F(l,m))^2}{2s^2}}) = C_3 - \frac{1}{2s^2}\sum\limits_{i,j,k} q_{ijk}(\X_k(i+l, j+m) - \F(l,m))^2,$$ что эквивалентно минимизации $$\sum\limits_{i,j,k} q_{ijk}(\X_k(i+l, j+m) - \F(l,m))^2.$$

Приравниваем к нулю производную, получаем, что 
$$ \sum\limits_{i,j,k} q_{ijk}\X_k(i+l, j+m) = \F(l,m)\sum\limits_{i,j,k} q_{ijk}$$
$$\F(l,m) = \frac{\sum\limits_{i,j,k} q_{ijk}\X_k(i+l, j+m)}{K}$$

###Оценка $\B$

Оценка для $\B$ получается схожим образом, но надо учитывать, что точке фона соответствуют точки $\X_k$ с теми же координатами, но только в тех случаях, когда область с лицом не накрывает нужную точку.

$$\B(l,m) = \frac{\sum\limits_{i,j,k} q_{ijk}\X_k(l,m)}{\sum\limits_{i,j,k} q_{ijk}},$$

где $(i,j)$ такие, что $(l,m) \notin faceArea((i,j))$

###Оценка $s^2$

Обозначим за $\mu^{ij}_{lm}$ пиксель, который находится на позиции $(l,m)$, если смещение лица равно $(i,j)$ (При заданных $\F$ и $\B$). Тогда, для оценки $s^2$ нам нужно максимизировать следующее выражение:

$E_{q(\d)}\log p(\X,\d|\theta,\A) = \sum\limits_{i,j,k} q_{ijk} \log(p(X_k|(i,j), \theta)) + C_1 = \sum\limits_{i,j,k} q_{ijk} \sum\limits_{l=0}^H\sum\limits_{m=0}^W \log (\frac{1}{s\sqrt{2\pi}}e^{-\frac{(\X_k(l,m) - \mu^{ij}_{lm})^2}{2s^2}}) + C_1 = \\ = -KHW\log s - \frac{\sum\limits_{i,j,k} q_{ijk}\sum\limits_{l=0}^H\sum\limits_{m=0}^W(\X_k(l,m) - \mu^{ij}_{lm})^2}{s^2}$

Обозначим $\sum\limits_{l=0}^H\sum\limits_{m=0}^W(\X_k(l,m) - \mu^{ij}_{lm})^2$ за $v_{ijk}$. Продифференцируем по $s$ и приравняем производную к нулю:

$$-\frac{HWK}{s} + \frac{\sum\limits_{i,j,k} q_{ijk}v_{ijk}}{s^3} = 0$$
$$s^2 = \frac{\sum\limits_{i,j,k} q_{ijk}v_{ijk}}{HWK}$$


##3. Вывод формулы для подсчета $\mathcal{L}(q, \theta, \A)$ 

$\mathcal{L}(q,\theta,\A) = \E_{q(\d)}\log p(\X,\d|\theta,\A) - \E_{q(\d)}\log q(\d) = \E_{q(\d)}\Big[\log\prod\limits_{k=1}^K p(\X_k | \d_k, \theta)p(\d_k | \A)\Big] - \E_{q(\d)}\Big[\log \prod\limits_{k=1}^K p(\d_k | \X_k, \theta, \A)\Big] = \sum\limits_k \sum\limits_{i, j} q_{ijk} \log [p(\X_k | (i,j), \theta)\A_{ij}]  - \sum\limits_k \sum\limits_{i, j}q_{ijk}\log q_{ijk}$

#Анализ

1. Была сгенерирована выборка из 50 изображений с такими "лицом" и фоном: 
 
\begin{figure}[H]
\centering
\includegraphics[width=100px]{smiley_small.png}
\includegraphics[width=150px]{bg_1.png}
\end{figure}

Смещение лица выбиралось случайным образом, $s=128$. Пример зашумленного изображения:

\begin{figure}[H]
\centering
\includegraphics[width=150px]{noise_1.png}
\end{figure}

Восстановленные лицо и фон для запуска с начальными условиями "черный фон, белое лицо" выглядели следующим образом:

\begin{figure}[H]
\centering
\includegraphics[width=100px]{gen_face_1.png}
\includegraphics[width=150px]{gen_bg_1.png}
\end{figure}

Стартовое приближение может некоторым образом повлиять на итоговый результат. Ниже приведены восстановленные изображения для трех разных случайно сгенерированных стартовых приближений лица, фона и дисперсии.

\begin{figure}[H]
\centering
\includegraphics[width=100px]{ds_1.png}
\includegraphics[width=100px]{ds_2.png}
\includegraphics[width=100px]{ds_3.png}
\end{figure}

Для получения максимально четкого изображения имеет смысл пробовать запускать EM алгоритм из разных стартовых приближений.

2. На тех же "лице" и фоне изменение размера выборки с 50 до 200 с шагом 50 существенных улучшений не показало. Нормированные значения оптимизируемого функционала были равны
```
[-4329.552, -4360.594, -4364.620, -4362.939, -4367.459]
```

Существенные изменения видны при увеличении размера обучающей выборки от 10 до 50 с шагом десять:

\begin{figure}[H]
\centering
\includegraphics[width=90px]{small_1.png}
\includegraphics[width=90px]{small_2.png}
\includegraphics[width=90px]{small_3.png}
\includegraphics[width=90px]{small_4.png}
\includegraphics[width=90px]{small_5.png}
\end{figure}

Уровень шума проверялся на выборке размером 50. Ниже результаты работы алгоритма для $s=208, 228, 238$.

\begin{figure}[H]
\centering
\includegraphics[width=100px]{s_208.png}
\includegraphics[width=100px]{s_228.png}
\includegraphics[width=100px]{s_238.png}
\end{figure}

3. Время работы алгоритма с выставленным и снятым параметром useMAP замерялось на двух выборках разных размеров и изображениях разных размеров. Результаты первого замера: 3.71 с и 6.81 с, второго замера: 35 с и 20.7 с. hard EM работает примерно вдвое быстрее. Сравнение результатов работы обычного EM и hard EM:

\begin{figure}[H]
\centering
\includegraphics[width=100px]{no_map.png}
\includegraphics[width=100px]{map.png}
\end{figure}

Результаты сильно отличаются, поскольку при большом шуме любая ошибка при MAP-оценке приводит к сильному изменению в оценке параметров на М-шаге.

\newpage

4. hard EM по всей выборке:

\begin{figure}[H]
\centering
\includegraphics[width=300px]{true_bg_usemap.png}
\includegraphics[width=100px]{true_face_usemap.png}
\end{figure}

EM по выборке из 500 картинок:

\begin{figure}[H]
\centering
\includegraphics[width=100px]{em_500.png}
\end{figure}

EM по всей выборке (срубил выполнение на разнице 10 между последними значениями функционала):

\begin{figure}[H]
\centering
\includegraphics[width=300px]{bg_full.png}
\includegraphics[width=100px]{face_ful.png}
\end{figure}