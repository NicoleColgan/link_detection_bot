import logging
from pathlib import Path
from .analyser import LLMAnalyser
from .readers import read_text_file, read_pdf_file
from .http_client import normalise_url, get_response, build_response_info
from .reporter import write_csv

"""ARe we not vaildating the input????


"""
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s") # set up root logger with specified level and format that other modules will use

ALLOWED_EXT = (".md", ".html", ".pdf")  #immutable

class LinkChecker():
    def __init__(self, input_dir: str, output_dir: str, llm=None):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.analyser = LLMAnalyser(llm)
        self.results = []
    
    def gather_urls(self):
        found = set()   # no duplicates

        for p in self.input_dir.iterdir():
            if p.suffix.lower() in (".md", ".html"):
                found.update(read_text_file(str(p)))
            elif p.suffix.lower() == ".pdf":
                found.update(read_pdf_file(str(p)))
            else:
                logger.debug("Skipping %s", p.name)
        return sorted(normalise_url(url) for url in found)
    
    def run(self):
        urls = self.gather_urls()
        logger.info("Found %d urls", len(urls))

        for url in urls:
            resp = get_response(url)
            info = build_response_info(url, resp)

            # Call LLM
            verdict = self.analyser.check_link_validity(info)
            row = {
                "original_url": url,
                **verdict,
                "status_code": info.get("status_code"),
                "response_url": info.get("response_url")
            }
            self.results.append(row)
            logger.info(row)
        csv_path = write_csv(self.results, str(self.output_dir))
        logger.info("CSV report writen: %s", csv_path)
