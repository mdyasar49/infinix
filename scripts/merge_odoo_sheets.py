"""
Odoo Leads Merger and Enricher Script
Maintains backward compatibility and executes the enriched multi-tab master workbook pipeline.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enrich_and_update_odoo_master import main as run_enrichment_pipeline

if __name__ == "__main__":
    run_enrichment_pipeline()
