"""
문서 스캐너 - CLI 진입점

실행 모드:
  python main.py scan <이미지경로>           단일 이미지 스캔
  python main.py trackbar <이미지경로>       트랙바 인터랙티브 모드
  python main.py batch <입력디렉토리>        배치 스캔 (20장 성능 평가)
  python main.py webcam                     웹캠 실시간 스캔
  python main.py eda <이미지디렉토리>        히스토그램 EDA 분석
"""

import sys
import os
import cv2

from core.scanner import scan_document, save_result, process_batch
from ui.trackbar_ui import run_trackbar_ui, display_results
from ui.webcam import run_webcam
from analysis.eda import analyze_images, save_histogram_comparison, print_stats_summary


def cmd_scan(image_path):
    """단일 이미지 스캔 모드."""
    image = cv2.imread(image_path)
    if image is None:
        print(f'[ERROR] Cannot load image: {image_path}')
        return

    result = scan_document(image)

    if result.success:
        base = os.path.splitext(os.path.basename(image_path))[0]
        output_path = f'scanned_{base}.png'
        save_result(result.scanned, output_path)
        print(f'[SUCCESS] Document scanned: {output_path}')
    else:
        print('[FAIL] Document contour not detected.')

    display_results(result)


def cmd_trackbar(image_path):
    """트랙바 인터랙티브 모드."""
    image = cv2.imread(image_path)
    if image is None:
        print(f'[ERROR] Cannot load image: {image_path}')
        return

    print('[INFO] Trackbar mode. Press "s" to save, "q" to quit.')
    run_trackbar_ui(image)


def cmd_batch(image_dir):
    """배치 스캔 및 성능 평가."""
    output_dir = os.path.join(image_dir, 'output')
    results = process_batch(image_dir, output_dir)

    if not results:
        print(f'[ERROR] No images found in: {image_dir}')
        return

    # 결과 요약 출력
    total = len(results)
    success = sum(1 for r in results if r['success'])
    fail = total - success

    print(f'\n=== Batch Scan Results ===')
    print(f'Total: {total}  |  Success: {success}  |  Fail: {fail}  |  Rate: {success / total * 100:.1f}%')
    print(f'\n{"#":<4} {"Filename":<30} {"Result":<10} {"Strategy":<25} {"Reason"}')
    print('-' * 90)

    for i, r in enumerate(results, 1):
        status = 'OK' if r['success'] else 'FAIL'
        print(f'{i:<4} {r["filename"]:<30} {status:<10} {r.get("strategy",""):<25} {r["reason"]}')

    print(f'\nOutput saved to: {output_dir}')


def cmd_eda(image_dir):
    """이미지 EDA 분석."""
    supported_ext = ('.jpg', '.jpeg', '.png', '.bmp')
    all_files = sorted([
        f for f in os.listdir(image_dir)
        if f.lower().endswith(supported_ext)
    ])

    if not all_files:
        print(f'[ERROR] No images found in: {image_dir}')
        return

    # 첫 5장을 쉬운 케이스, 나머지를 어려운 케이스로 분류
    # (실제 사용 시 직접 파일명 리스트를 지정하여 호출)
    easy = all_files[:5]
    hard = all_files[5:]

    print(f'Easy cases ({len(easy)}): {easy}')
    print(f'Hard cases ({len(hard)}): {hard}')

    easy_results, hard_results = analyze_images(image_dir, easy, hard)
    print_stats_summary(easy_results, hard_results)
    save_histogram_comparison(easy_results, hard_results,
                              os.path.join(image_dir, 'histogram_comparison.png'))


def print_usage():
    """사용법 출력."""
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    mode = sys.argv[1].lower()

    if mode == 'scan' and len(sys.argv) >= 3:
        cmd_scan(sys.argv[2])
    elif mode == 'trackbar' and len(sys.argv) >= 3:
        cmd_trackbar(sys.argv[2])
    elif mode == 'batch' and len(sys.argv) >= 3:
        cmd_batch(sys.argv[2])
    elif mode == 'webcam':
        run_webcam()
    elif mode == 'eda' and len(sys.argv) >= 3:
        cmd_eda(sys.argv[2])
    else:
        print_usage()


if __name__ == '__main__':
    main()
