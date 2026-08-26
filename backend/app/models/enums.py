"""
first file that was created on day 1 revature training 
START HERE
"""

from enum import Enum

class ATMStatus(str, Enum):
    OPERATIONAL = "Operational"
    LOW_CASH = "Low-Cash"
    MAINTENANCE = "Maintenance"
    OFFLINE = "Offline"

class Service_Call_Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    CRITICAL = "Critical"

class Service_Call_Status(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In-Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"

class Technician_RBAC(str, Enum):
    OPERATION_MANAGER = "Operation-Manager"
    FIELD_TECHNICIAN = "Field-Technician"
    AUDITOR = "Auditor"    