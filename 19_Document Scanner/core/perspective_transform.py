"""
기하학적 변환 모듈

4개의 꼭짓점 좌표를 기하학적 원리로 직접 정렬하고,
투시 변환(Perspective Transform)을 적용하여 문서를 반듯한 직사각형으로 펴준다.

좌표 정렬 로직은 외부 기하 라이브러리에 의존하지 않고 직접 구현한다.
"""

import cv2
import numpy as np


def order_points(pts):
    """
    4개의 꼭짓점을 [좌상, 우상, 우하, 좌하] 순서로 정렬한다.

    정렬 원리:
    1. x+y 합이 가장 작은 점 → 좌상 (왼쪽 위에 가까울수록 합이 작음)
    2. x+y 합이 가장 큰 점 → 우하 (오른쪽 아래에 가까울수록 합이 큼)
    3. y-x 차이가 가장 작은 점 → 우상 (x가 크고 y가 작을수록 차이가 작음)
    4. y-x 차이가 가장 큰 점 → 좌하 (x가 작고 y가 클수록 차이가 큼)

    Parameters:
        pts: 4개의 좌표 배열 (shape 무관, 총 4개 점)

    Returns:
        정렬된 좌표 배열 (4, 2) - [좌상, 우상, 우하, 좌하]
    """
    pts = pts.reshape(4, 2).astype(np.float32)
    ordered = np.zeros((4, 2), dtype=np.float32)

    # x + y 합 계산
    s = np.sum(pts, axis=1)
    ordered[0] = pts[np.argmin(s)]  # 좌상: 합이 최소
    ordered[2] = pts[np.argmax(s)]  # 우하: 합이 최대

    # x - y 차이 계산
    # np.diff(axis=1)은 y - x를 반환하므로,
    # 우상(x 큼, y 작음)은 y-x가 가장 작고, 좌하(x 작음, y 큼)는 y-x가 가장 크다.
    d = np.diff(pts, axis=1).flatten()
    ordered[1] = pts[np.argmin(d)]  # 우상: y-x가 최소 (= x-y가 최대)
    ordered[3] = pts[np.argmax(d)]  # 좌하: y-x가 최대 (= x-y가 최소)

    return ordered


def compute_output_dimensions(ordered_pts):
    """
    정렬된 4개 꼭짓점 사이의 거리를 계산하여
    변환 결과 이미지의 가로/세로 크기를 결정한다.

    상단 변과 하단 변 중 더 긴 쪽을 가로로,
    좌측 변과 우측 변 중 더 긴 쪽을 세로로 사용한다.

    Parameters:
        ordered_pts: 정렬된 좌표 (4, 2) - [좌상, 우상, 우하, 좌하]

    Returns:
        (width, height) 정수 튜플
    """
    tl, tr, br, bl = ordered_pts

    # 상단 변과 하단 변의 길이
    width_top = np.sqrt((tr[0] - tl[0]) ** 2 + (tr[1] - tl[1]) ** 2)
    width_bottom = np.sqrt((br[0] - bl[0]) ** 2 + (br[1] - bl[1]) ** 2)
    width = int(max(width_top, width_bottom))

    # 좌측 변과 우측 변의 길이
    height_left = np.sqrt((bl[0] - tl[0]) ** 2 + (bl[1] - tl[1]) ** 2)
    height_right = np.sqrt((br[0] - tr[0]) ** 2 + (br[1] - tr[1]) ** 2)
    height = int(max(height_left, height_right))

    return width, height


def warp_perspective(image, quadrilateral):
    """
    검출된 사각형 영역을 투시 변환하여 직사각형으로 펴준다.

    1. 꼭짓점을 순서대로 정렬한다
    2. 출력 이미지 크기를 계산한다
    3. 변환 행렬을 구한 뒤 warpPerspective를 적용한다

    Parameters:
        image: 원본 컬러 이미지
        quadrilateral: 4개 꼭짓점 좌표 배열

    Returns:
        투시 변환된 이미지 또는 None (실패 시)
    """
    if quadrilateral is None:
        return None

    ordered = order_points(quadrilateral)
    width, height = compute_output_dimensions(ordered)

    if width <= 0 or height <= 0:
        return None

    # 변환 목표 좌표 (반듯한 직사각형)
    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype=np.float32)

    # 투시 변환 행렬 계산 및 적용
    matrix = cv2.getPerspectiveTransform(ordered, dst)
    warped = cv2.warpPerspective(image, matrix, (width, height))

    return warped
