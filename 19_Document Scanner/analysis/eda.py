"""
이미지 탐색적 분석 (EDA) 모듈

각 이미지의 픽셀 히스토그램을 분석하고,
쉬운 케이스와 어려운 케이스의 밝기 분포 차이를 시각화한다.
"""

import cv2
import numpy as np
import os


def compute_histogram(image):
    """
    이미지의 그레이스케일 히스토그램을 계산한다.

    Parameters:
        image: BGR 컬러 이미지

    Returns:
        histogram: (256,) 배열 - 각 밝기 값(0~255)의 픽셀 수
        stats: 통계 딕셔너리 (mean, std, median)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()

    stats = {
        'mean': float(np.mean(gray)),
        'std': float(np.std(gray)),
        'median': float(np.median(gray)),
    }

    return hist, stats


def analyze_images(image_dir, easy_filenames, hard_filenames):
    """
    쉬운/어려운 케이스 이미지들의 히스토그램을 분석한다.

    Parameters:
        image_dir: 이미지 디렉토리
        easy_filenames: 쉬운 케이스 파일명 리스트
        hard_filenames: 어려운 케이스 파일명 리스트

    Returns:
        easy_results, hard_results: 각각 [{filename, hist, stats}, ...] 리스트
    """
    def _analyze_group(filenames):
        results = []
        for fname in filenames:
            path = os.path.join(image_dir, fname)
            image = cv2.imread(path)
            if image is None:
                print(f'[WARN] Cannot load: {path}')
                continue
            hist, stats = compute_histogram(image)
            results.append({'filename': fname, 'hist': hist, 'stats': stats})
        return results

    easy_results = _analyze_group(easy_filenames)
    hard_results = _analyze_group(hard_filenames)

    return easy_results, hard_results


def save_histogram_comparison(easy_results, hard_results, output_path='histogram_comparison.png'):
    """
    쉬운/어려운 케이스의 평균 히스토그램을 비교 그래프로 저장한다.

    Matplotlib 없이 OpenCV만으로 히스토그램을 그린다.

    Parameters:
        easy_results: 쉬운 케이스 분석 결과 리스트
        hard_results: 어려운 케이스 분석 결과 리스트
        output_path: 출력 이미지 경로
    """
    canvas_h, canvas_w = 400, 512
    canvas = np.ones((canvas_h, canvas_w, 3), dtype=np.uint8) * 255

    def _average_hist(results):
        if not results:
            return np.zeros(256)
        hists = np.array([r['hist'] for r in results])
        return np.mean(hists, axis=0)

    easy_avg = _average_hist(easy_results)
    hard_avg = _average_hist(hard_results)

    max_val = max(easy_avg.max(), hard_avg.max())
    if max_val == 0:
        max_val = 1

    # 히스토그램 그리기
    for i in range(256):
        x = i * 2
        # 쉬운 케이스 (초록색)
        h_easy = int(easy_avg[i] / max_val * (canvas_h - 40))
        cv2.line(canvas, (x, canvas_h - 20), (x, canvas_h - 20 - h_easy), (0, 180, 0), 1)
        # 어려운 케이스 (빨간색, 반투명 효과)
        h_hard = int(hard_avg[i] / max_val * (canvas_h - 40))
        cv2.line(canvas, (x + 1, canvas_h - 20), (x + 1, canvas_h - 20 - h_hard), (0, 0, 200), 1)

    # 범례
    cv2.putText(canvas, 'Easy', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 180, 0), 1)
    cv2.putText(canvas, 'Hard', (80, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 1)

    cv2.imwrite(output_path, canvas)
    print(f'[INFO] Histogram comparison saved: {output_path}')


def print_stats_summary(easy_results, hard_results):
    """
    쉬운/어려운 케이스의 밝기 통계를 요약 출력한다.
    """
    print('\n=== Brightness Statistics ===')
    print(f'{"Group":<10} {"File":<25} {"Mean":>8} {"Std":>8} {"Median":>8}')
    print('-' * 62)

    for r in easy_results:
        s = r['stats']
        print(f'{"Easy":<10} {r["filename"]:<25} {s["mean"]:>8.1f} {s["std"]:>8.1f} {s["median"]:>8.1f}')

    for r in hard_results:
        s = r['stats']
        print(f'{"Hard":<10} {r["filename"]:<25} {s["mean"]:>8.1f} {s["std"]:>8.1f} {s["median"]:>8.1f}')

    if easy_results:
        easy_mean = np.mean([r['stats']['mean'] for r in easy_results])
        print(f'\n  Easy average brightness: {easy_mean:.1f}')
    if hard_results:
        hard_mean = np.mean([r['stats']['mean'] for r in hard_results])
        print(f'  Hard average brightness: {hard_mean:.1f}')
