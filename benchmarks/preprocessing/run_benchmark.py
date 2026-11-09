"""benchmarks/preprocessing/run_benchmark.py"""

import json
import os
import statistics
import sys
import tempfile
import time
import urllib.request

from benchmarks.const import (
    PDF_URLS_JSON_PATH,
    PREPROCESSING_REPORT_DETAILS_ACADEMIC_DOCUMENT_VALIDATION_TIME_KEY,
    PREPROCESSING_REPORT_DETAILS_CHUNKING_TIME_KEY,
    PREPROCESSING_REPORT_DETAILS_EMBED_AND_INDEXING_TIME_KEY,
    PREPROCESSING_REPORT_DETAILS_KEY,
    PREPROCESSING_REPORT_DETAILS_PDF2MD_TIME_KEY,
    PREPROCESSING_REPORT_DETAILS_PDF_ID_KEY,
    PREPROCESSING_REPORT_DETAILS_TOT_TIME_KEY,
    PREPROCESSING_REPORT_JSON_PATH,
    PREPROCESSING_REPORT_METRIC_LABELS,
    PREPROCESSING_REPORT_P95_INDEX,
    PREPROCESSING_REPORT_P95_METHOD,
    PREPROCESSING_REPORT_P95_QUANTILES,
    PREPROCESSING_REPORT_P99_INDEX,
    PREPROCESSING_REPORT_P99_METHOD,
    PREPROCESSING_REPORT_P99_QUANTILES,
    PREPROCESSING_REPORT_ROUND_DIGITS,
    PREPROCESSING_REPORT_STATISTICS_MAX_KEY,
    PREPROCESSING_REPORT_STATISTICS_MEAN_KEY,
    PREPROCESSING_REPORT_STATISTICS_MEDIAN_KEY,
    PREPROCESSING_REPORT_STATISTICS_MIN_KEY,
    PREPROCESSING_REPORT_STATISTICS_P95_KEY,
    PREPROCESSING_REPORT_STATISTICS_P99_KEY,
    PREPROCESSING_REPORT_SUMMARY_KEY,
    PREPROCESSING_REPORT_SUMMARY_STATISTICS_KEY,
    PREPROCESSING_REPORT_SUMMARY_TOT_PDFS_KEY,
    PREPROCESSING_REPORT_TABLE_METRIC_HEADER,
    PREPROCESSING_REPORT_TABLE_METRIC_WIDTH,
    PREPROCESSING_REPORT_TABLE_STATISTIC_LABELS,
    PREPROCESSING_REPORT_TABLE_TITLE,
    PREPROCESSING_REPORT_TABLE_TITLE_PADDING,
    PREPROCESSING_REPORT_TABLE_VALUE_WIDTH,
    PREPROCESSING_REPORT_TABLE_WIDTH,
)
from src.config import config
from src.const import (
    UPLOAD_PAGE_UPLOADED_DOC_FORMAT,
    VECTOR_STORE_COLLECTION_NAME,
)
from src.preprocess import (
    _chunk_md,
    _create_and_store_embeddings,
    _is_valid_academic_doc,
    _pdf_to_md,
)


def _load_existing_report(save_path: str) -> tuple[list, set, dict]:
    """Load existing benchmark report if available.

    This function attempts to load an existing benchmark report from
    the specified JSON file. If the file exists and is valid, it extracts
    the list of PDF reports and the set of processed PDF IDs. If the file
    doesn't exist or is invalid, it initializes empty objects.

    Args:
        save_path (str):
            The path where the report JSON file is stored.

    Returns:
        tuple[list, set, dict]:
            A tuple containing the list of PDF reports, the set of processed
            PDF IDs, and the full report dictionary.
    """
    try:
        # Load existing PDF reports from benchmark
        # report if available
        with open(save_path) as f:
            report = json.load(f)
            pdf_reports = report.get(
                PREPROCESSING_REPORT_DETAILS_KEY,
                [],
            )
            processed_pdf_ids = {
                item[PREPROCESSING_REPORT_DETAILS_PDF_ID_KEY]
                for item in pdf_reports
            }
            return pdf_reports, processed_pdf_ids, report
    except Exception:
        # If the benchmark report file doesn't exist
        # or is invalid, initialize empty objects
        return [], set(), {}


def _download_pdf(url: str, save_path: str) -> bool:
    """Download a PDF from a URL and save it to the specified path.

    Args:
        url (str):
            The URL of the PDF to download.
        save_path (str):
            The local path where the PDF will be saved.

    Returns:
        bool:
            True if the download was successful, False otherwise.
    """
    try:
        # Make a request to the URL and download the PDF
        req = urllib.request.Request(url)
        with (
            urllib.request.urlopen(req) as response,
            open(save_path, "wb") as out_file,
        ):
            out_file.write(response.read())
        return True
    except Exception:
        return False


def _benchmark_single_pdf(pdf_path: str, pdf_id: str) -> dict | None:
    """Benchmark the preprocessing pipeline for a single PDF document.

    This function benchmarks the preprocessing pipeline for a single PDF document,
    measuring the time taken for each step of the preprocessing pipeline. The execution
    times for each step are collected and returned as a dictionary.

    Args:
        pdf_path (str):
            The path of the downloaded PDF file.
        pdf_id (str):
            The ID of the PDF.

    Returns:
        dict | None:
            A dictionary containing execution times for each step if successful,
            None otherwise.
    """
    # Start total timer for this PDF
    t_start_tot = time.perf_counter()

    # 1. Academic document validation
    t0 = time.perf_counter()
    is_valid = _is_valid_academic_doc(pdf_path)
    t_academic_validation = time.perf_counter() - t0
    if not is_valid:
        return None

    # 2. PDF to Markdown conversion
    t0 = time.perf_counter()
    md_content = _pdf_to_md(pdf_path)
    t_pdf2md = time.perf_counter() - t0
    if md_content is None:
        return None

    # 3. Structure-Aware Chunking
    t0 = time.perf_counter()
    chunks = _chunk_md(
        md_content,
        config.chunk_size,
        config.chunk_overlap,
    )
    t_chunking = time.perf_counter() - t0
    if chunks is None:
        return None

    # 4. Embedding & Vector Indexing
    t0 = time.perf_counter()
    _ = _create_and_store_embeddings(
        chunks,
        config.embedding_model_name,
        VECTOR_STORE_COLLECTION_NAME,
    )
    t_embed_and_indexing = time.perf_counter() - t0

    # Total time for this PDF
    t_tot = time.perf_counter() - t_start_tot

    return {
        PREPROCESSING_REPORT_DETAILS_PDF_ID_KEY: pdf_id,
        PREPROCESSING_REPORT_DETAILS_ACADEMIC_DOCUMENT_VALIDATION_TIME_KEY: round(
            t_academic_validation,
            PREPROCESSING_REPORT_ROUND_DIGITS,
        ),
        PREPROCESSING_REPORT_DETAILS_PDF2MD_TIME_KEY: round(
            t_pdf2md,
            PREPROCESSING_REPORT_ROUND_DIGITS,
        ),
        PREPROCESSING_REPORT_DETAILS_CHUNKING_TIME_KEY: round(
            t_chunking,
            PREPROCESSING_REPORT_ROUND_DIGITS,
        ),
        PREPROCESSING_REPORT_DETAILS_EMBED_AND_INDEXING_TIME_KEY: round(
            t_embed_and_indexing,
            PREPROCESSING_REPORT_ROUND_DIGITS,
        ),
        PREPROCESSING_REPORT_DETAILS_TOT_TIME_KEY: round(
            t_tot,
            PREPROCESSING_REPORT_ROUND_DIGITS,
        ),
    }


def _save_report(pdf_reports: list, save_path: str) -> dict:
    """Save the benchmark report to a JSON file.

    This function calculates step-specific and global preprocessing statistics
    based on the provided list of PDF reports. It then saves the report to a JSON file.

    Args:
        pdf_reports (list):
            A list of dictionaries containing the benchmark details for each PDF.
        save_path (str):
            The path where the report will be saved.

    Returns:
        dict:
            A dictionary containing a report with summary and details.
    """
    if not pdf_reports:
        return {}

    metric_keys = (
        PREPROCESSING_REPORT_DETAILS_ACADEMIC_DOCUMENT_VALIDATION_TIME_KEY,
        PREPROCESSING_REPORT_DETAILS_PDF2MD_TIME_KEY,
        PREPROCESSING_REPORT_DETAILS_CHUNKING_TIME_KEY,
        PREPROCESSING_REPORT_DETAILS_EMBED_AND_INDEXING_TIME_KEY,
        PREPROCESSING_REPORT_DETAILS_TOT_TIME_KEY,
    )
    statistics_by_metric = {}
    for metric_key in metric_keys:
        values = [report[metric_key] for report in pdf_reports]
        percentile_95 = (
            values[0]
            if len(values) == 1
            else statistics.quantiles(
                values,
                n=PREPROCESSING_REPORT_P95_QUANTILES,
                method=PREPROCESSING_REPORT_P95_METHOD,
            )[PREPROCESSING_REPORT_P95_INDEX]
        )
        percentile_99 = (
            values[0]
            if len(values) == 1
            else statistics.quantiles(
                values,
                n=PREPROCESSING_REPORT_P99_QUANTILES,
                method=PREPROCESSING_REPORT_P99_METHOD,
            )[PREPROCESSING_REPORT_P99_INDEX]
        )
        statistics_by_metric[metric_key] = {
            PREPROCESSING_REPORT_STATISTICS_MEAN_KEY: round(
                statistics.mean(values),
                PREPROCESSING_REPORT_ROUND_DIGITS,
            ),
            PREPROCESSING_REPORT_STATISTICS_MEDIAN_KEY: round(
                statistics.median(values),
                PREPROCESSING_REPORT_ROUND_DIGITS,
            ),
            PREPROCESSING_REPORT_STATISTICS_P95_KEY: round(
                percentile_95,
                PREPROCESSING_REPORT_ROUND_DIGITS,
            ),
            PREPROCESSING_REPORT_STATISTICS_P99_KEY: round(
                percentile_99,
                PREPROCESSING_REPORT_ROUND_DIGITS,
            ),
            PREPROCESSING_REPORT_STATISTICS_MIN_KEY: round(
                min(values),
                PREPROCESSING_REPORT_ROUND_DIGITS,
            ),
            PREPROCESSING_REPORT_STATISTICS_MAX_KEY: round(
                max(values),
                PREPROCESSING_REPORT_ROUND_DIGITS,
            ),
        }

    # Create a report dictionary with summary and details
    report = {
        PREPROCESSING_REPORT_SUMMARY_KEY: {
            PREPROCESSING_REPORT_SUMMARY_TOT_PDFS_KEY: len(pdf_reports),
            PREPROCESSING_REPORT_SUMMARY_STATISTICS_KEY: statistics_by_metric,
        },
        PREPROCESSING_REPORT_DETAILS_KEY: pdf_reports,
    }

    # Save the report to a JSON file
    with open(save_path, "w") as f:
        json.dump(report, f, indent=2)

    return report


def _display_report_summary(report: dict) -> None:
    """Display the benchmark summary.

    This function displays the benchmark summary in a formatted table. It extracts
    the relevant information from the report dictionary and prints it to the console.

    Args:
        report (dict):
            A dictionary containing the report summary and details.

    Returns:
        None
    """
    if report and PREPROCESSING_REPORT_SUMMARY_KEY in report:
        summary = report[PREPROCESSING_REPORT_SUMMARY_KEY]
        statistics_by_metric = summary.get(
            PREPROCESSING_REPORT_SUMMARY_STATISTICS_KEY,
            {},
        )
        if not statistics_by_metric:
            return

        print("\n" + "=" * PREPROCESSING_REPORT_TABLE_WIDTH)
        title = (
            PREPROCESSING_REPORT_TABLE_TITLE + " "
            f"(PDFs: {summary[PREPROCESSING_REPORT_SUMMARY_TOT_PDFS_KEY]})"
        )
        print(
            f"| {title:^{PREPROCESSING_REPORT_TABLE_WIDTH - PREPROCESSING_REPORT_TABLE_TITLE_PADDING}} |",
        )
        print("-" * PREPROCESSING_REPORT_TABLE_WIDTH)
        print(
            f"| {PREPROCESSING_REPORT_TABLE_METRIC_HEADER:<{PREPROCESSING_REPORT_TABLE_METRIC_WIDTH}} | "
            f"{PREPROCESSING_REPORT_TABLE_STATISTIC_LABELS[PREPROCESSING_REPORT_STATISTICS_MEAN_KEY]:>{PREPROCESSING_REPORT_TABLE_VALUE_WIDTH}} | "
            f"{PREPROCESSING_REPORT_TABLE_STATISTIC_LABELS[PREPROCESSING_REPORT_STATISTICS_MEDIAN_KEY]:>{PREPROCESSING_REPORT_TABLE_VALUE_WIDTH}} | "
            f"{PREPROCESSING_REPORT_TABLE_STATISTIC_LABELS[PREPROCESSING_REPORT_STATISTICS_P95_KEY]:>{PREPROCESSING_REPORT_TABLE_VALUE_WIDTH}} | "
            f"{PREPROCESSING_REPORT_TABLE_STATISTIC_LABELS[PREPROCESSING_REPORT_STATISTICS_P99_KEY]:>{PREPROCESSING_REPORT_TABLE_VALUE_WIDTH}} | "
            f"{PREPROCESSING_REPORT_TABLE_STATISTIC_LABELS[PREPROCESSING_REPORT_STATISTICS_MIN_KEY]:>{PREPROCESSING_REPORT_TABLE_VALUE_WIDTH}} | "
            f"{PREPROCESSING_REPORT_TABLE_STATISTIC_LABELS[PREPROCESSING_REPORT_STATISTICS_MAX_KEY]:>{PREPROCESSING_REPORT_TABLE_VALUE_WIDTH}} |",
        )
        print("-" * PREPROCESSING_REPORT_TABLE_WIDTH)
        for metric_key, label in PREPROCESSING_REPORT_METRIC_LABELS.items():
            metric = statistics_by_metric[metric_key]
            print(
                f"| {label:<{PREPROCESSING_REPORT_TABLE_METRIC_WIDTH}} | "
                f"{metric[PREPROCESSING_REPORT_STATISTICS_MEAN_KEY]:>{PREPROCESSING_REPORT_TABLE_VALUE_WIDTH}.{PREPROCESSING_REPORT_ROUND_DIGITS}f} | "
                f"{metric[PREPROCESSING_REPORT_STATISTICS_MEDIAN_KEY]:>{PREPROCESSING_REPORT_TABLE_VALUE_WIDTH}.{PREPROCESSING_REPORT_ROUND_DIGITS}f} | "
                f"{metric[PREPROCESSING_REPORT_STATISTICS_P95_KEY]:>{PREPROCESSING_REPORT_TABLE_VALUE_WIDTH}.{PREPROCESSING_REPORT_ROUND_DIGITS}f} | "
                f"{metric[PREPROCESSING_REPORT_STATISTICS_P99_KEY]:>{PREPROCESSING_REPORT_TABLE_VALUE_WIDTH}.{PREPROCESSING_REPORT_ROUND_DIGITS}f} | "
                f"{metric[PREPROCESSING_REPORT_STATISTICS_MIN_KEY]:>{PREPROCESSING_REPORT_TABLE_VALUE_WIDTH}.{PREPROCESSING_REPORT_ROUND_DIGITS}f} | "
                f"{metric[PREPROCESSING_REPORT_STATISTICS_MAX_KEY]:>{PREPROCESSING_REPORT_TABLE_VALUE_WIDTH}.{PREPROCESSING_REPORT_ROUND_DIGITS}f} |",
            )
        print("=" * PREPROCESSING_REPORT_TABLE_WIDTH)


def run_benchmark() -> None:
    """Benchmark the preprocessing pipeline for a set of PDFs.

    This function benchmarks the preprocessing pipeline for a set of PDFs specified
    in a JSON file. It measures the time taken for each step of the preprocessing
    pipeline and saves a report to a JSON file.

    Returns:
        None
    """
    # Load JSON file with PDF URLs
    with open(PDF_URLS_JSON_PATH) as f:
        json_file = json.load(f)

    # Load existing benchmark report if available
    pdf_reports, processed_pdf_ids, report = _load_existing_report(
        PREPROCESSING_REPORT_JSON_PATH,
    )

    # If benchmark data already exists, only refresh and display results
    if pdf_reports:
        report = _save_report(pdf_reports, PREPROCESSING_REPORT_JSON_PATH)
        _display_report_summary(report)
        return

    # Start benchmarking preprocessing pipeline for each PDF
    tot_pdfs = len(json_file)
    with tempfile.TemporaryDirectory() as temp_dir:
        for idx, (pdf_id, pdf_url) in enumerate(json_file.items(), 1):
            # Skip this PDF if already processed
            if pdf_id in processed_pdf_ids:
                continue

            # Print progress
            sys.stdout.write(
                f"\r\033[K[{(idx / tot_pdfs) * 100:>5.1f}%] Benchmarking preprocessing...",
            )
            sys.stdout.flush()

            # Download this PDF
            pdf_path = os.path.join(
                temp_dir,
                f"{pdf_id}.{UPLOAD_PAGE_UPLOADED_DOC_FORMAT}",
            )
            success = _download_pdf(pdf_url, pdf_path)
            if not success:
                continue

            # Benchmark single PDF
            pdf_report = _benchmark_single_pdf(pdf_path, pdf_id)
            if pdf_report is None:
                os.remove(pdf_path)
                continue

            # Collect benchmark details for this PDF and append to the list
            pdf_reports.append(pdf_report)

            # Save incremental benchmark report update to disk
            report = _save_report(pdf_reports, PREPROCESSING_REPORT_JSON_PATH)

            # Cleanup temporary downloaded PDF
            os.remove(pdf_path)

        print("\033[K")

    # Recalculate summary statistics from all existing details, including
    # reports loaded without running any new benchmark
    report = _save_report(pdf_reports, PREPROCESSING_REPORT_JSON_PATH)

    # Display report summary
    _display_report_summary(report)


if __name__ == "__main__":
    run_benchmark()
