from datetime import datetime, timedelta

test_date = datetime.now()
previous_month = test_date.month - 1
test_date = datetime(test_date.year, previous_month,1)

nxt_mnth = test_date.replace(day=28) + timedelta(days=4)
res = nxt_mnth - timedelta(days=nxt_mnth.day)
start_date = test_date
end_date = start_date + timedelta(days=res.day)
l1=[]
for i in range(0, res.day):
    l1.append(start_date)
    start_date = start_date + timedelta(days=1)


for i in l1:
    print(i.date())
