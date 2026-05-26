import logging
import os
from typing import List
from models.student import Student

logger = logging.getLogger(__name__)


class ReportService:

    def export_report(
        self,
        students: List[Student],
        summaries: List[str],
        topper: Student,
        avg: float,
        ranked_list: List[Student],
        file_path: str = "report.txt"
    ) -> str:

        if not students:
            raise ValueError("No students to export.")

        try:
            directory = os.path.dirname(file_path)
            
            if directory:
                os.makedirs(directory, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("Student Report\n")

                for s in summaries:
                    f.write(s + "\n")

                f.write(f"\nTop Performer: {topper.name}\n")
                f.write(f"Average Percentage: {avg:.2f}\n")

                f.write("\nRank List:\n")
                for s in ranked_list:
                    f.write(f"{s.name} - {s.percentage:.2f}%\n")

            logger.info(f"Report exported successfully: {file_path}")
            return file_path

        except Exception:
            logger.exception("Failed to export report")
            raise