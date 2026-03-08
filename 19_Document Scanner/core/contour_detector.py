"""
문서 윤곽선 추출 모듈

엣지 이미지에서 닫힌 윤곽선을 찾고, 면적 필터링과 다각형 근사를 통해
꼭짓점이 4개인 사각형 문서 영역을 검출한다.
"""

import cv2
import numpy as np


def find_contours(edges):
    """
    엣지 이미지에서 외곽 윤곽선을 찾는다.

    RETR_EXTERNAL: 최외곽 윤곽선만 추출 (내부 윤곽선 무시)
    CHAIN_APPROX_SIMPLE: 직선 구간은 양 끝점만 저장하여 메모리 절약

    Parameters:
        edges: Canny 엣지 이미지 (이진)

    Returns:
        윤곽선 리스트 (면적 내림차순 정렬)
    """
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 면적 기준 내림차순 정렬 (가장 큰 윤곽선이 문서일 가능성 높음)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours


def filter_by_area(contours, image_shape, min_ratio=0.05):
    """
    전체 이미지 면적 대비 일정 비율 이상인 윤곽선만 남긴다.

    작은 노이즈 윤곽선을 제거하기 위한 면적 필터링.

    Parameters:
        contours: 윤곽선 리스트
        image_shape: 이미지 shape (H, W, ...)
        min_ratio: 최소 면적 비율 (기본값 5%)

    Returns:
        면적 필터를 통과한 윤곽선 리스트
    """
    image_area = image_shape[0] * image_shape[1]
    min_area = image_area * min_ratio

    return [c for c in contours if cv2.contourArea(c) >= min_area]


def approximate_quadrilateral(contours, epsilon_ratio=0.02):
    """
    윤곽선을 다각형으로 근사하여 꼭짓점이 4개인 사각형을 찾는다.

    approxPolyDP는 Douglas-Peucker 알고리즘으로 윤곽선을 단순화한다.
    epsilon 값이 클수록 더 단순한 도형으로 근사된다.

    Parameters:
        contours: 면적 필터링된 윤곽선 리스트
        epsilon_ratio: 윤곽선 둘레 대비 근사 허용 오차 비율 (기본값 2%)

    Returns:
        4개 꼭짓점 좌표 배열 (shape: (4, 1, 2)) 또는 None
    """
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon_ratio * perimeter, True)

        if len(approx) == 4:
            return approx

    return None


def detect_document(edges, image_shape):
    """
    엣지 이미지에서 문서 사각형을 검출하는 통합 함수.

    Parameters:
        edges: Canny 엣지 이미지
        image_shape: 원본 이미지 shape

    Returns:
        4개 꼭짓점 좌표 배열 또는 None (검출 실패 시)
    """
    contours = find_contours(edges)
    contours = filter_by_area(contours, image_shape)
    quadrilateral = approximate_quadrilateral(contours)
    return quadrilateral


def draw_contour(image, quadrilateral, color=(0, 0, 255), thickness=3):
    """
    검출된 사각형 윤곽선을 이미지 위에 시각화한다.

    Parameters:
        image: 원본 컬러 이미지 (복사본에 그림)
        quadrilateral: 4개 꼭짓점 좌표 배열
        color: 선 색상 BGR (기본값: 빨간색)
        thickness: 선 두께

    Returns:
        윤곽선이 그려진 이미지 복사본
    """
    result = image.copy()
    if quadrilateral is not None:
        cv2.drawContours(result, [quadrilateral], -1, color, thickness)

        # 꼭짓점 표시
        for point in quadrilateral.reshape(-1, 2):
            cv2.circle(result, tuple(point), 8, (0, 255, 0), -1)

    return result
