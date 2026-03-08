"""
이미지 전처리 모듈

컬러 이미지를 Grayscale로 변환하고, 가우시안 블러와 Canny Edge Detection을 적용한다.
각 단계는 독립 함수로 분리하여 파이프라인에서 조합할 수 있도록 설계한다.
"""

import cv2
import numpy as np


def to_grayscale(image):
    """
    컬러 이미지를 그레이스케일로 변환한다.

    Parameters:
        image: BGR 컬러 이미지 (H, W, 3)

    Returns:
        그레이스케일 이미지 (H, W)
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_gaussian_blur(gray, kernel_size=5):
    """
    가우시안 블러를 적용하여 노이즈를 제거한다.

    커널 크기가 클수록 블러가 강해지며, 미세한 엣지가 사라지고
    주요 윤곽선만 남게 된다. 커널 크기는 반드시 홀수여야 한다.

    Parameters:
        gray: 그레이스케일 이미지
        kernel_size: 블러 커널 크기 (홀수, 기본값 5)

    Returns:
        블러가 적용된 이미지
    """
    # 커널 크기가 짝수이면 홀수로 보정
    if kernel_size % 2 == 0:
        kernel_size += 1
    if kernel_size < 1:
        kernel_size = 1

    return cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)


def detect_edges(blurred, low_threshold=50, high_threshold=150):
    """
    Canny Edge Detection으로 엣지를 검출한다.

    low_threshold: 이 값 미만의 그래디언트는 엣지가 아닌 것으로 버린다.
    high_threshold: 이 값 이상의 그래디언트는 확실한 엣지로 판정한다.
    두 값 사이의 그래디언트는 확실한 엣지와 연결된 경우에만 엣지로 포함된다.

    Parameters:
        blurred: 블러가 적용된 그레이스케일 이미지
        low_threshold: 하한 임계값 (기본값 50)
        high_threshold: 상한 임계값 (기본값 150)

    Returns:
        엣지 이미지 (이진 이미지)
    """
    return cv2.Canny(blurred, low_threshold, high_threshold)


def preprocess(image, blur_kernel=5, canny_low=50, canny_high=150):
    """
    전처리 파이프라인: 그레이스케일 → 블러 → 엣지 검출

    Parameters:
        image: BGR 컬러 이미지
        blur_kernel: 블러 커널 크기
        canny_low: Canny 하한 임계값
        canny_high: Canny 상한 임계값

    Returns:
        (gray, blurred, edges) 각 단계의 결과 이미지 튜플
    """
    gray = to_grayscale(image)
    blurred = apply_gaussian_blur(gray, blur_kernel)
    edges = detect_edges(blurred, canny_low, canny_high)
    return gray, blurred, edges
