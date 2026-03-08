"""
이미지 후처리 모듈

투시 변환된 이미지에 적응형 이진화를 적용하여
그림자나 조명 얼룩이 있어도 글씨가 선명한 스캔본을 만든다.
"""

import cv2
import numpy as np


def adaptive_threshold(image, block_size=21, c=10):
    """
    적응형 이진화를 적용한다.

    일반 이진화는 하나의 고정 임계값을 사용하므로 조명이 불균일한 이미지에서
    일부 영역이 너무 밝거나 어둡게 처리된다.
    적응형 이진화는 각 픽셀 주변의 지역적 평균을 기준으로 임계값을 결정하므로
    그림자나 조명 차이가 있는 문서에서도 비교적 균일한 결과를 얻을 수 있다.

    Parameters:
        image: 투시 변환된 컬러 이미지 (BGR)
        block_size: 임계값 계산에 사용할 이웃 영역 크기 (홀수, 기본값 21)
        c: 계산된 평균에서 빼는 상수 (기본값 10)

    Returns:
        이진화된 그레이스케일 이미지
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # block_size는 홀수이고 1보다 커야 한다
    if block_size % 2 == 0:
        block_size += 1
    if block_size < 3:
        block_size = 3

    binary = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        block_size,
        c
    )

    return binary


def sharpen(image):
    """
    샤프닝 필터를 적용하여 텍스트 선명도를 높인다.

    Parameters:
        image: 입력 이미지

    Returns:
        샤프닝이 적용된 이미지
    """
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
    return cv2.filter2D(image, -1, kernel)


def postprocess(warped, apply_sharpen=False, block_size=21, c=10):
    """
    후처리 파이프라인: (선택적 샤프닝 →) 적응형 이진화

    Parameters:
        warped: 투시 변환된 이미지
        apply_sharpen: 샤프닝 적용 여부
        block_size: 이진화 블록 크기
        c: 이진화 상수

    Returns:
        후처리된 이미지
    """
    if warped is None:
        return None

    if apply_sharpen:
        warped = sharpen(warped)

    return adaptive_threshold(warped, block_size, c)
