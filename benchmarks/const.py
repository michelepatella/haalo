"""benchmarks/const.py"""

from pathlib import Path

########################################################################################
# General
########################################################################################
BENCHMARKS_DIR = Path(__file__).resolve().parent
PDF_URLS_JSON_PATH = BENCHMARKS_DIR / "pdf_urls.json"

########################################################################################
# Preprocessing
########################################################################################
PREPROCESSING_REPORT_SUMMARY_KEY = "summary"
PREPROCESSING_REPORT_SUMMARY_TOT_PDFS_KEY = "tot_pdfs"
PREPROCESSING_REPORT_SUMMARY_AVG_PDF2MD_TIME_KEY = "avg_pdf2md_s"
PREPROCESSING_REPORT_SUMMARY_AVG_CHUNKING_TIME_KEY = "avg_chunking_s"
PREPROCESSING_REPORT_SUMMARY_AVG_EMBED_AND_INDEXING_TIME_KEY = (
    "avg_embed_and_indexing_s"
)
PREPROCESSING_REPORT_SUMMARY_AVG_TOT_TIME_KEY = "avg_tot_s"

PREPROCESSING_REPORT_DETAILS_KEY = "details"
PREPROCESSING_REPORT_DETAILS_PDF_ID_KEY = "pdf_id"
PREPROCESSING_REPORT_DETAILS_PDF2MD_TIME_KEY = "pdf2md_s"
PREPROCESSING_REPORT_DETAILS_CHUNKING_TIME_KEY = "chunking_s"
PREPROCESSING_REPORT_DETAILS_EMBED_AND_INDEXING_TIME_KEY = (
    "embed_and_indexing_s"
)
PREPROCESSING_REPORT_DETAILS_TOT_TIME_KEY = "tot_s"

PREPROCESSING_REPORT_JSON_PATH = (
    BENCHMARKS_DIR / "preprocessing" / "report.json"
)
