"""benchmarks/preprocessing/run_benchmark.py"""

import json
import os
import sys
import tempfile
import time
import urllib.request

from benchmarks.const import (
    PDF_URLS_JSON_PATH,
    PREPROCESSING_REPORT_DETAILS_CHUNKING_TIME_KEY,
    PREPROCESSING_REPORT_DETAILS_EMBED_AND_INDEXING_TIME_KEY,
    PREPROCESSING_REPORT_DETAILS_KEY,
    PREPROCESSING_REPORT_DETAILS_PDF2MD_TIME_KEY,
    PREPROCESSING_REPORT_DETAILS_PDF_ID_KEY,
    PREPROCESSING_REPORT_DETAILS_TOT_TIME_KEY,
    PREPROCESSING_REPORT_JSON_PATH,
    PREPROCESSING_REPORT_SUMMARY_AVG_CHUNKING_TIME_KEY,
    PREPROCESSING_REPORT_SUMMARY_AVG_EMBED_AND_INDEXING_TIME_KEY,
    PREPROCESSING_REPORT_SUMMARY_AVG_PDF2MD_TIME_KEY,
    PREPROCESSING_REPORT_SUMMARY_AVG_TOT_TIME_KEY,
    PREPROCESSING_REPORT_SUMMARY_KEY,
    PREPROCESSING_REPORT_SUMMARY_TOT_PDFS_KEY,
)
from src.config import config
from src.const import (
    UPLOAD_PAGE_UPLOADED_DOC_FORMAT,
    VECTOR_STORE_COLLECTION_NAME,
)
from src.preprocess import (
    _chunk_md,
    _create_and_store_embeddings,
    _pdf_to_md,
)


def download_pdf(url: str, output_path: str) -> bool:
    """Download a PDF from a URL and save it to the specified output path.

    Args:
        url (str):
            The URL of the PDF to download.
        output_path (str):
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
            open(output_path, "wb") as out_file,
        ):
            out_file.write(response.read())
        return True
    except Exception:
        return False


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

    # Start benchmarking preprocessing pipeline for each PDF
    pdf_reports = []
    tot_pdfs = len(json_file)
    with tempfile.TemporaryDirectory() as temp_dir:
        for idx, (pdf_id, pdf_url) in enumerate(json_file.items(), 1):
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
            success = download_pdf(pdf_url, pdf_path)
            if not success:
                continue

            # Start total timer for this PDF
            t_start_tot = time.perf_counter()

            # 1. PDF to Markdown conversion
            t0 = time.perf_counter()
            md_content = _pdf_to_md(pdf_path)
            t_pdf2md = time.perf_counter() - t0
            if md_content is None:
                continue

            # 2. Structure-Aware Chunking
            t0 = time.perf_counter()
            chunks = _chunk_md(
                md_content,
                config.chunk_size,
                config.chunk_overlap,
            )
            t_chunking = time.perf_counter() - t0
            if chunks is None:
                continue

            # 3. Embedding & Vector Indexing
            t0 = time.perf_counter()
            _ = _create_and_store_embeddings(
                chunks,
                config.embedding_model_name,
                VECTOR_STORE_COLLECTION_NAME,
            )
            t_embed_and_indexing = time.perf_counter() - t0

            # Total time for this PDF
            t_tot = time.perf_counter() - t_start_tot

            # Save report for this PDF
            pdf_report = {
                PREPROCESSING_REPORT_DETAILS_PDF_ID_KEY: pdf_id,
                PREPROCESSING_REPORT_DETAILS_PDF2MD_TIME_KEY: round(
                    t_pdf2md,
                    3,
                ),
                PREPROCESSING_REPORT_DETAILS_CHUNKING_TIME_KEY: round(
                    t_chunking,
                    3,
                ),
                PREPROCESSING_REPORT_DETAILS_EMBED_AND_INDEXING_TIME_KEY: round(
                    t_embed_and_indexing,
                    3,
                ),
                PREPROCESSING_REPORT_DETAILS_TOT_TIME_KEY: round(t_tot, 3),
            }
            pdf_reports.append(pdf_report)

            # Cleanup temporary downloaded PDF
            os.remove(pdf_path)

        print("\033[K")

    # Averages and reporting
    if pdf_reports:
        # Average metrics across all PDFs
        avg_pdf2md = sum(
            m[PREPROCESSING_REPORT_DETAILS_PDF2MD_TIME_KEY]
            for m in pdf_reports
        ) / len(pdf_reports)
        avg_chunking = sum(
            m[PREPROCESSING_REPORT_DETAILS_CHUNKING_TIME_KEY]
            for m in pdf_reports
        ) / len(pdf_reports)
        avg_embed_and_indexing = sum(
            m[PREPROCESSING_REPORT_DETAILS_EMBED_AND_INDEXING_TIME_KEY]
            for m in pdf_reports
        ) / len(pdf_reports)
        avg_tot = sum(
            m[PREPROCESSING_REPORT_DETAILS_TOT_TIME_KEY] for m in pdf_reports
        ) / len(pdf_reports)

        # Print the benchmark report
        print("\n" + "=" * 56)
        print(
            f"| {f'[PREPROCESSING] BENCHMARK SUMMARY (PDFs: {len(pdf_reports)})':^52} |",
        )
        print("-" * 56)
        print(f"| {'Metric':<36} | {'Value':>13} |")
        print("-" * 56)
        print(
            f"| {'Avg. PDF to Markdown Conversion':<36} | {avg_pdf2md:>11.3f} s |",
        )
        print(
            f"| {'Avg. Structure-Aware Chunking':<36} | {avg_chunking:>11.3f} s |",
        )
        print(
            f"| {'Avg. Embedding & Vector Indexing':<36} | {avg_embed_and_indexing:>11.3f} s |",
        )
        print("-" * 56)
        print(f"| {'Avg. Total Time':<36} | {avg_tot:>11.3f} s |")
        print("=" * 56)

        print(
            f"Full benchmark report available at: {PREPROCESSING_REPORT_JSON_PATH}",
        )

        # Save the final report with a summary containing averages
        # and detailed metrics for each PDF
        final_report = {
            PREPROCESSING_REPORT_SUMMARY_KEY: {
                PREPROCESSING_REPORT_SUMMARY_TOT_PDFS_KEY: len(pdf_reports),
                PREPROCESSING_REPORT_SUMMARY_AVG_PDF2MD_TIME_KEY: round(
                    avg_pdf2md,
                    3,
                ),
                PREPROCESSING_REPORT_SUMMARY_AVG_CHUNKING_TIME_KEY: round(
                    avg_chunking,
                    3,
                ),
                PREPROCESSING_REPORT_SUMMARY_AVG_EMBED_AND_INDEXING_TIME_KEY: round(
                    avg_embed_and_indexing,
                    3,
                ),
                PREPROCESSING_REPORT_SUMMARY_AVG_TOT_TIME_KEY: round(
                    avg_tot,
                    3,
                ),
            },
            PREPROCESSING_REPORT_DETAILS_KEY: pdf_reports,
        }
        with open(PREPROCESSING_REPORT_JSON_PATH, "w") as f:
            json.dump(final_report, f, indent=2)


if __name__ == "__main__":
    run_benchmark()
