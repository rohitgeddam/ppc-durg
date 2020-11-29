from memberships.models import Member, Fee
from dateutil.relativedelta import relativedelta
from datetime import date


def scheculed_member_active_check():

    TODAY = date.today()
    EXTRA_DAYS = 10
    print(f"****SCHEDULED CHECK STARTED ON {TODAY}****")
    try:
        all_members = Member.objects.all()
        for member in all_members:
            deactivate_member = (
                TODAY
                >= member.fee.last().next_due_date + relativedelta(days=+EXTRA_DAYS)
            )
            if deactivate_member:
                member.is_active = False
                member.is_registeration_done = False
                member.registeration_step = 5
                member.save()
    except:
        print("ERROR")
    print("****SCHEDULED CHECK COMPLETED****")