"""
문서 스캐너 파이프라인

전처리 → 엣지 검출 → 윤곽선 추출 → 투시 변환 → 후처리를 하나의 파이프라인으로 통합한다.
기본 파라미터로 실패할 경우, 다중 전략을 자동으로 시도하여 검출률을 높인다.

전략 설계 배경:
  20장 테스트 결과 기본 파라미터(blur=5, canny 50/150)로 75% 성공.
  실패 이미지를 분석하여 다음 폴백 전략을 도출했다.
  1단계: 파라미터 변경 (블러, Canny 임계값 조합)
  2단계: Morphology 보강 (끊긴 엣지 연결)
  3단계: 적응형 임계값 전처리 (배경-문서 대비가 낮은 경우)
  4단계: 확장 epsilon (극도로 어려운 케이스)
"""

import cv2
import numpy as np
import os

from core.preprocessing import to_grayscale, apply_gaussian_blur, detect_edges
from core.contour_detector import (
    detect_document, draw_contour,
    find_contours, filter_by_area, approximate_quadrilateral
)
from core.perspective_transform import warp_perspective
from core.postprocessing import postprocess


class ScanResult:
    """스캔 파이프라인의 각 단계 결과를 담는 데이터 클래스."""

    def __init__(self):
        self.original = None
        self.gray = None
        self.blurred = None
        self.edges = None
        self.contour_image = None
        self.quadrilateral = None
        self.warped = None
        self.scanned = None
        self.success = False
        self.strategy = ''          # 성공한 전략 이름


# ====================================================================== #
#  전략 정의
# ====================================================================== #

PARAM_STRATEGIES = [
    {'blur_kernel': 5,  'canny_low': 50,  'canny_high': 150},
    {'blur_kernel': 7,  'canny_low': 30,  'canny_high': 100},
    {'blur_kernel': 3,  'canny_low': 30,  'canny_high': 100},
    {'blur_kernel': 5,  'canny_low': 20,  'canny_high': 80},
    {'blur_kernel': 9,  'canny_low': 40,  'canny_high': 120},
    {'blur_kernel': 3,  'canny_low': 20,  'canny_high': 60},
]


def _try_basic(image, gray, params):
    """기본 Canny 파이프라인."""
    blurred = apply_gaussian_blur(gray, params['blur_kernel'])
    edges = detect_edges(blurred, params['canny_low'], params['canny_high'])
    quad = detect_document(edges, image.shape)
    return edges, quad


def _try_morphology(image, gray, params, dilate_iter=2, erode_iter=1):
    """Morphology 보강: 팽창→침식으로 끊긴 엣지를 연결한다."""
    blurred = apply_gaussian_blur(gray, params['blur_kernel'])
    edges = detect_edges(blurred, params['canny_low'], params['canny_high'])
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    edges = cv2.dilate(edges, kernel, iterations=dilate_iter)
    edges = cv2.erode(edges, kernel, iterations=erode_iter)
    quad = detect_document(edges, image.shape)
    return edges, quad


def _try_adaptive_threshold(image, gray):
    """적응형 임계값 전처리: 배경-문서 대비가 낮을 때 경계를 강화한다."""
    blurred = apply_gaussian_blur(gray, 5)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 5
    )
    edges = detect_edges(thresh, 50, 150)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    edges = cv2.dilate(edges, kernel, iterations=1)
    quad = detect_document(edges, image.shape)
    return edges, quad


def _try_expanded_epsilon(image, gray):
    """확장 epsilon: 다각형 근사 허용 범위를 넓혀 최후 수단으로 시도한다."""
    for eps in [0.03, 0.04, 0.05]:
        for blur_k in [3, 5, 7]:
            for clow, chigh in [(20, 60), (30, 80), (30, 100)]:
                blurred = apply_gaussian_blur(gray, blur_k)
                edges = detect_edges(blurred, clow, chigh)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                for dil in [1, 2, 3]:
                    e = cv2.dilate(edges, kernel, iterations=dil)
                    e = cv2.erode(e, kernel, iterations=max(1, dil - 1))
                    contours = find_contours(e)
                    contours = filter_by_area(contours, image.shape)
                    quad = approximate_quadrilateral(contours, epsilon_ratio=eps)
                    if quad is not None:
                        warped = warp_perspective(image, quad)
                        if warped is not None:
                            wh, ww = warped.shape[:2]
                            aspect = max(ww, wh) / max(min(ww, wh), 1)
                            if 1.1 < aspect < 2.0:
                                return e, quad
    return None, None


# ====================================================================== #
#  메인 스캔 함수
# ====================================================================== #

def scan_document(image, blur_kernel=5, canny_low=50, canny_high=150,
                  threshold_block=21, threshold_c=10, auto_fallback=True):
    """
    하나의 이미지에 대해 전체 스캔 파이프라인을 실행한다.

    auto_fallback=True이면 기본 파라미터 실패 시 다중 전략을 자동 시도한다.
    auto_fallback=False이면 주어진 파라미터로만 1회 시도한다(트랙바 모드용).

    Parameters:
        image: BGR 컬러 이미지
        blur_kernel, canny_low, canny_high: 전처리 파라미터
        threshold_block, threshold_c: 후처리 이진화 파라미터
        auto_fallback: 다중 전략 자동 시도 여부

    Returns:
        ScanResult 객체
    """
    result = ScanResult()
    result.original = image.copy()
    result.gray = to_grayscale(image)
    result.blurred = apply_gaussian_blur(result.gray, blur_kernel)

    # 1단계: 지정된 파라미터로 시도
    edges, quad = _try_basic(
        image, result.gray,
        {'blur_kernel': blur_kernel, 'canny_low': canny_low, 'canny_high': canny_high}
    )
    result.edges = edges

    if quad is not None:
        result.strategy = 'basic'
    elif auto_fallback:
        # 2단계: 다른 파라미터 조합
        for params in PARAM_STRATEGIES[1:]:
            edges, quad = _try_basic(image, result.gray, params)
            if quad is not None:
                result.edges = edges
                result.strategy = (
                    f'params(blur={params["blur_kernel"]},'
                    f'canny={params["canny_low"]}/{params["canny_high"]})'
                )
                break

        # 3단계: Morphology 보강
        if quad is None:
            for params in PARAM_STRATEGIES[:3]:
                edges, quad = _try_morphology(image, result.gray, params)
                if quad is not None:
                    result.edges = edges
                    result.strategy = 'morphology'
                    break

        # 4단계: 적응형 임계값 전처리
        if quad is None:
            edges, quad = _try_adaptive_threshold(image, result.gray)
            if quad is not None:
                result.edges = edges
                result.strategy = 'adaptive_threshold'

        # 5단계: 확장 epsilon (최후 수단)
        if quad is None:
            edges, quad = _try_expanded_epsilon(image, result.gray)
            if quad is not None:
                result.edges = edges
                result.strategy = 'expanded_epsilon'

    # 결과 조합
    result.quadrilateral = quad
    result.contour_image = draw_contour(image, quad)

    if quad is None:
        result.success = False
        return result

    result.warped = warp_perspective(image, quad)
    if result.warped is None:
        result.success = False
        return result

    result.scanned = postprocess(result.warped, block_size=threshold_block, c=threshold_c)
    result.success = True
    return result


def save_result(scanned_image, output_path):
    """스캔 결과를 이미지 파일로 저장한다."""
    if scanned_image is None:
        return False
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    return cv2.imwrite(output_path, scanned_image)


def process_batch(image_dir, output_dir, **params):
    """
    디렉토리 내 모든 이미지에 대해 배치 스캔을 수행한다.

    Returns:
        results: [{filename, success, strategy, reason}, ...] 리스트
    """
    os.makedirs(output_dir, exist_ok=True)
    supported_ext = ('.jpg', '.jpeg', '.png', '.bmp')
    results = []

    for filename in sorted(os.listdir(image_dir)):
        if not filename.lower().endswith(supported_ext):
            continue

        filepath = os.path.join(image_dir, filename)
        image = cv2.imread(filepath)

        if image is None:
            results.append({
                'filename': filename, 'success': False,
                'strategy': '', 'reason': 'Failed to load image'
            })
            continue

        scan = scan_document(image, **params)

        if scan.success:
            save_result(scan.scanned, os.path.join(output_dir, f'scanned_{filename}'))
            save_result(scan.contour_image, os.path.join(output_dir, f'contour_{filename}'))
            save_result(scan.warped, os.path.join(output_dir, f'warped_{filename}'))

        results.append({
            'filename': filename,
            'success': scan.success,
            'strategy': scan.strategy,
            'reason': '' if scan.success else 'Document contour not detected'
        })

    return results
