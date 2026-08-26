from app.models import Branch, ATM, DiagnosticReport, ServiceCall, Technician, ATMStatus, Service_Call_Status, Service_Call_Priority

def find_low_cash_atms(atms: list[ATM], threshold: int = 20) -> list[ATM]:
    return [
        atm for atm in atms
        if atm.status != ATMStatus.OFFLINE and atm.is_low_cash(threshold)
    ]

def find_atms_for_maintenance(atms: list[ATM]) -> list[ATM]:
    return[
        atm for atm in atms
        if atm.needs_maintenance()
    ]

def demo_seed_data() -> None:

    Branch(1, "Chase", "LA", capacity=50, manager_id=10)
    Branch(2, "Wells Fargo", "SG", capacity=50, manager_id=20)
    Branch(3, "America", "COM", capacity=50, manager_id=30)
    Branch(4, "EastWest", "ELM", capacity=50, manager_id=40)

    ATM(11, "LA089454", "chaseatm", cash_level=19, branch_id=1, status=ATMStatus.LOW_CASH)
    ATM(12, "LA089455", "chaseatm", cash_level=100, branch_id=1, status=ATMStatus.OPERATIONAL)
    ATM(21, "SG022222", "wellsatm", cash_level=50, branch_id=2, status=ATMStatus.OPERATIONAL)
    ATM(22, "SG022223", "wellsatm", cash_level=15, branch_id=2, status=ATMStatus.LOW_CASH)
    ATM(31, "COM03331", "americaatm", cash_level=10000, branch_id=3, status=ATMStatus.MAINTENANCE)
    ATM(32, "COM03332", "americaatm", cash_level=-10, branch_id=3, status=ATMStatus.OFFLINE)
    ATM(41, "ELM04441", "eastatm", cash_level=19, branch_id=4, status=ATMStatus.LOW_CASH)

    ServiceCall(1, "cash sensor not working", atm_id=31, technician_id=31, priority=Service_Call_Priority.CRITICAL, status=Service_Call_Status.IN_PROGRESS)
    ServiceCall(2, "cash sensor not working", atm_id=32, technician_id=31, priority=Service_Call_Priority.CRITICAL, status=Service_Call_Status.IN_PROGRESS)


def main() -> None:

    demo_seed_data()

    print("====FULL ATM REGISTRY====")
    for atm in ATM.registry:
        print(atm)

    print("====FIND ATMS NEEDING CASH====")
    alerts = find_low_cash_atms(ATM.registry, threshold=20)
    for atm in alerts:
        print(f"ATM {atm.serial_number} NEEDS CASH")

    print("====FIND ATMS NEEDING MAINTENANCE====")
    maintain = find_atms_for_maintenance(ATM.registry)
    for atm in maintain:
        print(f"ATM {atm.serial_number} NEEDS MAINTENANCE ")


if __name__ == "__main__":
    main()