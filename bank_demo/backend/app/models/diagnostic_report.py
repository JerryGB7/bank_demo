from typing import ClassVar
from datetime import datetime

class DiagnosticReport:
    registry: ClassVar[list["DiagnosticReport"]] = []

    def __init__(self, DR_id: int, service_call_id: int, file_url: str, notes: str, created_at: datetime = datetime.now):
        self.id = DR_id
        self.service_call_id = service_call_id
        self.file_url = file_url
        self.notes = notes
        self.created_at = created_at | datetime.now
        DiagnosticReport.registry.append(self)

    @classmethod
    def find_by_id(cls, dr_id: int) -> "DiagnosticReport | None":
        for dr in cls.registry:
            if dr_id == dr_id:
                return dr

        return None    

    def __repr__(self) -> str:
        return (f"Diagnostic Report attributes: {self.service_call_id}{self.file_url}{self.notes}{self.created_at}")