"""
트랙바 UI 모듈

블러 강도와 Canny 임계값을 트랙바로 실시간 조절하면서
각 처리 단계의 결과를 윈도우로 확인할 수 있는 인터페이스를 제공한다.
"""

import cv2
from core.scanner import scan_document


# 트랙바 콜백 (OpenCV 트랙바는 콜백이 필수이나, 루프에서 값을 읽으므로 빈 함수 사용)
def _nothing(x):
    pass


def run_trackbar_ui(image):
    """
    트랙바 기반 인터랙티브 UI를 실행한다.

    트랙바로 조절 가능한 파라미터:
    - Blur Kernel: 가우시안 블러 커널 크기 (1~31)
    - Canny Low: Canny 하한 임계값 (0~300)
    - Canny High: Canny 상한 임계값 (0~500)

    조작법:
    - 트랙바: 파라미터를 실시간으로 조절하면 결과가 즉시 갱신
    - 's' 키: 현재 파라미터로 스캔 결과 저장
    - 'q' 키 또는 ESC: 종료

    Parameters:
        image: BGR 컬러 이미지
    """
    window_name = 'Document Scanner - Trackbar'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # 트랙바 생성
    cv2.createTrackbar('Blur Kernel', window_name, 5, 31, _nothing)
    cv2.createTrackbar('Canny Low', window_name, 50, 300, _nothing)
    cv2.createTrackbar('Canny High', window_name, 150, 500, _nothing)

    while True:
        # 트랙바에서 현재 값 읽기
        blur_k = cv2.getTrackbarPos('Blur Kernel', window_name)
        canny_low = cv2.getTrackbarPos('Canny Low', window_name)
        canny_high = cv2.getTrackbarPos('Canny High', window_name)

        # 커널 크기 보정 (홀수, 최소 1)
        if blur_k < 1:
            blur_k = 1
        if blur_k % 2 == 0:
            blur_k += 1

        # 파이프라인 실행
        result = scan_document(image, blur_kernel=blur_k,
                               canny_low=canny_low, canny_high=canny_high,
                               auto_fallback=False)

        # 단계별 시각화
        cv2.imshow('1. Original', result.original)
        cv2.imshow('2. Preprocessed (Gray + Blur)', result.blurred)
        cv2.imshow('3. Edges (Canny)', result.edges)
        cv2.imshow('4. Contours', result.contour_image)

        if result.warped is not None:
            cv2.imshow('5. Warped', result.warped)

        if result.scanned is not None:
            cv2.imshow('6. Scanned (Final)', result.scanned)

        # 키 입력 처리
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q') or key == 27:  # q 또는 ESC
            break
        elif key == ord('s') and result.scanned is not None:
            cv2.imwrite('scanned_output.png', result.scanned)
            print('[INFO] Saved: scanned_output.png')

    cv2.destroyAllWindows()


def display_results(result, wait=True):
    """
    스캔 결과를 윈도우에 표시한다 (트랙바 없이 단순 표시).

    Parameters:
        result: ScanResult 객체
        wait: True이면 키 입력 대기
    """
    cv2.imshow('1. Original', result.original)

    if result.edges is not None:
        cv2.imshow('3. Edges', result.edges)

    if result.contour_image is not None:
        cv2.imshow('4. Contours', result.contour_image)

    if result.warped is not None:
        cv2.imshow('5. Warped', result.warped)

    if result.scanned is not None:
        cv2.imshow('6. Scanned', result.scanned)

    if wait:
        cv2.waitKey(0)
        cv2.destroyAllWindows()
